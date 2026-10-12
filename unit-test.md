---
name: unit-test-writer
description: Generate unit tests from a markdown spec or documentation file (SKILL.md, API docs, feature spec, etc). Use this skill whenever the user wants to write unit tests, test cases, or a test plan from a spec or documentation file — including after Executor produces new code, when a SKILL.md is ready to test, or when any markdown spec needs coverage. Always use this skill when the user says "bikin unit test", "tulis test", "test coverage", or passes a .md file and asks for tests.
---

# Unit Test Writer

An agent skill for the HITL-Work pipeline. Takes a markdown spec (SKILL.md, feature doc, API contract, etc.) and produces a structured **Test Plan** first, then generates the **test code** — language-agnostic by design, adapting to whatever stack is declared in the spec or inferred from context.

---

## Input

A markdown file passed by the user or piped from the Executor agent. Can be:
- `SKILL.md` — skill spec with behavior descriptions
- Feature spec / PRD fragment
- API contract or endpoint documentation
- Any `.md` describing expected behavior, inputs, and outputs

---

## Workflow

### Phase 1 — Read & Analyze the Spec

Before writing anything, read the entire markdown file and extract:

1. **What is being built?** — summarize the component/module/skill in 1–2 sentences
2. **What are the inputs?** — parameters, types, required vs optional
3. **What are the expected outputs?** — return values, side effects, file outputs
4. **What are the edge cases mentioned or implied?** — missing inputs, invalid types, empty states, boundary values
5. **What are the success criteria?** — explicit assertions the spec defines or implies
6. **What is the tech stack?** — detect from: file paths, code snippets, import statements, or framework mentions in the spec. If ambiguous, ask the user before proceeding.

---

### Phase 2 — Generate Test Plan

Output a structured test plan in this format before writing any code:

```
## Test Plan: [Component Name]

### Stack
- Language: [detected or confirmed]
- Test Framework: [e.g. PHPUnit, Go testing, Jest, PyTest, etc.]

### Test Cases

| # | Case | Input | Expected Output | Category |
|---|------|-------|-----------------|----------|
| 1 | Happy path: ... | ... | ... | happy |
| 2 | Edge: empty input | null / "" | error / fallback | edge |
| 3 | Invalid type | wrong type | throws / returns error | negative |
| ... | | | | |

### Coverage Goals
- [ ] All required inputs tested
- [ ] At least 1 negative/invalid input per required param
- [ ] Edge cases: empty, null, boundary values
- [ ] Side effects covered (if any)
```

**Stop here and present the Test Plan to the user.** Wait for confirmation or revision before proceeding to Phase 3.

---

### Phase 3 — Generate Test Code

After the user approves the Test Plan, generate the test code:

#### Universal Rules (applies to all stacks)

- One test function per test case from the plan — no bundling multiple cases into one test
- Each test must have a **descriptive name** that mirrors the case description
- Use the **AAA pattern**: Arrange → Act → Assert
- Mock external dependencies (DB, API calls, filesystem) — never hit real services in unit tests
- Tests must be **isolated** — no shared state between test functions
- Include a comment block at the top of the file: source spec, date generated, and coverage summary

#### Stack-Specific Conventions

**PHP / CodeIgniter 4 (PHPUnit)**
```php
// Use CIUnitTestCase for CI4 components
// Mock using Mockery or PHPUnit's built-in mock builder
// Place in tests/unit/ following CI4 structure
// Run with: php spark test
```

**Go**
```go
// Use standard testing package
// Table-driven tests preferred for multiple cases
// Use testify/assert for cleaner assertions if available
// Place in same package as source with _test.go suffix
```

**JavaScript / TypeScript (Jest / Vitest)**
```ts
// Use describe() to group by component
// Use it() or test() for individual cases
// Mock with jest.mock() or vi.mock()
// Prefer ts-jest for TypeScript projects
```

**Python (PyTest)**
```python
# Use pytest fixtures for setup/teardown
# Parametrize where multiple inputs test same logic
# Mock with unittest.mock or pytest-mock
# Place in tests/ with test_ prefix
```

**If stack is unknown or not in the list above:**
Produce the test in **pseudocode-style comments first**, then ask the user which language to transpile into.

---

### Phase 4 — Output Delivery

Deliver the test file with:

1. A brief **coverage summary** — how many cases, which categories covered
2. **Instructions to run** — exact command for the detected stack
3. **What's NOT covered** — explicitly list anything the spec implied but wasn't testable from the markdown alone (e.g., needs live DB, needs real API key, UI interaction)
4. A note on **next steps**: which agent in the HITL pipeline should run next (typically QA Agent or Debug Agent)

---

## HITL Pipeline Position

```
Planner → Executor → [Unit Test Writer] → QA Agent → Debug Agent → Review Agents
```

This skill sits **after Executor** and **before QA**. Its output (test files) feeds directly into the QA Agent's verification step.

If called standalone (user passes a spec manually), still follow the same 4-phase workflow.

---

## Quality Checklist Before Delivering

- [ ] Test plan was shown and approved before code was generated
- [ ] Every test case in the plan has a corresponding test function
- [ ] No test depends on another test's state
- [ ] External dependencies are mocked
- [ ] File includes a run command
- [ ] "Not covered" section is honest and complete
