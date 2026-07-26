---
role: config
triggers: { phase: "*", type: "*", complexity: "*", valid: true }
layer: base
priority: 20
status: active
context_cost: low
overridable: true
override_strategy: extend
version: "1.0.0"
---

# Default Tool Conventions

## Version Control (Git)

- **Commit messages:** Conventional format — `<type>: <description>`. Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `ci`.
- **Commit frequency:** One logical change per commit. Commit after each green step in TDD.
- **Branch naming:** `feature/<name>`, `bugfix/<name>`, `refactor/<name>`, `hotfix/<name>`.
- **Never commit:** Secrets, API keys, tokens, passwords, build artifacts, generated files, IDE config, OS files (use `.gitignore`).
- **PR workflow:** All changes go through pull requests. No direct commits to main/master.
- **Squash merging:** Squash feature branches to a single commit on merge. Clean history > granular branch history.

## Linting & Formatting

- **Automated formatting:** Must be configured (Prettier, Black, ruff format, etc.). Run on save or pre-commit hook.
- **Automated linting:** Must be configured (ESLint, ruff, pylint, etc.). Lint errors block CI. Warnings addressed in the PR.
- **No unformatted code in commits.** The CI pipeline enforces this. Format before pushing.
- **No style debates.** Configure the tool once. The tool's output is the standard.

## Testing

- **Single command:** Tests must be runnable with one command: `npm test`, `pytest`, `cargo test`, `go test ./...`.
- **CI enforcement:** Full test suite runs on every PR. Failing tests block merge. No exceptions.
- **Test isolation:** Tests must be independent. No test should depend on another test's execution or side effects.
- **Fast feedback:** Unit tests should run in <10 seconds. Integration tests in <2 minutes. E2E tests in CI only.

## Package Management

- **Lockfiles committed:** `package-lock.json`, `yarn.lock`, `Pipfile.lock`, `Cargo.lock`, `go.sum`. Ensures reproducible builds.
- **Pinned versions:** Dependencies pinned to specific versions or narrow ranges. Automatically updated by Dependabot/Renovate.
- **Security vulnerabilities:** Treated as bugs. Critical vulns: fix within 24 hours. High: within the sprint. Medium/Low: next sprint.
- **Audit regularly:** `npm audit`, `pip-audit`, `cargo audit`. CI should run audit on every PR.

## Code Review

- **PR required:** No direct commits to protected branches. Every change goes through review.
- **Approval required:** At least one approval before merge. For critical changes: two approvals.
- **Review turnaround:** <24 hours for standard PRs, <4 hours for hotfixes.
- **PR size:** Target <400 lines. Split larger changes into reviewable chunks.
- **CI must be green.** No merging with failing checks.
