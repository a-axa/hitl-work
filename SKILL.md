---
name: hitl-work
description: "Human-in-the-loop multi-agent coding workflow with 17 agents. Use when: decompose PRD, plan feature/spec, execute prd.md, QA, doubt/security/architecture/performance/migration/API/debug/refactor/unit-test review. Indonesian triggers: buatin prd, plan fitur, kerjain sesuai prd, QA dulu, cek security, audit, debug, refactor, bikin unit test. Skip for: one-liners, commit messages, simple snippets, file reads, SQL one-offs, translations."
---

# HITL·Work

One agent, one responsibility. Planner doesn't write code. Executor doesn't improvise. QA trusts nothing without verification.

## Pipeline
```
(Decomposer) -> Planner -> (Doubt Review) -> Executor -> (Unit Test Writer) -> QA -> (Specialist Reviews) -> Docs/Skill Extractor
```

## Workflow State & Artifacts

For each non-trivial feature, create `.hitl-work/features/<feature-slug>/` and copy `workflow-state.template.md` to `status.md`. Every agent must read the state before acting and update only the fields belonging to its role before handoff. Keep the artifact index, routing decisions, findings ledger, and verification evidence current at every handoff.

Store feature artifacts in that directory: `prd.md`, `doubt-review.md`, `test-plan.md`, `qa-report.md`, `ui-spec.md`, and `reviews/<specialist>.md`. Do not overwrite another feature's root-level artifacts.

**Start where:**
- Large PRD -> **Decomposer**
- New feature/bug/refactor -> **Planner**
- `prd.md` ready -> **Executor**
- Code written -> **QA** or specialist review
- Code needs triage -> **Debug**
- Markdown spec to test -> **Unit Test Writer**

## Agents

| Agent | File | When |
|-------|------|------|
| Decomposer | `decomposer.md` | PRD too large for one spec |
| Planner | `planner.md` | No spec yet |
| Doubt Review | `doubt-review.md` | After Planner, before Executor — risky/multi-tenant/DB changes |
| Executor | `executor.md` | `prd.md` exists |
| Unit Test Writer | `unit-test-writer.md` | After Executor — test plan + code from markdown spec |
| QA | `qa.md` | After Executor reports done |
| Architecture Review | `architecture-review.md` | Layer boundaries, duplication |
| Security Review | `security-review.md` | New endpoints, auth, input handling |
| Performance Review | `performance-review.md` | N+1, indexing, caching |
| Migration Review | `migration-review.md` | Any DB migration |
| Refactor Agent | `refactor-agent.md` | Code works but needs cleanup |
| API Agent | `api-agent.md` | DESIGN / INTEGRATION / AUDIT |
| Debug Agent | `debug.md` | Root-cause investigation (no fixes) |
| Documentation | `documentation.md` | After QA passes |
| Skill Extractor | `skill-extractor.md` | After QA, distill patterns |
| UI/UX Planner | `ui-ux-planner.md` | When Planner delegates UI |
| UI Skill Extractor | `ui-skill-extractor.md` | After QA, extract visual tokens |

## Required Routing

| Change condition | Required stages |
|---|---|
| New endpoint, auth/authz, webhook, user-controlled input, external API | Security Review |
| Schema change, index, backfill, or data migration | Doubt Review + Migration Review |
| New query, bulk operation, caching, queue/job, or high-traffic endpoint | Performance Review |
| Cross-module change, new architectural pattern, or substantial refactor | Architecture Review |
| New screen, critical UI flow, reusable UI component, or substantial redesign | UI/UX Planner; UI Skill Extractor after QA |
| Non-trivial business logic | Unit Test Writer, including approved Test Plan |
| Bug with unknown root cause | Debug Agent before planning a fix |

A required stage may be skipped only when `status.md` records the reason and the human accepts the risk.

## Re-verification Loop

1. QA or specialist findings receive IDs (`QA-001`, `SEC-001`, `PERF-001`, and so on) in `status.md`.
2. Executor fixes only approved findings and marks them `Fixed` with the changed files.
3. QA verifies the regression after every fix. The specialist who reported a Critical finding re-checks it before closure.
4. A finding is closed only as `Fixed`, `Accepted risk` (human decision recorded), or `Deferred` (owner and follow-up recorded).

## Instructions

1. **Read the agent file before acting.** Never summarize from memory.
2. **Follow each agent's process exactly.** Boundaries are intentional.
3. **Respect pipeline order.** Don't skip Planner to write code. Don't skip QA to ship.
4. **HITL checkpoints:**
   - After Decomposer -> stop, human reviews task list.
   - After Planner -> optionally run Doubt Review.
   - After Executor -> optionally run Unit Test Writer (recommended for non-trivial logic).
   - After Unit Test Writer -> QA uses generated tests as baseline.
   - QA FAIL -> return to Executor.
5. **Specialist reviews report only** — findings go back to Executor to fix.
6. **Close the loop** with Docs + Skill Extractor after QA passes.

## Workflow

1. **Decompose** *(optional)* — `decomposer.md`. Output `task-N.md`. Stop for review.
2. **Plan** — `planner.md`. Output `prd.md`: Necessity Check, Duplication Scan, Security/Perf/UI-UX, Scope, Files, Steps, Breaking Changes, What NOT to Touch, DoD.
3. **Doubt Review** *(optional)* — `doubt-review.md`. Verdict: READY / BLOCKED / NEEDS CLARIFICATION.
4. **Execute** — `executor.md`. One step at a time. Stop on ambiguity.
5. **Unit Test Writer** *(optional)* — `unit-test-writer.md`. Test Plan -> approval -> Test Code.
6. **QA** — `qa.md`. Spec Compliance -> Breaking Changes -> DoD -> Code Quality. Verdict: PASS / FAIL / PASS WITH WARNINGS.
7. **Specialist Reviews** *(required by the routing table; otherwise as needed, parallel ok)* — findings by severity -> Executor -> re-verification.
8. **Docs & Skill Extraction** — write from actual implementation, not the plan, after all blocking findings are closed.

## Rules

- Never let one agent do another's job.
- Always read codebase skill files before speccing.
- Every spec must include "What NOT to Touch" and "Breaking Changes".
- Executor stops and asks on ambiguity — never improvises.
- Unit Test Writer never skips Test Plan approval.
