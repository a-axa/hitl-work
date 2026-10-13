---
name: hitl-work
description: Human-in-the-loop multi-agent coding workflow (Decomposer → Planner → Executor → Unit Test Writer → QA → Specialist Reviews) with 17 agents for structured development. ALWAYS use this skill when user wants to decompose a PRD into tasks, plan a feature/spec/PRD (including necessity/duplication/security/performance checks), execute a prd.md step-by-step, verify/QA implementation, doubt-review a spec, or run architecture/security/performance/migration/API/debug/refactor reviews — including Indonesian triggers like 'decompose', 'buatin prd', 'plan fitur', 'kerjain sesuai prd', 'QA dulu', 'cek security', 'audit', 'debug', 'refactor', even if user doesn't say HITL. Do NOT trigger for one-liner utilities, commit messages, simple code snippets, file reads, installs, SQL one-offs, translations, weather, or casual 'looks good' reviews where no formal spec/execution/verification separation is needed. Make sure to use this skill whenever the task benefits from separated planning, implementation, and verification responsibilities.
---

# HITL·Work — Multi-Agent Development Workflow

One agent, one responsibility. Planner doesn't write code. Executor doesn't think about architecture. QA trusts nothing without verification.

## Pipeline

```
(Decomposer) → Planner → (Doubt Review) → Executor → (Unit Test Writer) → QA → (Specialist Reviews) → Documentation/Skill Extractor
```

**When to start where:**
- Large PRD spanning many modules → start at **Decomposer**
- Single feature / bug / refactor with clear scope → start at **Planner**
- Spec already exists (`prd.md`) → start at **Executor**
- Code already written → start at **QA** or specialist review
- Existing code needs triage → start at **Debug**
- Markdown spec/SKILL.md ready to test → start at **Unit Test Writer**

## Agents

| Agent | File | When to load |
|-------|------|-------------|
| Decomposer | `decomposer.md` | PRD too large for one spec |
| Planner | `planner.md` | New feature/bug/refactor, no spec yet |
| Doubt Review | `doubt-review.md` | After Planner, before Executor (risky/multi-tenant/DB/migration changes) |
| Executor | `executor.md` | `prd.md` exists, ready to implement |
| Unit Test Writer | `unit-test-writer.md` | After Executor — generate test plan + test code from markdown spec |
| QA | `qa.md` | Executor reports "Ready for QA" |
| Architecture Review | `architecture-review.md` | Structure, layer boundaries, duplication |
| Security Review | `security-review.md` | New endpoints, auth, input handling, external APIs |
| Performance Review | `performance-review.md` | N+1, indexing, caching, scalability |
| Migration Review | `migration-review.md` | Any DB migration |
| Refactor Agent | `refactor-agent.md` | Code works but needs cleanup plan |
| API Agent | `api-agent.md` | DESIGN / INTEGRATION / AUDIT of HTTP APIs |
| Debug Agent | `debug.md` | Root-cause investigation (does not fix) |
| Documentation | `documentation.md` | After QA passes, write docs from actual code |
| Skill Extractor | `skill-extractor.md` | After QA, distill patterns into `skill.md` |
| UI/UX Planner | `ui-ux-planner.md` | Planner delegates when UI complexity is high |
| UI Skill Extractor | `ui-skill-extractor.md` | After QA, extract visual tokens/components |

## Instructions

1. **Read the agent file before acting.** Each `.md` file is the agent's full system prompt. Do not summarize or paraphrase from memory — read it.
2. **Follow the agent's process exactly.** Planner never writes code. Executor never improvises. QA never approves without reading code. These boundaries are intentional.
3. **Respect pipeline order.** Do not skip Planner to write code. Do not skip QA to ship. Doubt Review is cheap before execution, expensive after.
4. **HITL checkpoints:**
   - After Decomposer → stop, human reviews `task-N.md` list before Planner.
   - After Planner → optionally run Doubt Review before handing to Executor.
   - After Executor → optionally run Unit Test Writer before QA (recommended for non-trivial logic).
   - After Unit Test Writer → QA verifies using generated tests as baseline.
   - After Executor/QA → on FAIL, return to Executor with fixes.
5. **Specialist reviews report only.** Architecture/Security/Performance/Migration/Refactor agents never fix — they produce findings for Executor to address.
6. **Close the loop** with Documentation and Skill Extractor after QA passes — document what was actually built, not what was planned.

## Workflow Steps

### 1. Decompose (optional)
Read `decomposer.md` and follow it. Output `task-N.md` files. Stop for human review.

### 2. Plan
Read `planner.md` and follow it. Read relevant skill files for the codebase first. Output `prd.md` with Necessity Check, Reusability Assessment, Duplication Scan, Security/Performance/Observability/UI-UX considerations, Scope, Files to Modify/Create, Steps, Expected Behavior, Breaking Changes, What NOT to Touch, and Definition of Done.

### 3. Doubt Review (optional but recommended for risky changes)
Read `doubt-review.md` and follow it. Verdict: READY / BLOCKED / NEEDS CLARIFICATION. Only proceed to Executor on READY.

### 4. Execute
Read `executor.md` and follow it. One step at a time, minimal scope, match existing patterns. Report per-step completion or `Partial Execution Report` if blocked.

### 5. Unit Test Writer (optional but recommended for non-trivial logic)
Read `unit-test-writer.md` and follow it. Pass the relevant markdown spec or SKILL.md as input. Two phases: Test Plan (stop for human approval) → Test Code. Output test files ready for QA to use as verification baseline.

### 6. QA
Read `qa.md` and follow it. Four phases: Spec Compliance → Breaking Changes → Definition of Done → Code Quality. If Unit Test Writer ran, use generated tests as part of verification. Verdict: PASS / FAIL / PASS WITH WARNINGS.

### 7. Specialist Reviews (as needed, can run in parallel)
Read the relevant `*-review.md` or `api-agent.md`/`debug.md` and follow it. Each produces a report with findings classified by severity. Route findings back to Executor.

### 8. Documentation & Skill Extraction
Read `documentation.md` / `skill-extractor.md` / `ui-skill-extractor.md` and follow them. Write docs from actual implementation.

## Rules

- Never let one agent do another's job. If the user asks to "plan and implement" in one turn, run Planner first, output the spec, then wait for confirmation before Executing.
- Always read the codebase skill files referenced in Planner step 2 before speccing.
- Always include "What NOT to Touch" and "Breaking Changes" in every spec — Planner enforces this.
- Executor stops and asks on ambiguity — never silently improvises.
- Unit Test Writer never skips the Test Plan phase — always get human approval before generating test code.
