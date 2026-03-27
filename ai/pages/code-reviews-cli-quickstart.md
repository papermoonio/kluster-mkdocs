---
title: CLI Quickstart
description: Learn how to install kluster-cli, authenticate with your API key, and review your first changes. No IDE or CI pipeline required.
categories:
- Basics
- CLI
url: https://docs.kluster.ai/code-reviews/cli/quickstart/
word_count: 765
token_estimate: 1680
version_hash: sha256:dc114a942aabf73ecbd3a10a6ea98bdc64d88004c0ba14c2547a6456ee651e0b
last_updated: '2026-03-27T17:26:06+00:00'
---

# Quickstart

Run [kluster.ai](https://www.kluster.ai/){target=\_blank} code reviews straight from your terminal. Install kluster-cli, authenticate with your API key, and review your first changes. No IDE or CI pipeline required.

## Prerequisites

You need:

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.
- **An API key**: Get your API key from the [CLI setup page](https://platform.kluster.ai/cli){target=\_blank}.

## 1. Install

=== "macOS / Linux / WSL"
    
    Run the following command in your terminal:


    ```bash
    curl -fsSL https://cli.kluster.ai/install.sh | sh
    ```

    <div data-termynal>
      <span data-ty  ="input"> curl -fsSL https://cli.kluster.ai/install.sh | sh</span>
      <span data-ty>Downloading kluster-cli...</span>
      <span data-ty>Installing to ~/.kluster/cli/bin/kluster...</span>
      <span data-ty>✅ kluster-cli installed successfully</span>
      <span data-ty>Run 'kluster login' to authenticate</span>
    </div>
=== "Windows PowerShell"
    
    Run the following command in PowerShell:

    ```powershell
    irm https://cli.kluster.ai/install.ps1 | iex
    ```

    <div data-termynal>
      <span data-ty="input-windows">irm https://cli.kluster.ai/install.ps1 | iex</span>
      <span data-ty>Downloading kluster-cli...</span>
      <span data-ty>Installing to %USERPROFILE%\.kluster\cli\bin\kluster.exe...</span>
      <span data-ty>✅ kluster-cli installed successfully</span>
      <span data-ty>Run 'kluster login' to authenticate</span>
    </div>
For installer options, supported platforms, and troubleshooting, see [Installation](/kluster-mkdocs/code-reviews/cli/installation/).

## 2. Login

Authenticate the CLI with your API key:

```bash
kluster login
```

<div data-termynal>
  <span data-ty  ="input"> kluster login</span>
  <span data-ty>Get your API key at: https://platform.kluster.ai/cli</span>
  <span data-ty>Enter your API key:</span>
  <span data-ty ="input"> ************************************</span>
  <span data-ty>→ Validating API key...</span>
  <span data-ty>✓ Successfully authenticated</span>
  <span data-ty></span>
  <span data-ty>Time to ship better code, try one of these:</span>
  <span data-ty>  kluster review staged             # Review staged changes</span>
  <span data-ty>  kluster hooks install pre-push   # Auto-review on git push/commit</span>
</div>
When prompted, paste the API key from [platform.kluster.ai/cli](https://platform.kluster.ai/cli){target=\_blank}.

## 3. Review your code

Stage some changes and run your first review:

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
That's it. kluster.ai analyzes your code and flags issues with severity levels, explanations, and suggested fixes.

Want a deeper scan? Re-run the same command with `--mode deep`.

The CLI can do more than review staged changes—you can also [review diffs against branches](/kluster-mkdocs/code-reviews/cli/review-commands/#review-a-diff), [review individual files](/kluster-mkdocs/code-reviews/cli/review-commands/#review-files), or set up [git hooks](/kluster-mkdocs/code-reviews/cli/git-hooks/) to automate reviews on every commit or push.

## Next steps

- **[Installation](/kluster-mkdocs/code-reviews/cli/installation/)**: Shell completions, update system, and advanced install options.
- **[Review commands](/kluster-mkdocs/code-reviews/cli/review-commands/)**: Review diffs, branches, and individual files.
- **[Git hooks](/kluster-mkdocs/code-reviews/cli/git-hooks/)**: Automate reviews on every commit or push.
- **[Reference](/kluster-mkdocs/code-reviews/cli/reference/)**: Configuration, exit codes, and full command reference.
