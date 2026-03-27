---
title: Git Hooks
description: Automate kluster.ai code reviews with git hooks. Install pre-commit or pre-push hooks to catch issues before they reach your repository.
categories:
- CLI
url: https://docs.kluster.ai/code-reviews/cli/git-hooks/
word_count: 889
token_estimate: 1786
version_hash: sha256:52fc9c35b45a55127f269d75df5e34fe9824a454959728f8696f6b29d4b380b4
last_updated: '2026-03-27T17:26:06+00:00'
---

# Git hooks

Git hooks allow you to run [kluster.ai](https://www.kluster.ai/){target=\_blank} code reviews automatically every time you commit or push. Set up a pre-commit or pre-push hook and kluster-cli will review your changes in the background, blocking the operation if issues above your severity threshold are found.

## Hook types

| Hook | When it runs | What it reviews |
|------|-------------|-----------------|
| `pre-commit` | Before each `git commit` | Staged changes |
| `pre-push` | Before each `git push` | Commits being pushed |

**Which one should I use?**

- Use **pre-commit** for fast feedback on every commit. Best for individual workflows.
- Use **pre-push** to review the full set of changes before they leave your machine. Best for team workflows.
- Use **both** for maximum coverage.

## How hooks work

When a hook triggers, the CLI runs a review and checks the results against your severity threshold.

**If issues meet the threshold — the operation is blocked:**

<div data-termynal>
  <span data-ty  ="input"> git push origin feature-branch</span>
  <span data-ty>kluster.ai: Reviewing changes from a1b2c3d to e4f5f6a...</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439013</span>
  <span data-ty></span>
  <span data-ty>Found 1 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 HIGH [P1] security</span>
  <span data-ty>API key exposed in source code.</span>
  <span data-ty>at src/config.js:15</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Move the API key to environment variables and access via process.env.API_KEY</span>
  <span data-ty></span>
  <span data-ty></span>
  <span data-ty>kluster.ai: Push blocked due to code review issues (severity threshold: high).</span>
  <span data-ty>kluster.ai: Fix the issues above or use 'git push --no-verify' to skip.</span>
  <span data-ty>kluster.ai: View this review again: kluster show 507f1f77bcf86cd799439013</span>
</div>
**If no issues meet the threshold — the operation proceeds:**

<div data-termynal>
  <span data-ty  ="input"> git push origin feature-branch</span>
  <span data-ty>kluster.ai: Reviewing changes from a1b2c3d to e4f5a6b...</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>✓ Code review complete - no issues found!</span>
  <span data-ty></span>
  <span data-ty>Enumerating objects: 5, done.</span>
  <span data-ty>Counting objects: 100% (5/5), done.</span>
  <span data-ty>Writing objects: 100% (3/3), 340 bytes | 340.00 KiB/s, done.</span>
</div>
## Install hooks

Install a single hook:

```bash
kluster hooks install <hook_name>
```

<div data-termynal>
  <span data-ty  ="input"> kluster hooks install pre-push</span>
  <span data-ty>✓ pre-push hook installed successfully</span>
  <span data-ty>→ Hook location: .git/hooks/pre-push</span>
  <span data-ty>→ Mode: blocking on high severity and above</span>
</div>
Or install all hooks at once:

```bash
kluster hooks install all
```

<div data-termynal>
  <span data-ty  ="input"> kluster hooks install all</span>
  <span data-ty>✓ pre-commit hook installed successfully</span>
  <span data-ty>✓ pre-push hook installed successfully</span>
  <span data-ty>  Reviews will block on HIGH severity or above</span>
</div>
!!! info "Existing hooks"
    If a hook file already exists, the CLI will warn you. Use `--force` to overwrite it.

## Configure blocking severity

By default, hooks block on `high` severity or above. Use `--block-on` to change the threshold:

```bash
kluster hooks install pre-push --block-on critical
```

| Threshold | Blocks on |
|-----------|-----------|
| `critical` | Critical issues only |
| `high` (default) | High and critical issues |
| `medium` | Medium, high, and critical issues |
| `low` | Any issue blocks |

### Warn-only mode

To show review results without blocking, use `--warn-only`:

```bash
kluster hooks install pre-push --warn-only
```

In this mode, the review runs and displays any issues found, but the git operation always proceeds.

## Check hook status

See which hooks are installed:

```bash
kluster hooks status
```

<div data-termynal>
  <span data-ty  ="input"> kluster hooks status</span>
  <span data-ty>✓ pre-push: installed (kluster.ai)</span>
  <span data-ty>! pre-commit: not installed</span>
</div>
## Bypass hooks

In an emergency, you can skip hooks with git's `--no-verify` flag:

```bash
git commit --no-verify -m "hotfix: urgent production fix"
git push --no-verify
```

!!! note "Use sparingly"
    Bypassing hooks skips the code review entirely. Reserve this for urgent hotfixes and follow up with a manual review.

## Uninstall hooks

Remove hooks when no longer needed:

```bash
kluster hooks uninstall all
```

<div data-termynal>
  <span data-ty  ="input"> kluster hooks uninstall all</span>
  <span data-ty>✓ pre-push hook uninstalled successfully</span>
  <span data-ty>✓ pre-commit hook uninstalled successfully</span>
</div>
You can also uninstall a specific hook:

```bash
kluster hooks uninstall pre-commit
```

The CLI only removes hooks it installed (identified by the `KLUSTER_HOOK_START` marker). Other hooks are left untouched.

## Custom hook paths

The CLI respects git's `core.hooksPath` configuration. If you use a custom hooks directory:

```bash
git config core.hooksPath .githooks
kluster hooks install pre-push
# Hook is installed at .githooks/pre-push
```

If `core.hooksPath` is not set, hooks are installed in `.git/hooks/`.

## Next steps

- **[Review commands](/kluster-mkdocs/code-reviews/cli/review-commands/)**: Run reviews manually when you need them.
- **[Reference](/kluster-mkdocs/code-reviews/cli/reference/)**: Configuration, exit codes, and full command reference.
