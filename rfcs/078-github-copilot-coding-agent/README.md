# RFC 078: Working with GitHub Copilot coding agent

This RFC discusses how to work effectively with GitHub Copilot coding agent within the Wellcome Collection development team, establishing guidelines, processes, and best practices for successful adoption.

**Last modified:** 2025-07-29T12:41:03Z

## Context

GitHub Copilot coding agent represents a new paradigm in software development where an AI agent can work independently in the background to complete tasks, just like a human developer. Unlike traditional Copilot suggestions, the coding agent can autonomously:

- Analyze issues and requirements
- Write and modify code across multiple files
- Run tests and fix issues
- Create pull requests and respond to review feedback
- Work asynchronously while developers focus on other tasks

For a small development team like Wellcome Collection's, this technology offers significant potential to increase productivity and handle routine tasks, but requires careful consideration of workflows, quality control, and cost management.

## Proposal

### Working Model

The GitHub Copilot coding agent operates within a controlled environment:

**Technical Constraints:**
- **Sandboxed environment:** The agent operates in a restricted environment with an allow list for network requests
- **Tool access:** Has access to common development tools and dependency management repositories (e.g., npm, pip)
- **Branch restrictions:** Can only push changes to `copilot/` prefixed branches
- **Repository scope:** Issues must be in the same repository as the resulting PR

**Workflow:**
1. Agent analyzes the assigned issue
2. Creates and works on a `copilot/` prefixed branch
3. Implements solution iteratively with access to build/test tools
4. Creates PR and requests review when complete
5. Responds to review feedback and iterates on solution
6. Human reviewers can check out the branch and push additional changes if needed

**Transparency:**
- Full thought process visible via "view session" feature
- All changes tracked in standard git history
- Code review process remains unchanged

### Process Rules for Wellcome Collection

**Responsibility Assignment:**
- **Issue Assigner:** Responsible for the resulting PR and its quality
- **Prompting:** The assigner should be the primary person prompting the agent in PR discussions
- **Review Requirements:** All Copilot-authored PRs require review from a developer other than the assigner

**Quality Control:**
- Human review is mandatory - the agent can be convincingly wrong
- Reviewers should examine both the code and the agent's reasoning process
- Standard code review practices apply (testing, documentation, architecture)
- Consider the agent's solution as a starting point, not a final implementation

**Issue Assignment Guidelines:**
- Choose well-defined issues where the desired outcome is clear
- Prefer issues where you can confidently say "this one is easy, I know how to do it"
- Avoid open-ended or architectural decisions that require significant human judgment
- Ensure issues have clear acceptance criteria

### Cost Considerations

**Resource Usage:**
- Consumes GitHub Actions minutes (finite monthly allocation)
- Uses premium Copilot requests (300 per user per month on Business plan)
- Cost scales with complexity and iteration requirements

**Cost Management:**
- Monitor monthly usage against allocation
- Prioritize agent use for appropriate task types
- Track ROI by comparing agent time vs human development time
- Consider agent work as an investment in team productivity

### Guidelines for Effective Use

**Issue Preparation:**
- **Clear prompts:** Write detailed issue descriptions with specific outcomes
- **Repository instructions:** Leverage `.github/instructions/.instructions.md` for project-specific guidance
- **Acceptance criteria:** Define clear success metrics and testing requirements
- **Context:** Provide links to relevant documentation, similar implementations, or architectural decisions

**Work Patterns:**
- **Asynchronous work:** Assign issues and work on other tasks while the agent operates
- **Parallel development:** Use for independent features while team works on core functionality
- **Maintenance tasks:** Ideal for updates, refactoring, and routine improvements
- **Learning opportunities:** Review agent solutions to understand different approaches

**Optimal Task Types:**
- Bug fixes with clear reproduction steps
- Feature implementations with well-defined requirements
- Test addition or improvement
- Documentation updates
- Dependency updates and maintenance
- Code refactoring with clear objectives

## Potential Pitfalls and Considerations

**Quality Risks:**
- **Convincing incorrectness:** Agent may produce plausible but flawed solutions
- **Over-engineering:** May implement complex solutions for simple problems
- **Missing context:** Could miss important architectural or business considerations
- **Testing gaps:** May not consider all edge cases or integration scenarios

**Process Risks:**
- **Review bottleneck:** High-quality human review becomes the limiting factor
- **Skill atrophy:** Risk of reduced hands-on coding experience for team members
- **Dependency risk:** Over-reliance on agent for routine tasks

**Mitigation Strategies:**
- Maintain strong code review practices
- Use agent work as learning opportunities
- Ensure team members continue hands-on development
- Gradually increase agent responsibility as confidence grows
- Regular retrospectives on agent effectiveness

**Technical Considerations:**
- Agent solutions may not follow team coding conventions
- Limited understanding of legacy system quirks
- May not consider performance implications
- Could introduce new dependencies unnecessarily

## Alternatives Considered

**Traditional Development:** Continue with purely human development
- *Pros:* Full control, no new processes needed
- *Cons:* Misses productivity opportunities, doesn't leverage available tools

**Copilot Suggestions Only:** Use traditional Copilot without the coding agent
- *Pros:* Lower risk, familiar workflow
- *Cons:* Requires more human time, less autonomous task completion

**External AI Tools:** Use other AI coding platforms
- *Pros:* Potentially different capabilities
- *Cons:* Additional tooling, security concerns, integration challenges

## Impact

**Expected Benefits:**
- Increased team productivity for routine tasks
- Faster turnaround on well-defined issues
- More time for complex architectural and strategic work
- Learning opportunities from agent-generated solutions
- Reduced backlog of maintenance tasks

**Potential Challenges:**
- Learning curve for effective agent interaction
- Adjustment of review processes and quality gates
- Initial overhead in issue preparation and context setting
- Need for clear guidelines and team training

**Success Metrics:**
- Reduction in time-to-completion for appropriate issue types
- Maintained or improved code quality metrics
- Team satisfaction with agent collaboration
- Cost-effectiveness compared to human development time

## Next Steps

1. **Pilot Program:** Start with 2-3 well-defined, low-risk issues per sprint
2. **Guidelines Documentation:** Create team-specific prompting guidelines and examples
3. **Review Process:** Establish review checklist specifically for agent-generated code
4. **Repository Instructions:** Enhance `.github/instructions/.instructions.md` with project context
5. **Team Training:** Conduct workshops on effective agent collaboration
6. **Monitoring Setup:** Track usage, costs, and success rates
7. **Regular Retrospectives:** Weekly reviews of agent effectiveness and process improvements
8. **Gradual Scale-up:** Increase agent usage based on team comfort and demonstrated value

**Timeline:**
- Week 1-2: Team training and initial guidelines
- Week 3-4: Pilot with simple issues
- Week 5-8: Iterate on processes and expand usage
- Month 2+: Full integration with regular retrospectives

**Dependencies:**
- GitHub Copilot Business plan subscription
- Team buy-in and training completion
- Established code review processes
- Clear issue backlog with appropriate candidates