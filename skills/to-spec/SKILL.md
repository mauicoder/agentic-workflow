---
name: to-spec
description: >-
  Synthesize the current conversation and codebase context into a formal feature
  specification and save it to docs/specs/<feature-slug>.md (or publish it to the
  configured issue tracker) without interviewing the user. Use when the user asks
  to create a spec, run /to-spec, or formalize a refined feature discussion.
---

# To Spec

This skill takes the current conversation context and codebase understanding and produces a formal specification. Do **not** interview the user; synthesize what has already been discussed.

## Tracker & Storage Resolution

Check `.agents/workflows/agentic-tdd-sdlc.yaml` if present, or follow the user's explicit instruction:
- **Phase Model:** `"Gemini 4 Argon"` (`models.specification`) — pass `model="Gemini 4 Argon"` explicitly when invoking spec-generation agents via `run_workflow` or `invoke_subagent`.
- **Local mode (default):** Write the specification to `docs/specs/<feature-slug>.md`.
- **External tracker (`github`, `gitlab`, `linear`):** Publish the specification to the project issue tracker and apply the `ready-for-agent` triage label.

## Process

1. **Explore the codebase:** If you have not already inspected the relevant modules, explore the repository to understand its current architecture. Use the project's domain glossary vocabulary throughout the spec, and respect any Architecture Decision Records (ADRs) in the area being modified.

2. **Identify testing seams:** Sketch out the seams at which the feature will be tested.
   - Prefer existing seams over creating new ones.
   - Choose the highest practical seam (public API, module boundary, or service interface).
   - Keep the number of seams minimal—ideally one primary seam.
   - Briefly confirm with the user that these testing seams match their expectations.

3. **Write and publish the spec:** Generate the specification using the template below and save it to `docs/specs/<feature-slug>.md` (or publish it to the configured issue tracker with the `ready-for-agent` label).

<spec-template>

# <Feature Title>

**Status:** ready-for-agent

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A comprehensive, numbered list of user stories covering all primary flows and edge cases. Each user story must follow the format:

1. As an `<actor>`, I want `<feature>`, so that `<benefit>`

<user-story-example>
1. As a mobile bank customer, I want to see the balance on my accounts, so that I can make better-informed decisions about my spending.
</user-story-example>

## Implementation Decisions

A list of architectural and technical decisions made during refinement:

- Modules to be built or modified
- Public interfaces and contracts to be introduced or updated
- Technical clarifications and domain constraints
- Architectural decisions
- Schema or data model changes
- API contracts and error semantics
- Specific module interactions

Do **not** include brittle file paths or full implementation code snippets that go stale quickly.
*Exception:* If a prototype or discussion produced a concise snippet that encodes a decision more precisely than prose can (e.g., a state machine, reducer signature, schema, or contract interface), inline only the decision-rich excerpt and note that it came from a prototype.

## Testing Decisions

A list of testing decisions for the TDD phase:

- **Testing philosophy:** Test external behavior at the public seam, not internal implementation details.
- **Target seams/modules:** Which module boundaries or interfaces will be tested.
- **Prior art:** Existing test patterns or fixtures in the codebase to follow.

## Out of Scope

Explicit boundaries of what is excluded from this specification.

## Further Notes

Any additional context, rollout considerations, or open notes.

</spec-template>
