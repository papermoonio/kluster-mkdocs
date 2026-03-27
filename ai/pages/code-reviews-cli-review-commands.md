---
title: Review Commands
description: Review staged changes, diffs, branches, and individual files with kluster-cli. Choose between instant and deep analysis modes.
categories:
- CLI
url: https://docs.kluster.ai/code-reviews/cli/review-commands/
word_count: 1532
token_estimate: 3686
version_hash: sha256:495f1bfee43e4ca879bdf2c6877734ae88122f1ac8b2933b68af65e9fa8dcb48
last_updated: '2026-03-27T17:26:06+00:00'
---

# Review commands

[kluster.ai](https://www.kluster.ai/){target=\_blank}'s CLI provides three ways to review code from the terminal — staged changes, diffs against branches or commits, and individual files — each suited to a different stage of your workflow. All commands support instant and deep analysis modes.

| Command | What it reviews | Requires git? |
|---------|----------------|:-------------:|
| `kluster review staged` | Staged changes (`git add`) | Yes |
| `kluster review diff <target>` | Diff against a branch or commit range | Yes |
| `kluster review file <path>` | One or more files | No |

## Review staged changes

Review everything you have staged before committing:

```bash
kluster review staged
```

<div data-termynal>
  <span data-ty  ="input"> kluster review staged</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439011</span>
  <span data-ty></span>
  <span data-ty>Found 2 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 CRITICAL [P0] security</span>
  <span data-ty>SQL injection vulnerability detected in user input handling. User-provided</span>
  <span data-ty>data is concatenated directly into SQL query without sanitization.</span>
  <span data-ty>at src/db/queries.go:45-52</span>
  <span data-ty></span>
  <span data-ty>More details</span>
  <span data-ty>  The function buildQuery() takes user input from the request body and</span>
  <span data-ty>  concatenates it directly into the SQL string.</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Use parameterized queries: db.Query("SELECT * FROM users</span>
  <span data-ty>  WHERE id = ?", userID)</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>#2 HIGH [P1] logical</span>
  <span data-ty>Potential null pointer dereference. The variable 'config' may be nil</span>
  <span data-ty>when accessed on line 78.</span>
  <span data-ty>at cmd/server.go:78</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Add a nil check before accessing config properties.</span>
</div>
!!! info "No staged changes?"
    If nothing is staged, the CLI will prompt you to `git add` files first.

## Review a diff

Compare your current work against a branch or between commits:

**Against a branch:**

```bash
kluster review diff main
```

<div data-termynal>
  <span data-ty  ="input"> kluster review diff main</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439016</span>
  <span data-ty></span>
  <span data-ty>Found 2 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 MEDIUM [P4] quality</span>
  <span data-ty>Function exceeds 200 lines without decomposition</span>
  <span data-ty>at src/handlers/upload.go:34-240</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>#2 LOW [P5] knowledge</span>
  <span data-ty>Error return value not checked on file close</span>
  <span data-ty>at src/handlers/upload.go:189</span>
</div>
**Between commits:**

```bash
kluster review diff HEAD~3..HEAD
```

<div data-termynal>
  <span data-ty  ="input"> kluster review diff HEAD~3..HEAD</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439017</span>
  <span data-ty></span>
  <span data-ty>✓ Code review complete - no issues found!</span>
</div>
Shell completions autocomplete branch names when available. See [Installation](/kluster-mkdocs/code-reviews/cli/installation/#shell-completions) to set this up.

## Review files

Review specific files without needing a git repository:

```bash
kluster review file src/auth.go src/middleware.go
```

<div data-termynal>
  <span data-ty  ="input"> kluster review file src/auth.go src/middleware.go</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439018</span>
  <span data-ty></span>
  <span data-ty>Found 1 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 CRITICAL [P2] security</span>
  <span data-ty>JWT token verification skips expiration check</span>
  <span data-ty>at src/auth.go:67-72</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Add token expiration validation before processing claims.</span>
</div>
This is useful for reviewing standalone scripts, config files, or code outside a git repository.

!!! tip "Exclude files with .klusterignore"
    If your repository contains folders you want to exclude from review (for example `dist/`, `vendor/`, or generated files), add them to a [`.klusterignore`](/kluster-mkdocs/code-reviews/configuration/klusterignore/) file. CLI review commands respect `.klusterignore`.

## Analysis modes

All review commands support two analysis modes via the `--mode` flag:

- **Instant**: Completes in about five seconds. Detects most issues and is suited for fast review and iteration cycles.
- **Deep**: Takes up to a few minutes. Conducts deeper analysis to uncover even subtle edge cases, ideal for critical code and final reviews.
Use the `--mode` flag to select:

```bash
kluster review staged --mode deep
```

<div data-termynal>
  <span data-ty  ="input"> kluster review staged --mode deep</span>
  <span data-ty>→ Reviewing code [████████████████████████████████████████] 100%</span>
  <span data-ty>✓ Reviewing code complete!</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439019</span>
  <span data-ty></span>
  <span data-ty>Found 2 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 HIGH [P1] logical</span>
  <span data-ty>Race condition in concurrent map access</span>
  <span data-ty>at src/cache/store.go:45-67</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>#2 MEDIUM [P2] performance</span>
  <span data-ty>N+1 query pattern in user listing endpoint</span>
  <span data-ty>at src/handlers/users.go:89-102</span>
</div>
The default mode is `instant`.

## CI/CD and scripting

For automation, prefer machine-readable output and check the command exit code.

Example (JSON output via environment variable):

```bash
KLUSTER_OUTPUT=json kluster review staged
```

See [CLI reference](/kluster-mkdocs/code-reviews/cli/reference/#exit-codes) for exit codes and [Output formats](/kluster-mkdocs/code-reviews/cli/reference/#output-formats) for configuration options.

## Review history

### List recent reviews

```bash
kluster log
```

<div data-termynal>
  <span data-ty  ="input"> kluster log</span>
  <span data-ty>→ Fetching review history...</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439011</span>
  <span data-ty>Date: 2026-02-09 14:32</span>
  <span data-ty>Issues: 2</span>
  <span data-ty>[CRITICAL] SQL injection vulnerability detected in user input handling...</span>
  <span data-ty>[HIGH] Potential null pointer dereference in config access...</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439010</span>
  <span data-ty>Date: 2026-02-09 11:15</span>
  <span data-ty>Issues: No issues</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439009</span>
  <span data-ty>Date: 2026-02-08 16:45</span>
  <span data-ty>Issues: 1</span>
  <span data-ty>[LOW] Consider adding error context to wrapped errors</span>
  <span data-ty></span>
  <span data-ty>Showing 3 of 47 reviews</span>
</div>
Use `--limit` to control how many reviews are shown (default: 20, max: 100):

```bash
kluster log --limit 5
```

### View review details

Use the review ID from `kluster log` to see the full report:

```bash
kluster show <review-id>
```

<div data-termynal>
  <span data-ty  ="input"> kluster show 507f1f77bcf86cd799439011</span>
  <span data-ty>→ Fetching review details...</span>
  <span data-ty></span>
  <span data-ty>Review: 507f1f77bcf86cd799439011</span>
  <span data-ty>Date: 2026-02-09 14:32:15</span>
  <span data-ty>Project: my-awesome-app</span>
  <span data-ty></span>
  <span data-ty>Found 2 issue(s)</span>
  <span data-ty></span>
  <span data-ty>#1 CRITICAL [P0] security</span>
  <span data-ty>SQL injection vulnerability detected in user input handling. User-provided</span>
  <span data-ty>data is concatenated directly into SQL query without sanitization.</span>
  <span data-ty>at src/db/queries.go:45-52</span>
  <span data-ty></span>
  <span data-ty>More details</span>
  <span data-ty>  The function buildQuery() takes user input from the request body and</span>
  <span data-ty>  concatenates it directly into the SQL string.</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Use parameterized queries: db.Query("SELECT * FROM users</span>
  <span data-ty>  WHERE id = ?", userID)</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>#2 HIGH [P1] logical</span>
  <span data-ty>Potential null pointer dereference. The variable 'config' may be nil</span>
  <span data-ty>when accessed on line 78.</span>
  <span data-ty>at cmd/server.go:78</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Add a nil check before accessing config properties.</span>
</div>
Long output is automatically paged using your system pager (`less`, `more`, or `most`).

## Next steps

- **[Git hooks](/kluster-mkdocs/code-reviews/cli/git-hooks/)**: Automate reviews on every commit or push.
- **[Repo reviews from CLI](/kluster-mkdocs/code-reviews/cli/repo-reviews/)**: Start and inspect full-repository reviews from terminal.
- **[Reference](/kluster-mkdocs/code-reviews/cli/reference/)**: Configuration, exit codes, and full command reference.
