#!/usr/bin/env python3
"""Validate the RFC 089 Identifiers API OpenAPI spec and render it to Markdown.

`openapi.yaml` is the source of truth. This script validates it and (re)writes
`openapi.md` so the contract is browsable on GitHub without a Swagger/Redoc
renderer. Run after editing the spec:

    uv run python render_docs.py
"""

import pathlib
import sys

import yaml
from openapi_spec_validator import validate

HERE = pathlib.Path(__file__).resolve().parent
SPEC_PATH = HERE / "openapi.yaml"
OUT_PATH = HERE / "openapi.md"

HTTP_METHODS = ["get", "put", "post", "delete", "patch", "options", "head"]


def clean(text):
    """Collapse whitespace and escape pipes so text is safe in a table cell."""
    if not text:
        return ""
    return " ".join(str(text).split()).replace("|", "\\|")


def anchor(name):
    """GitHub-style heading anchor for a schema name."""
    return name.lower()


def ref_name(ref):
    return ref.rsplit("/", 1)[-1]


def type_str(schema):
    """A short human-readable type description for a schema fragment."""
    if not schema:
        return ""
    if "$ref" in schema:
        name = ref_name(schema["$ref"])
        return f"[`{name}`](#{anchor(name)})"
    if "const" in schema:
        return f"`{schema['const']}` (const)"
    t = schema.get("type")
    base = " or ".join(t) if isinstance(t, list) else (t or "")
    if base == "array":
        inner = type_str(schema.get("items", {}))
        return f"array of {inner}" if inner else "array"
    if base == "object":
        ap = schema.get("additionalProperties")
        if isinstance(ap, dict):
            return f"object (map to {type_str(ap)})"
        return "object"
    fmt = schema.get("format")
    if fmt:
        return f"{base} ({fmt})"
    if "enum" in schema:
        return f"{base} (enum: {', '.join(map(str, schema['enum']))})"
    return base


def properties_table(schema):
    """Render an object schema's properties as a Markdown table."""
    props = schema.get("properties")
    if not props:
        return []
    required = set(schema.get("required", []))
    lines = [
        "| Property | Type | Required | Description |",
        "|---|---|---|---|",
    ]
    for name, prop in props.items():
        req = "yes" if name in required else "no"
        lines.append(
            f"| `{name}` | {type_str(prop) or 'n/a'} | {req} | {clean(prop.get('description'))} |"
        )
    return lines


def resolve_param(param, spec):
    if "$ref" in param:
        return spec["components"]["parameters"][ref_name(param["$ref"])]
    return param


def security_str(security):
    """Render an operation's security requirement list."""
    if not security:
        return "None"
    parts = []
    for requirement in security:
        schemes = []
        for scheme, scopes in requirement.items():
            schemes.append(f"`{scheme}`" + (f" ({', '.join(scopes)})" if scopes else ""))
        parts.append(" + ".join(schemes))
    return " or ".join(parts)


def render_operation(method, path, op, path_params, spec):
    lines = [f"#### `{method.upper()} {path}`", ""]
    if op.get("summary"):
        lines += [f"_{clean(op['summary'])}_", ""]
    if op.get("description"):
        lines += [op["description"].strip(), ""]
    # Operation-level security overrides the document-level default when present.
    op_security = op.get("security", spec.get("security"))
    lines += [f"**Security:** {security_str(op_security)}", ""]

    # Parameters (path-level + operation-level), resolving any $refs.
    params = [resolve_param(p, spec) for p in (path_params + op.get("parameters", []))]
    if params:
        lines += [
            "**Parameters:**",
            "",
            "| Name | In | Required | Type | Description |",
            "|---|---|---|---|---|",
        ]
        for p in params:
            req = "yes" if p.get("required") else "no"
            lines.append(
                f"| `{p['name']}` | {p.get('in', '')} | {req} | "
                f"{type_str(p.get('schema', {})) or 'n/a'} | {clean(p.get('description'))} |"
            )
        lines.append("")

    # Request body.
    body = op.get("requestBody")
    if body:
        schema = body.get("content", {}).get("application/json", {}).get("schema", {})
        required = " (required)" if body.get("required") else ""
        lines += [f"**Request body**{required}:", ""]
        if "$ref" in schema:
            lines += [f"- {type_str(schema)}", ""]
        else:
            table = properties_table(schema)
            lines += (table + [""]) if table else [f"- {type_str(schema) or 'object'}", ""]

    # Responses.
    lines += [
        "**Responses:**",
        "",
        "| Status | Body | Description |",
        "|---|---|---|",
    ]
    for status, resp in op.get("responses", {}).items():
        schema = resp.get("content", {}).get("application/json", {}).get("schema", {})
        lines.append(
            f"| `{status}` | {type_str(schema) or 'n/a'} | {clean(resp.get('description'))} |"
        )
    lines.append("")
    return lines


def render(spec):
    info = spec.get("info", {})
    lines = [
        f"# {info.get('title', 'API')}",
        "",
        "> Generated from [`openapi.yaml`](openapi.yaml) by `render_docs.py`. "
        "Do not edit by hand.",
        "> Regenerate with `uv run python render_docs.py`.",
        "",
        f"**Version:** `{info.get('version', '')}`",
        "",
    ]
    if info.get("description"):
        lines += [info["description"].strip(), ""]

    if spec.get("servers"):
        lines += ["## Servers", ""]
        for server in spec["servers"]:
            desc = f": {server['description']}" if server.get("description") else ""
            lines.append(f"- `{server['url']}`{desc}")
        lines.append("")

    # Group operations by tag, in declared tag order (then any extras).
    tag_defs = spec.get("tags", [])
    tag_order = [t["name"] for t in tag_defs]
    tag_desc = {t["name"]: t.get("description", "") for t in tag_defs}
    by_tag = {name: [] for name in tag_order}

    for path, item in spec.get("paths", {}).items():
        path_params = item.get("parameters", [])
        for method in HTTP_METHODS:
            if method not in item:
                continue
            op = item[method]
            for tag in op.get("tags", ["(untagged)"]):
                by_tag.setdefault(tag, [])
                if tag not in tag_order:
                    tag_order.append(tag)
                by_tag[tag].append((method, path, op, path_params))

    lines += ["## Operations", ""]
    for tag in tag_order:
        ops = by_tag.get(tag)
        if not ops:
            continue
        lines += [f"### Tag: {tag}", ""]
        if tag_desc.get(tag):
            lines += [clean(tag_desc[tag]), ""]
        lines += ["| Method | Path | Summary |", "|---|---|---|"]
        for method, path, op, _ in ops:
            lines.append(f"| `{method.upper()}` | `{path}` | {clean(op.get('summary'))} |")
        lines.append("")
        for method, path, op, path_params in ops:
            lines += render_operation(method, path, op, path_params, spec)

    # Schemas.
    schemas = spec.get("components", {}).get("schemas", {})
    if schemas:
        lines += ["## Schemas", ""]
        for name, schema in schemas.items():
            lines += [f"### {name}", ""]
            if schema.get("description"):
                lines += [clean(schema["description"]), ""]
            if schema.get("required"):
                lines += [
                    "**Required:** " + ", ".join(f"`{r}`" for r in schema["required"]),
                    "",
                ]
            table = properties_table(schema)
            if table:
                lines += table + [""]
            elif not schema.get("description"):
                lines += [f"Type: {type_str(schema) or 'object'}", ""]

    return "\n".join(lines).rstrip() + "\n"


def main():
    if not SPEC_PATH.exists():
        sys.exit(f"Spec not found: {SPEC_PATH}")
    try:
        with SPEC_PATH.open(encoding="utf-8") as f:
            spec = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        sys.exit(f"Could not parse {SPEC_PATH.name} as YAML:\n{exc}")

    try:
        validate(spec)
    except Exception as exc:  # openapi-spec-validator raises a validation error subclass
        sys.exit(f"OpenAPI spec validation failed:\n{exc}")

    OUT_PATH.write_text(render(spec), encoding="utf-8")
    print(f"Spec valid. Wrote {OUT_PATH.relative_to(HERE.parent.parent)}")


if __name__ == "__main__":
    main()
