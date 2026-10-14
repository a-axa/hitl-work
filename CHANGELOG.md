# Changelog

All notable changes to HITL·Work are documented here.

## [Unreleased]

## [1.1.0] - 2026-10-14

### Added
- Lean Code Discipline: ponytail-audited minimalism as native HITL·Work rules (minimality ladder in Planner, reuse-first minimal implementation in Executor, cut-list in QA Phase 5, `shortcut:` comments harvested into TECH-DEBT.md); applies to shipped code only, never to process artifacts
- Explicit user mode choice: the agent stops and asks the user to pick Full / Standard / Quick before any agent runs, validating the choice against eligibility rules
- Standardized agent file headers: YAML frontmatter (`name`, `description` with trigger guidance) and uniform Title Case headings across all 17 agent files, matching unit-test-writer.md
- Extended anti-slop to the Planner: new `### Anti-slop` hard-rules subsection in `planner.md` (no vague language, falsifiable acceptance criteria, final cut pass over `plan.md`); the combine step now covers Planner, QA, and Documentation
- New `RULES.md`: all detail rules (agent table, modes, routing, checkpoints, arbitration, recovery, lean values) live here; `SKILL.md` is now a pure index

### Changed
- `SKILL.md` trimmed from 13,858 to 995 characters (pipeline chain + anti-slop and mode STOP gates only)
- Renamed the Planner's output artifact from `prd.md` to `plan.md` across all skill files, README, and the workflow-state template (uppercase `PRD` still refers to the Decomposer's input requirements document)

## [1.0.0] - 2026-10-14

### Added
- 17-agent pipeline: (Decomposer) → Planner → (Doubt Review) → Executor → (Unit Test Writer) → QA → (Specialist Reviews) → Documentation / Skill Extractor
- Three workflow modes (Full Pipeline, Standard, Quick) with eligibility rules
- Required routing table mapping risk conditions to mandatory review stages
- Re-verification loop with finding IDs (`QA-001`, `SEC-001`, `PERF-001`) and recorded closure states (`Fixed`, `Accepted risk`, `Deferred`)
- Conflict arbitration rule: contradictory specialist findings are recorded as `Open` and decided by the human, never by the Executor alone
- Workflow state protocol: `.hitl-work/features/<slug>/status.md` as the cross-session source of truth
- Session recovery protocol: resume from the Current Handoff field after context compaction or restart
- Opt-in anti-slop companion skill: first-run detection gate with an explicit STOP, a four-answer offer (`yes` / `yes, always` / `no` / `never ask again`), preferences saved per project (`.hitl-work/preferences.md`) and globally (`~/.hitl-work/preferences.md`); QA and Documentation apply slop checks when the skill is available
- Generic companion-skill check hooks in QA Phase 5 and Documentation quality checks
- TECH-DEBT.md written or appended after every QA run
