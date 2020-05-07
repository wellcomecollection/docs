# RFC 025: Minting asset identifiers from filenames

**Last updated: 7 May 2020.**

## Background

Whether generated through photography during digitisation, or acquired in digital form, all assets enter workflows with a filename on disk:

* b12345678_0001.jp2
* bob-field-recording-june-1978.wav

We want to preserve this filename so that it is reflected in the URL of an asset on the web, which will usually be some sort of derivative. A IIIF Image service, or an mp3 created from a master audio file.

The filename is used to generate a meaningful identifier, that ends up in a URL path segment:

```
https://..../some-prefix/b28047345_0035.jp2/info.json
                         |--- asset id ---|
```

The filename is present in the METS file, and becomes the identifier for that asset.

## Problem

The filename can't always be used as-is, because:

* While unique within the METS file it might not be globally unique across all digitised content. This is not _usually_ the case for digitised image content, because the naming conventions in Goobi workflow should ensure uniqueness. In most but not all cases the Sierra b number forms the start of the filename. For AV content, the acquired file could have any name (e.g., my-film.mpeg).
* The filename might have characters in it that require escaping when used in a URL.

The second point is especially evident with spaces:

* Filename is `bob field recording june 1978.wav` (a perfectly valid filename).
* Derivative is available at https://..../some-prefix/bob field recording june 1978.wav

Which is equivalent to:

```
https://..../some-prefix/bob%20field%20recording%20june%201978.mp3
                         |------------- asset id ----------------|
```

The unescaped form is fragile when used in the real world (pasted into an email, for example). The escaped form is ugly and also is not visually the same as the original filename, regardless of any technical equivalence. Either way, usability of URLs is hurt.

## Solution

The filename needs to be transformed into a string appropriate for a URL path segment, by following a set of rules.

Independent software systems need to be able to deduce this path segment, given a filename in METS. Therefore they all need to implement the same rules.

The rules are:

* If the filename does not begin with the b number, prepend the b number followed by an underscore. This must be a case-insensitive comparison, and must prepend the b number with a lower-case "b".
* All spaces should be replaced with an underscore.
* TODO - define rules for percent-encoding and treatment of other characters. 

Examples:

```
my-image.jp2           => b12345678_my-image.jp2
b12345678_my-image.jp2 => (no change)
B12345678_my-image.jp2 => (no change)
my image.jp2           => b12345678_my_image.jp2
```




