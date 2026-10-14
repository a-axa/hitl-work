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

For each non-trivial feature, create `.hitl-work/features/<feature-slug>/` and copy `workflow-state.template.md` to `status.md`. Every agent must read the state before acting and update only the fields belonging to its role before handoff. Keep the artifact index, routing decisions, findings ledger, verification evidence, and a one-row Session Log entry current at every handoff. The Session Log is a concise chronology, not a transcript.

Store feature artifacts in that directory: `prd.md`, `doubt-review.md`, `test-plan.md`, `qa-report.md`, `ui-spec.md`, and `reviews/<specialist>.md`. Do not overwrite another feature's root-level artifacts.

**Start where:**
- Large PRD -> **Decomposer**
- New feature/bug/refactor -> **Planner**
- `prd.md` ready -> **Executor**
- Code written -> **QA** or specialist review
- Code needs triage -> **Debug**
- Markdown spec to test -> **Unit Test Writer**

## Companion Skill: anti-slop (opt-in)

HITL·Work pairs well with [anti-slop](https://github.com/miqdadbadjuber/anti-slop), a skill set that filters generic AI-generated code, UI, and copy. Integration is strictly opt-in. Run this gate ONCE per project, BEFORE any agent runs:

1. **Detect.** Run `npx skills list | grep -i antislop`. If nothing matches, inspect the active agent's skill directories (`.claude/skills/`, `.agents/skills/`, `~/.claude/skills/`, `~/.agents/skills/`, or the equivalent). The result must be exactly one of: INSTALLED or NOT INSTALLED. Write the result to `.hitl-work/preferences.md` (create `.hitl-work/` and the file if they do not exist).
2. **Gate.** If the result is NOT INSTALLED and `.hitl-work/preferences.md` contains no `antislop:` entry: STOP. Do not start the Planner, Executor, QA, or any other agent. Ask the user exactly this: "anti-slop is not installed. Install it and combine with HITL·Work so QA and Documentation also check outputs for AI slop? (yes / yes, always / no / never ask again)". Wait for the user's answer, then:
   - `yes` → run `npx skills add miqdadbadjuber/anti-slop`; record `antislop: installed` in `.hitl-work/preferences.md`.
   - `yes, always` → same as `yes`, plus record in `~/.hitl-work/preferences.md` so future projects skip this gate.
   - `no` → record `antislop: declined` in `.hitl-work/preferences.md`; continue without it.
   - `never ask again` → record in `~/.hitl-work/preferences.md`; never run this gate again on any project.
   Only after the answer is recorded may the pipeline continue.
3. **Combine only when present.** When the anti-slop skill is available (pre-installed or just installed), the QA and Documentation agents must read its core rules and add an explicit slop check to their verdicts: reject generic AI-pattern code, copy, and UI. Note: `npx skills add` copies the skill folders but does not write a session auto-load pointer; HITL·Work agents load the anti-slop rules explicitly, so no pointer is needed.

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

## Workflow Modes

Select a mode before acting and record it in `status.md`. If the user explicitly requests a mode, use it only when it satisfies the eligibility rules. Otherwise choose the lowest safe mode. Any risk signal escalates the work immediately; never use Quick mode to bypass a required review.

| Mode | Use for | Required path | Not allowed when |
|---|---|---|---|
| 🔴 **Full Pipeline** | New feature, multi-module work, migration, security-sensitive change, external integration, unclear/high blast radius | Decomposer when scope needs splitting → full Planner → required reviews → Executor → tests when applicable → QA → docs/skill extraction as applicable | Never downgrade merely to save time |
| 🟡 **Standard** | Scoped bug fix or enhancement, understood root cause, normally 1–2 files and no high-risk surface | Planner Lite → Executor → QA; add only reviews triggered by routing | Migration, auth/authz, external API, user-controlled input, cross-module change, unclear root cause, or more than 2 expected files |
| 🟢 **Quick** | Typo, comment, documentation-only correction, known-safe config value, or isolated hotfix with an obvious one-file fix | Executor with Quick Change Record → minimal QA | Migration, secrets, auth/authz, security surface, external API, user input, dependency, public API/contract, database query, unclear root cause, or more than 1 expected file |

**Quick Change Record** must state: target file, exact intended change, expected behavior, rollback method, and why the change is eligible for Quick mode. Executor stops and escalates to Standard or Full if the actual code contradicts that record.

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

### Conflicting findings

When two specialist reviews contradict each other (for example Security requires X while Performance requires Y):

1. Do not let the Executor pick a side on its own.
2. Record both findings in `status.md` with status `Open` and note the conflict explicitly.
3. STOP and present the trade-off to the human. The human arbitrates.
4. Record the decision and its rationale in `status.md`. Only then may the Executor proceed.

## Session Recovery

If your context was compacted, the session restarted, or you are picking up existing work:

1. Find the feature state: look for `.hitl-work/features/<feature-slug>/status.md`. If several features exist, continue the most recently updated one, or ask the user which one.
2. Read `status.md` in full. Trust it over your memory of this conversation.
3. Continue from the **Current Handoff** field. Do not re-run stages already marked complete in the Artifact Index.
4. If no `status.md` exists for the requested work, start the pipeline normally.

## Instructions

1. **Read the agent file before acting.** Never summarize from memory.
2. **Follow each agent's process exactly.** Boundaries are intentional.
3. **Respect the selected mode.** Full Pipeline requires Planner and QA; Standard requires Planner Lite and QA; Quick may skip Planner only with a recorded Quick Change Record and minimal QA. Don't skip QA to ship.
4. **HITL checkpoints:**
   - After Decomposer -> stop, human reviews task list.
   - After Planner -> optionally run Doubt Review.
   - After Executor -> optionally run Unit Test Writer (recommended for non-trivial logic).
   - After Unit Test Writer -> QA uses generated tests as baseline.
   - QA FAIL -> return to Executor.
5. **Specialist reviews report only** — findings go back to Executor to fix.
6. **Close the loop** with Docs + Skill Extractor after QA passes.

## Workflow

1. **Select mode** — Full, Standard, or Quick, and record the reason in `status.md`.
2. **Decompose** *(Full only, optional)* — `decomposer.md`. Output `task-N.md`. Stop for review.
3. **Plan** — Full: `planner.md` full spec. Standard: Planner Lite spec. Quick: Quick Change Record only.
4. **Doubt Review** *(required by routing; otherwise Full only when risk warrants it)* — `doubt-review.md`. Verdict: READY / BLOCKED / NEEDS CLARIFICATION.
5. **Execute** — `executor.md`. One step at a time. Stop and escalate if scope exceeds the selected mode.
6. **Unit Test Writer** *(required by routing; otherwise optional)* — `unit-test-writer.md`. Test Plan -> approval -> Test Code.
7. **QA** — Full/Standard: full QA. Quick: minimal QA. All modes require a clear PASS / FAIL / PASS WITH WARNINGS verdict and recorded evidence.
8. **Specialist Reviews** *(required by the routing table; otherwise as needed, parallel ok)* — findings by severity -> Executor -> re-verification.
9. **Docs & Skill Extraction** — Full when applicable; Standard/Quick only when the change establishes a reusable or user-facing behavior, after all blocking findings are closed.

## Rules

- Never let one agent do another's job.
- Always read codebase skill files before speccing.
- Every spec must include "What NOT to Touch" and "Breaking Changes".
- Executor stops and asks on ambiguity — never improvises.
- Unit Test Writer never skips Test Plan approval.
