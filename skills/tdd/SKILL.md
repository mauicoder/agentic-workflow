---
name: tdd
description: >-
  Execute a strict Test-Driven Development (Red-Green-Refactor) cycle to implement
  a feature slice or ticket. Use when implementing a ticket from implement-spec,
  fixing a bug test-first, or when the user asks to build something using TDD.
---

# Test-Driven Development (Red-Green-Refactor)

Implement behavior using a strict, iterative **Red → Green → Refactor** loop. Test external behavior through public interfaces and seams rather than internal implementation details.

> **Model Configuration:** Parallel ticket implementation and TDD coding agents run on `"Gemini 4 Hydrogen"` (`models.implementation` / `subagents.models.coding` in `.agents/workflows/agentic-tdd-sdlc.yaml`), with `model="Gemini 4 Hydrogen"` passed explicitly on agent instantiation.

## Core Principles

1. **Test Behavior, Not Implementation:** Write tests at the highest practical seam (public API, module boundary, or service contract). Avoid coupling tests to private helpers or internal state.
2. **Contract-First:** If the ticket introduces or modifies a shared boundary, define the interface/types first so tests and callers can compile against the contract.
3. **One Slice of Behavior at a Time:** Do not write all tests upfront. Cycle through Red → Green → Refactor one acceptance criterion or edge case at a time.
4. **Never Skip Verification:** Always execute the project's test runner at every transition (Red, Green, and post-Refactor).

## The TDD Loop

Repeat the following three steps for each acceptance criterion in the ticket until all criteria are satisfied:

### 1. RED — Write a Failing Test

1. Identify the next unimplemented acceptance criterion or behavior from the ticket/spec.
2. Write a focused automated test that expresses the expected external behavior.
3. Run the test suite to verify the test fails **for the expected reason** (e.g., assertion failure or missing behavior, not a syntax or test-setup error).
   - *If the test passes immediately:* Check whether the behavior already exists or if the test assertion is vacuous.

### 2. GREEN — Write Minimum Production Code to Pass

1. Write the simplest production code required to make the failing test pass without breaking existing tests.
2. Avoid speculative generality, premature abstractions, or extra features not demanded by the current test.
3. Run the test suite and confirm **all** tests pass.

### 3. REFACTOR — Clean Up While Staying Green

1. Inspect both the newly written production code and test code for smells:
   - Duplicated logic or setup
   - Unclear naming (`Mysterious Name`)
   - Long functions or `Data Clumps`
   - Accidental coupling across module boundaries
2. Refactor in small steps to improve clarity and adhere to the repository's coding standards.
3. Re-run the test suite after refactoring to verify everything remains green.

## Completion Checklist

Before marking a ticket complete or committing:
- [ ] Every acceptance criterion in the ticket is covered by automated tests.
- [ ] All unit/integration tests in the affected area pass.
- [ ] Type-checkers and linters (if configured in the repository) pass with zero errors.
- [ ] No unrelated files or speculative features were introduced.
