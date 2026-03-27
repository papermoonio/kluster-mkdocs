---
category: Configuration
includes_base_categories: true
base_categories:
- basics
- reference
word_count: 12467
token_estimate: 23658
page_count: 16
build_timestamp: '2026-03-27T17:27:40.236808+00:00'
version_hash: sha256:26bbcc36821b143f95fc45a6b4555199b03893869bdef254a973700e2700ebd6
---

# Begin New Bundle: Configuration
Includes shared base categories: basics, reference


---

Page Title: .klusterignore

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-configuration-klusterignore.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/configuration/klusterignore/
- Summary: Exclude files and folders from kluster.ai Code Reviews with a .gitignore-compatible .klusterignore file, using patterns, wildcards, and negation.
- Word Count: 435; Token Estimate: 801
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:848156888d765edd2ef1792d1c32c77f823b95f6f0c7d50305d7f9fa8c683bf4

# .klusterignore

Use a `.klusterignore` file to exclude files and folders from **kluster.ai Code Reviews**.

The syntax and matching behavior are intentionally the same as `.gitignore` (patterns, wildcards, negation rules, and comments).

!!! info "Already respects .gitignore"
    If your repository contains a `.gitignore`, kluster.ai automatically excludes anything ignored by git.
    Use `.klusterignore` to add review-specific exclusions (or to keep your review scope strict even when your `.gitignore` is minimal).

## Supported workflows

`.klusterignore` is currently available on:

| Tool | Workflow | Reference |
|---|---|---|
| IDE | On-demand reviews (human-written code) | [On-demand reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/) |
| IDE | Automatic reviews (human-written code) | [Automatic reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/automatic-reviews/) |
| CLI | kluster.ai CLI | [Review commands](/kluster-mkdocs/code-reviews/cli/review-commands/) |

!!! note "Not yet supported"
    `.klusterignore` is currently **not** applied to AI assistant-triggered automatic reviews (the "AI-generated code" automatic review flow) or AI agent reviews (for example, reviews triggered by an AI assistant tool call).

## Quickstart

1. Create a file named `.klusterignore` in the **root of your repository**.
2. Add ignore patterns for paths you never want to send for review.

Example:

```gitignore
# Dependencies
node_modules/
vendor/

# Build output
dist/
build/

# Local config and secrets
.env
*.pem

# Logs
*.log

# Re-include one file
!.gitkeep
```

## Syntax

Most teams can copy patterns directly from their `.gitignore`.

Common rules:

- Blank lines are ignored.
- Lines starting with `#` are comments.
- `*`, `?`, and `[]` work as wildcards.
- `**` can match across directory boundaries.
- A trailing `/` matches directories.
- A leading `/` anchors the pattern to the repository root.
- Prefix a pattern with `!` to re-include paths previously excluded.
- If multiple patterns match a path, the **last matching rule wins** (same as `.gitignore`).

## How it affects reviews

When a file matches `.klusterignore`, it is excluded from the review input:

- Excluded files are not reviewed, even if they are staged or part of a diff.
- Excluding a directory excludes everything under it (unless you re-include specific files with `!`).

## Next steps

- **[On-demand reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)**: Run manual reviews in your IDE and verify changes on your terms.
- **[Automatic reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/automatic-reviews/)**: Enable automatic reviews that trigger after you stop typing.
- **[Review commands (CLI)](/kluster-mkdocs/code-reviews/cli/review-commands/)**: Review staged changes, diffs, or specific files from the terminal.

## Troubleshooting

- If something is still being reviewed, double-check that your pattern matches the path **relative to the repository root**.
- If you use negation (`!`), ensure the re-include pattern appears **after** the exclude rule.


---

Page Title: Automatic reviews for AI-generated code

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-ide-reviews-ai-generated-code-automatic-reviews.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/
- Summary: Set up automatic code reviews and dependency checks for AI-generated code. Reviews run in real-time as your AI writes code.
- Word Count: 772; Token Estimate: 1434
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:b34ae3d8c947e3933699b72280dcc6ab524e08a6210581c8293119e600b4a509

# Automatic reviews

Learn how to use [kluster.ai](https://www.kluster.ai/){target=\_blank} with your preferred AI assistant to catch bugs, security flaws, and logic errors instantly—as your AI writes code.

!!! note ".klusterignore is not applied in this flow (yet)"
    Automatic reviews triggered by AI assistants currently do **not** use [`.klusterignore`](/kluster-mkdocs/code-reviews/configuration/klusterignore/) to exclude files.

## Prerequisites

Before getting started, ensure you have:

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.
- **kluster.ai installed in your IDE**: Follow the [Installation guide](/kluster-mkdocs/code-reviews/get-started/installation/) to set it up in your favourite IDE.
## How automatic reviews work

<div class="embed-container">
    <iframe
        src="https://www.youtube.com/embed/-V0VsqgTza8"
        title="Instant Code Reviews with kluster.ai"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
        loading="lazy">
    </iframe>
</div>

The most powerful way to use Code Reviews is to let it work in the background. You don't need to change how you work—just ask your AI assistant for what you need.

1.  **You prompt**: Ask your AI assistant to generate code (e.g., "Create a user login endpoint").
2.  **AI generates**: The AI writes the code.
3.  **kluster.ai verifies**: Code Reviews automatically analyzes the diff in real-time.


In this example, the AI creates an API endpoint but makes a critical security error that kluster.ai intervenes to fix.

=== "VS Code"

    In VS Code, you'll see the review appear directly in the chat. kluster.ai flags the issue (e.g., "Unprotected API Endpoint") and provides a fix.

    ![VS Code Auto Review - Unprotected API](/kluster-mkdocs/images/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/vscode-auto-review.webp)

=== "Claude Code"

    In the terminal, Claude Code displays the review results immediately.

    ![Claude Code Auto Review - Unprotected API](/kluster-mkdocs/images/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/claude-auto-review.webp)

## Compatible with

<div class="grid cards" markdown>

-   :simple-cursor: **Cursor**

    ---

    AI-native code editor with built-in kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Cursor](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :material-microsoft-visual-studio-code: **VS Code**

    ---

    Lightweight editor with kluster.ai extension and Copilot integration.

    [:octicons-arrow-right-24: Install for VS Code](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-windsurf: **Windsurf**

    ---

    AI-powered IDE by Codeium with kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Windsurf](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :antigravity-antigravity: **Antigravity**

    ---

    Next-generation IDE with native MCP integration for kluster.ai.

    [:octicons-arrow-right-24: Install for Antigravity](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-anthropic: **Claude Code**

    ---

    Anthropic's CLI tool with automatic kluster.ai reviews via MCP.

    [:octicons-arrow-right-24: Install for Claude Code](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :octicons-terminal-24: **Codex CLI**

    ---

    OpenAI's CLI agent with kluster.ai integration via MCP.

    [:octicons-arrow-right-24: Install for Codex CLI](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-jetbrains: **JetBrains**

    ---

    JetBrains IDEs (IntelliJ IDEA, WebStorm, and others) with kluster.ai plugin support.

    [:octicons-arrow-right-24: Install for JetBrains](/kluster-mkdocs/code-reviews/get-started/installation/)

</div>

## Configuration

You can customize how automatic reviews work in your [configuration options](/kluster-mkdocs/code-reviews/configuration/options/):

- **Enabled tools**: Toggle Code Review and Dependency Analysis on/off.
- **Sensitivity**: Adjust how strictly issues are flagged (Low → Critical).
- **Bug check types**: Select which issue types to check (Security, Logic, Performance, etc.).

## Dependency checks

Code Reviews protects you when starting new projects or adding libraries by validating dependencies before installation.

!!! note ".klusterignore is not applied in this flow (yet)"
    Automatic dependency checks triggered by AI assistants currently do **not** use [`.klusterignore`](/kluster-mkdocs/code-reviews/configuration/klusterignore/) to exclude files.

### How dependency checks work

1.  **You prompt**: Ask your AI to start a project (e.g., "Scaffold a Next.js app with Auth.js").
2.  **AI suggests**: The AI lists the necessary dependencies.
3.  **kluster.ai verifies**: The `kluster_dependency_check` tool checks every package for security vulnerabilities and license compliance before you install them.


When the AI suggests a package version with a known vulnerability, kluster.ai alerts you immediately, preventing the risk from entering your codebase.

![Dependency Analysis Example](/kluster-mkdocs/images/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/dependency-analysis.webp)

## Next steps

- **[On-demand reviews](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/on-demand-reviews/)**: Review existing code on demand.
- **[Configuration](/kluster-mkdocs/code-reviews/configuration/options/)**: Customize dependency check behavior.


---

Page Title: Automatic reviews for human-written code

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-ide-reviews-human-written-code-automatic-reviews.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/ide-reviews/human-written-code/automatic-reviews/
- Summary: Enable automatic reviews to scan uncommitted changes after you stop typing. Learn how kluster.ai detects idle time and surfaces results.
- Word Count: 570; Token Estimate: 1019
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:b9dc7d8c2f5f396b99a433ed38f59a577ab6648e924d632e7556e6d718ee79de

# Automatic reviews

Automatic reviews watch your uncommitted changes and run in the background. You do not need to click anything.

!!! tip "Exclude files with .klusterignore"
    Add a [`.klusterignore`](/kluster-mkdocs/code-reviews/configuration/klusterignore/) file to exclude files and folders from automatic reviews (syntax is the same as `.gitignore`).

## Prerequisites

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.
- **kluster.ai installed in your IDE**: Follow the [Installation guide](/kluster-mkdocs/code-reviews/get-started/installation/) to set it up in your favourite IDE.
## Turn it on

1.  Open [Options](/kluster-mkdocs/code-reviews/configuration/options/) in the kluster.ai platform or IDE.
2.  In **Enabled Tools**, toggle **Ambient Background Reviews (Beta, Enterprise plan)** on.
3.  Keep coding. Reviews run automatically once enabled.

!!! note
    Automatic reviews appear as **Ambient Background Reviews** in the platform UI.

![Background reviews enabled in Options](/kluster-mkdocs/images/code-reviews/ide-reviews/human-written-code/background-reviews/background-reviews.webp)

## How it works

Automatic reviews run in the background while you code. The extension periodically checks your diff and resets an idle timer each time it changes. When the timer runs out, [kluster.ai](https://www.kluster.ai/){target=\_blank} scans your uncommitted changes and notifies you only if it finds issues.

## What gets reviewed

Automatic reviews include staged, unstaged, untracked, and unsaved editor changes—basically everything that would show up in `git status` plus your current unsaved work.

Only text files are reviewed. Binary files and common generated files (like `node_modules` or build outputs) are filtered out automatically.

!!! note "Large changesets"
    If your changes are very large, the review may skip context or fail. Use [on-demand reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/) to review smaller chunks instead.

## Where results appear

Results show up in three places:

- **Inline comments**: Collapsed by default, expand to see details.
- **Gutter icons**: Visual markers next to flagged lines.
- **Problems panel**: All issues listed in one place.

Automatic review results are appended to any existing on-demand review results—they don't replace them.

## Branch switching

When you switch git branches, kluster.ai resets its tracking state. This prevents stale results from a previous branch showing up in your current work.

## Compatible with

<div class="grid cards" markdown>

-   :simple-cursor: **Cursor**

    ---

    AI-native code editor with built-in kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Cursor](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :material-microsoft-visual-studio-code: **VS Code**

    ---

    Lightweight editor with kluster.ai extension and Copilot integration.

    [:octicons-arrow-right-24: Install for VS Code](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-windsurf: **Windsurf**

    ---

    AI-powered IDE by Codeium with kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Windsurf](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :antigravity-antigravity: **Antigravity**

    ---

    Next-generation IDE with native MCP integration for kluster.ai.

    [:octicons-arrow-right-24: Install for Antigravity](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-jetbrains: **JetBrains**

    ---

    JetBrains IDEs (IntelliJ IDEA, WebStorm, and others) with kluster.ai plugin support.

    [:octicons-arrow-right-24: Install for JetBrains](/kluster-mkdocs/code-reviews/get-started/installation/)

</div>

## Next steps

- **[On-demand reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)**: Run reviews manually in your editor.
- **[Configuration options](/kluster-mkdocs/code-reviews/configuration/options/)**: Adjust sensitivity and issue types.


---

Page Title: CLI Installation

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-cli-installation.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/cli/installation/
- Summary: Install kluster-cli on macOS, Linux, or Windows. Set up shell completions, configure your PATH, and keep the CLI up to date.
- Word Count: 828; Token Estimate: 1827
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:d1215f98100645a5d44434afdff2b1b0d8c042402d5ca72e79c8b9c04ce279ce

# Installation

[kluster.ai](https://www.kluster.ai/){target=\_blank}'s CLI is available for macOS, Linux, and Windows. The installer downloads a single binary, adds it to your `PATH`, and you're ready to go. This page covers installation, updates, shell completions, and uninstalling.

## Install kluster-cli

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
    The installer places the binary at `~/.kluster/cli/bin/kluster` and adds it to your `PATH`.

    **Installer options**:

    | Flag | Description |
    |------|-------------|
    | `-b <dir>` | Custom install directory (default: `~/.kluster/cli/bin`). |
    | `-d` | Enable debug logging. |
    | `-q` | Quiet mode (errors only). |
    | `-n` | Dry run (no changes). |

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
    The installer places the binary at `%USERPROFILE%\.kluster\cli\bin\kluster.exe` and adds it to your `PATH`.

### Verify installation

After installation, verify the CLI is working:

```bash
kluster version
```

<div data-termynal>
  <span data-ty  ="input"> kluster version</span>
  <span data-ty>kluster.ai CLI version 0.1.2</span>
  <span data-ty>  commit: a1b2c3d4e5f6a7b8</span>
  <span data-ty>  built:  2026-02-01T10:30:00Z</span>
  <span data-ty>  go:     go1.24.0</span>
  <span data-ty>  os/arch: darwin/arm64</span>
</div>
If you get `command not found: kluster`, your `PATH` likely wasn't updated. See [Troubleshooting](/kluster-mkdocs/code-reviews/troubleshooting/#command-not-found-kluster).

### Login

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
Get your API key from the [CLI setup page](https://platform.kluster.ai/cli){target=\_blank}.

To authenticate non-interactively (useful for CI/CD):

```bash
kluster login --api-key kl_your_key_here
```

To remove stored credentials:

```bash
kluster logout
```

## Supported platforms

| OS | Architectures |
|----|---------------|
| Linux | amd64, arm64 |
| macOS | amd64 (Intel), arm64 (Apple Silicon) |
| Windows | amd64, arm64 |

## Update

The CLI can update itself to the latest version:

```bash
kluster update
```

<div data-termynal>
  <span data-ty  ="input"> kluster update</span>
  <span data-ty>→ Checking for updates...</span>
  <span data-ty>Current version: v0.1.0</span>
  <span data-ty>Latest version:  v0.1.2</span>
  <span data-ty>→ Updating to v0.1.2...</span>
  <span data-ty>→ Downloading...</span>
  <span data-ty>→ Checksum verified</span>
  <span data-ty>✓ Successfully updated to v0.1.2</span>
</div>
To check if an update is available without installing:

```bash
kluster update --check
```

<div data-termynal>
  <span data-ty  ="input"> kluster update --check</span>
  <span data-ty>→ Checking for updates...</span>
  <span data-ty>✓ Already up to date (v0.1.2)</span>
</div>
The update process downloads the latest binary, verifies its SHA256 checksum, and replaces the current installation.

## Uninstall

To remove kluster-cli, delete the installation directory:

=== "macOS / Linux / WSL"

    ```bash
    rm -rf ~/.kluster/cli
    ```

=== "Windows PowerShell"

    ```powershell
    Remove-Item -Recurse -Force "$env:USERPROFILE\.kluster\cli"
    ```

## Shell completions (optional) { #shell-completions }

Enable tab completion for commands, flags, and git branches.

=== "Bash"

    ```bash
    # Current session only
    source <(kluster completion bash)

    # Permanent (Linux, requires sudo)
    kluster completion bash | sudo tee /etc/bash_completion.d/kluster > /dev/null

    # Permanent (macOS with Homebrew)
    kluster completion bash > "$(brew --prefix)/etc/bash_completion.d/kluster"
    ```

=== "Zsh"

    ```zsh
    # Enable completions if not already
    echo "autoload -U compinit; compinit" >> ~/.zshrc

    # Add completion
    kluster completion zsh > "${fpath[1]}/_kluster"

    # Or source directly
    echo 'source <(kluster completion zsh)' >> ~/.zshrc
    ```

=== "Fish"

    ```fish
    # Current session only
    kluster completion fish | source

    # Permanent
    kluster completion fish > ~/.config/fish/completions/kluster.fish
    ```

=== "PowerShell"

    ```powershell
    # Current session only
    kluster completion powershell | Out-String | Invoke-Expression

    # Permanent (add to profile)
    kluster completion powershell >> $PROFILE
    ```

## Next steps

- **[Quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/)**: Run your first review from the terminal.
- **[Review commands](/kluster-mkdocs/code-reviews/cli/review-commands/)**: All review options and output formats.
- **[Reference](/kluster-mkdocs/code-reviews/cli/reference/)**: Configuration, exit codes, and full command reference.


---

Page Title: CLI Quickstart

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-cli-quickstart.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/cli/quickstart/
- Summary: Learn how to install kluster-cli, authenticate with your API key, and review your first changes. No IDE or CI pipeline required.
- Word Count: 765; Token Estimate: 1680
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:dc114a942aabf73ecbd3a10a6ea98bdc64d88004c0ba14c2547a6456ee651e0b

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


---

Page Title: CLI Reference

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-cli-reference.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/cli/reference/
- Summary: Reference for kluster.ai CLI commands, configuration options, and exit codes, with quick lookups for flags, config settings, and environment variables.
- Word Count: 700; Token Estimate: 1700
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:54874100972c7a85a1888c47278ece23a62169dbff730402f23fe6d8e148e0bc

# CLI reference

Complete reference for all [kluster.ai](https://www.kluster.ai/){target=\_blank}'s CLI commands, configuration options, and exit codes. Use this page for quick lookups on commands, flags, config file settings, and environment variables.

## Commands

Tip: Use `--help` on any command to see available flags:

```bash
kluster --help
kluster review staged --help
```

=== "Review"

    | Command | Description |
    |---------|-------------|
    | `kluster review staged` | Review staged changes |
    | `kluster review staged --mode deep` | Deep analysis mode |
    | `kluster review diff <target>` | Review diff against branch or commit range |
    | `kluster review file <path> [paths...]` | Review one or more files |

=== "History"

    | Command | Description |
    |---------|-------------|
    | `kluster log` | List recent reviews (default: 20) |
    | `kluster log --limit <n>` | Limit results (max: 100) |
    | `kluster show <review-id>` | View full review details |

=== "Hooks"

    | Command | Description |
    |---------|-------------|
    | `kluster hooks install <hook>` | Install a hook (`pre-commit`, `pre-push`, `all`) |
    | `kluster hooks install <hook> --block-on <level>` | Set blocking severity (`critical`, `high`, `medium`, `low`) |
    | `kluster hooks install <hook> --warn-only` | Show issues without blocking |
    | `kluster hooks uninstall <hook>` | Remove a hook |
    | `kluster hooks status` | Show installed hooks |

=== "Auth"

    | Command | Description |
    |---------|-------------|
    | `kluster login` | Authenticate with API key |
    | `kluster login --api-key <key>` | Authenticate non-interactively |
    | `kluster logout` | Remove stored credentials |

=== "Utility"

    | Command | Description |
    |---------|-------------|
    | `kluster version` | Print version info |
    | `kluster update` | Update to latest version |
    | `kluster update --check` | Check for updates without installing |
    | `kluster completion <shell>` | Generate shell completions (`bash`, `zsh`, `fish`, `powershell`) |

## Configuration

kluster-cli uses a YAML config file with optional environment variable overrides.

### Config file

The config file is created automatically on first use:

| OS | Location |
|----|----------|
| macOS / Linux | `~/.kluster/cli/config.yaml` |
| Windows | `%USERPROFILE%\.kluster\cli\config.yaml` |

**Available settings:**

| Key | Default | Description |
|-----|---------|-------------|
| `api_key` | — | Your kluster.ai API key (set by `kluster login`) |
| `api_url` | `https://api.kluster.ai` | API endpoint |
| `output` | `table` | Default output format |

Example config file:

```yaml
api_key: kl_your_api_key_here
api_url: https://api.kluster.ai
output: table
```

### Environment variables

Environment variables override config file values. All variables use the `KLUSTER_` prefix:

| Variable | Overrides | Example |
|----------|-----------|---------|
| `KLUSTER_API_KEY` | `api_key` | `export KLUSTER_API_KEY=kl_abc123` |
| `KLUSTER_API_URL` | `api_url` | `export KLUSTER_API_URL=https://custom.endpoint` |
| `KLUSTER_OUTPUT` | `output` | `export KLUSTER_OUTPUT=json` |

This is useful for CI/CD pipelines where you don't want to store a config file:

```bash
KLUSTER_API_KEY=kl_abc123 kluster review staged
```

### Output formats

The CLI supports three output formats, configurable globally or per command:

=== "Table (default)"

    Human-readable format with colors and borders. Best for interactive use.

    ```bash
    kluster log --output table
    ```

=== "JSON"

    Machine-readable format. Best for scripts and CI/CD integration.

    ```bash
    kluster log --output json
    ```

    Review commands support the same output formats:

    ```bash
    kluster review staged --output json
    ```

=== "Text"

    Simple pipe-separated format. Easy to parse with standard Unix tools.

    ```bash
    kluster log --output text
    ```

Set the default format globally:

```yaml
# ~/.kluster/cli/config.yaml
output: json
```

Or override per command with the `--output` flag:

```bash
kluster log --output json
```

### Configuration priority

When the same setting is defined in multiple places, the CLI uses this order (highest priority first):

1. **Command-line flags** — `--output json`
2. **Environment variables** — `KLUSTER_OUTPUT=json`
3. **Config file** — `output: json` in `config.yaml`
4. **Built-in defaults** — `table`

## Authentication

Your API key is stored in the config file and managed through the `login` and `logout` commands:

```bash
# Save your API key
kluster login

# Remove your API key
kluster logout
```

Get your API key from the [CLI setup page](https://platform.kluster.ai/cli){target=\_blank}.

You can also provide the API key directly without the interactive prompt:

```bash
kluster login --api-key kl_your_key_here
```

## Exit codes

### Review commands

| Code | Meaning |
|:----:|---------|
| `0` | No issues found |
| `1` | Low severity issues found |
| `2` | Medium severity issues found |
| `3` | High severity issues found |
| `4` | Critical severity issues found |

The exit code reflects the **highest** severity issue found. This makes it easy to use in scripts:

```bash
kluster review staged
if [ $? -ge 3 ]; then
  echo "High or critical issues found"
fi
```

### Git hooks

| Code | Meaning |
|:----:|---------|
| `0` | Allow the git operation |
| `1` | Block the git operation |

### General errors

| Code | Meaning |
|:----:|---------|
| `1` | Command error (authentication failure, invalid arguments, etc.) |

## Next steps

- **[Quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/)**: Get started with your first review.
- **[Review commands](/kluster-mkdocs/code-reviews/cli/review-commands/)**: Detailed usage and examples.
- **[Git hooks](/kluster-mkdocs/code-reviews/cli/git-hooks/)**: Automate reviews in your workflow.


---

Page Title: Code Reviews - Modes, Features, and Setup

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-review-modes.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/review-modes/
- Summary: Learn how to use kluster.ai's Code Reviews to validate your code in real time—detecting bugs, security issues, and quality problems so you can ship safely.
- Word Count: 914; Token Estimate: 1567
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:1da456c091e0fda3fafabee409ce4adf5114adbbaaa34b39d51973382fb5960d

# Code Reviews

Code Reviews analyzes your code for bugs, security vulnerabilities, and quality issues. It works for **human-written code**, **AI-generated code**, **repo reviews**, and the **standalone CLI**, with review modes tailored to each workflow.

For in-editor reviews, the service integrates directly into your IDE or CLI (Cursor, VS Code, Windsurf, JetBrains, Claude Code, and others), analyzing code as you work. For terminal-based workflows, the standalone CLI provides reviews directly from the command line. For system-wide analysis, repo reviews scan your entire repository via the web dashboard or `kluster-cli`.

<div class="embed-container">
    <iframe
        src="https://www.youtube.com/embed/KLZlNpYbD4g"
        title="Code review modes with kluster.ai"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
        loading="lazy">
    </iframe>
</div>

## Key features

- **Flexible review modes**: Reviews for human-written code, AI-generated code, and system-wide repo analysis.
- **Comprehensive issue detection**: Analyzes 7 issue types — *Semantic, Intent, Logical, Security, Knowledge, Performance,* and *Quality*.
- **Customizable sensitivity**: Configure detection sensitivity from *Low* to *Critical*.
- **Dual analysis tools**: Real-time Code Review and Dependency Analysis for complete coverage.
- **Instant fixes**: Apply suggested fixes with one click, or let your AI assistant handle them automatically.

## Human-written code

**For direct, in-editor reviews without AI.**

Review code you write yourself with on-demand reviews—no AI assistant needed. Available features include:

- **Code block review**: Review selected code snippets.
- **Current file review**: Analyze the file you're working on.
- **Uncommitted changes review**: Check all modified files before committing.

**Compatible with**: Cursor, VS Code, Windsurf, Antigravity, JetBrains (IDEs only)

[:octicons-arrow-right-24: Get started with human-written code reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)

## AI-generated code

**For AI-assisted coding workflows.**

When your AI coding assistant generates or modifies code, kluster.ai automatically reviews it in real-time. You can also ask your AI to review existing files on demand.

**AI-generated code reviews also verify *intent*—ensuring your AI actually did what you asked**, not just that the code works. This context-aware check is only possible when kluster.ai sees your original prompt.

- **Automatic reviews**: Triggered automatically when AI generates code.
- **On-demand reviews**: Triggered when you ask your AI to review existing code.

**Compatible with**: Cursor, VS Code, Windsurf, Antigravity, JetBrains (IDEs) and Claude Code, Codex CLI (CLIs)

[:octicons-arrow-right-24: Get started with AI-generated code reviews](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)

## Repo reviews

**For system-wide codebase analysis.**

Repo reviews analyze your entire repository as a system, uncovering bugs and risks that don't belong to any single change or PR. These issues only emerge when multiple parts of the code interact—problems that survive individual code reviews because they're invisible in isolation.

Common issues found by repo reviews include:

- **Cross-module bugs**: Code paths that look safe in isolation but break when exercised together.
- **Silent error propagation**: Errors that propagate silently across modules and only surface in production.
- **State inconsistencies**: State that becomes inconsistent under retries, partial failures, or restarts.
- **Bypassed validation**: Security or validation checks applied in one place but bypassed in another.
- **Assumption violations**: Logic that relies on assumptions enforced elsewhere in the codebase.

Repo reviews complement PR-level reviews by revealing problems that already exist in your system—issues that would remain hidden until something breaks.

**Available on**: Web dashboard and kluster-cli (requires GitHub, GitLab, or Bitbucket connection)

[:octicons-arrow-right-24: Get started with repo reviews](/kluster-mkdocs/code-reviews/repo-reviews/quickstart/)

## CLI

**For command-line workflows and automation.**

Review code directly from the terminal without an IDE or AI assistant. The kluster-cli tool provides full review functionality with git integration, automated hooks, and machine-readable output formats.

- **On-demand reviews**: Review staged changes, diffs against branches, or individual files.
- **Git hook automation**: Install pre-commit or pre-push hooks to catch issues automatically.
- **Scriptable output**: JSON and text output formats for CI/CD integration.

**Available on**: macOS, Linux, Windows

[:octicons-arrow-right-24: Get started with CLI](/kluster-mkdocs/code-reviews/cli/quickstart/)

## External knowledge

**For context-aware reviews using your project management tools.**

External Knowledge connects kluster to external sources like Jira, so code reviews can verify your implementation against real ticket requirements and specifications. Instead of reviewing code in isolation, kluster uses the context from your connected tools to make its analysis more accurate.

**Available integrations**: Jira

[:octicons-arrow-right-24: Set up External Knowledge](/kluster-mkdocs/code-reviews/external-knowledge/quickstart/)

!!! tip "Need help choosing?"
    See [Pick your workflow](/kluster-mkdocs/code-reviews/get-started/pick-your-workflow/) for a detailed comparison and decision guide.



## Next steps

- **[Installation](/kluster-mkdocs/code-reviews/get-started/installation/)**: Install kluster.ai in your IDE or CLI tool.
- **[Human-written code](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)**: Get started with in-editor reviews.
- **[AI-generated code](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)**: Set up automatic and on-demand reviews.
- **[Repo reviews](/kluster-mkdocs/code-reviews/repo-reviews/quickstart/)**: Analyze your entire codebase for system-wide issues.
- **[CLI](/kluster-mkdocs/code-reviews/cli/quickstart/)**: Review code from the terminal with the standalone CLI.
- **[External Knowledge](/kluster-mkdocs/code-reviews/external-knowledge/quickstart/)**: Connect kluster to Jira for context-aware reviews.
- **[Pick your workflow](/kluster-mkdocs/code-reviews/get-started/pick-your-workflow/)**: Compare modes and find the right fit.


---

Page Title: Custom rules

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-configuration-rules.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/configuration/rules/
- Summary: Learn how to define and manage custom code review rules to enforce consistent code quality, using manual rules or learned rules from GitHub repositories.
- Word Count: 315; Token Estimate: 523
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:f56e57a5b2d9e4623bc255dfba5ec223f75af882e367b9bd4639473f40490b17

# Custom rules

Rules define the standards and requirements that help maintain consistent code quality across your projects. They give Code Reviews a clear basis for evaluating new code, ensuring it aligns with your defined criteria. [kluster.ai](https://www.kluster.ai/){target=\_blank} Code Reviews automatically check code changes against these rules.

## Rule types

To accommodate different workflows, Code Reviews supports two types of rules:

- **Manual rules**: Custom rules you create based on specific team requirements and coding standards.
- **Learned rules**: Automatically extracted from your GitHub repositories, continuously updated to reflect your codebase patterns.

## Set up instructions


!!! info "Extraction rate limit"
    Rule extraction from repositories is limited to once per hour. Wait 60 minutes between extraction requests.

1. Access the platform by navigating to [**Custom Code Review Rules**](https://platform.kluster.ai/custom-code-review-rules){target=\_blank}.

2. (Optional) Connect your GitHub account to enable project-specific rules. In this context, each GitHub repository is treated as a 'project' - Code Reviews learns patterns from each repository and applies those specific rules when reviewing code for that project.

    ![Connect to GitHub](/kluster-mkdocs/images/code-reviews/configuration/rules/rules-01.webp)

3. Click **Add review rule** to create custom rules.

    ![Add review rule button](/kluster-mkdocs/images/code-reviews/configuration/rules/rules-02.webp)

4. Configure rule scope and select one of the following:
    - **All**: Rules apply globally to all your coding sessions.
    - **Project-specific**: Select a repository from the dropdown (requires GitHub connection).

5. Click **Save & Add Another** to add multiple rules or **Save** to finish.

    ![Add code review rule dialog](/kluster-mkdocs/images/code-reviews/configuration/rules/rules-03.webp)

## Next steps

- **[Installation guide](/kluster-mkdocs/code-reviews/get-started/installation/)**: Set up Code Reviews in your preferred IDE.
- **[See real examples](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/examples/cursor-firebase-nextjs/)**: Walk through a complete Firebase migration case study.


---

Page Title: External Knowledge Quickstart for Reviews

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-external-knowledge-quickstart.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/external-knowledge/quickstart/
- Summary: Connect external sources like Jira to kluster.ai so code reviews can verify your code against real project requirements and specifications.
- Word Count: 256; Token Estimate: 434
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:5e9570ff968109bd59e0c552058e97043cd202c20ded840a2e2c21dd35113b2d

# Quickstart

External Knowledge lets [kluster.ai](https://www.kluster.ai/){target=\_blank} Code Reviews pull context from the tools your team already uses. Instead of reviewing code in isolation, kluster uses requirements, specifications, and ticket details from connected sources to make its analysis more accurate and actionable.

## Connecting to external tools

1. **Connect an integration**: Go to the [External Knowledge](https://platform.kluster.ai/external-knowledge){target=\_blank} page on the kluster.ai platform and connect your tool. [Jira](/kluster-mkdocs/code-reviews/external-knowledge/jira/) is the available integration.

2. **Make sure the ticket ID is reachable by kluster**: How you do this depends on your tool:

    | Tool | What to do |
    |------|------------|
    | Cursor, VS Code, Windsurf, JetBrains, Antigravity | Check out a branch with the ticket ID in the name (e.g., `feat/KAN-2`) — kluster detects it automatically. |
    | Claude Code, Codex CLI | Include the ticket ID in your prompt (e.g., "...Ticket KAN-2"). |

3. **Ask your AI assistant to write code as usual**: kluster automatically includes the ticket requirements in the review and flags any gaps between the specification and the generated code.

!!! tip
    If your branch is named something generic like `main` and you do not reference a ticket in your prompt, kluster will not include any External Knowledge context. Always reference the ticket when it matters.

## Available integrations

<div class="grid cards" markdown>

-   :simple-jira: **Jira**

    ---

    Pull ticket requirements into code reviews to verify your implementation matches specifications.

    [:octicons-arrow-right-24: Set up Jira](/kluster-mkdocs/code-reviews/external-knowledge/jira/)

</div>


---

Page Title: Install kluster.ai Code Reviews for Your IDE or CLI

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-get-started-installation.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/get-started/installation/
- Summary: Set up kluster.ai Code Reviews in minutes. Scan code for errors, vulnerabilities, and performance issues in Cursor, VS Code, JetBrains, and more.
- Word Count: 2544; Token Estimate: 5006
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:0cd4c26fe0e2037f3f8f0de4ace3127191b7785252371fa545ac22cc7389db61

# Get started with Code Reviews

Fast-moving development introduces risk. Code may contain logic errors, security flaws, or performance issues that slip through and reach production.

The [kluster.ai](https://www.kluster.ai/){target=\_blank} Code Reviews service integrates directly into your development workflow, scanning code in real-time. It catches potential issues instantly within your IDE, allowing you to ship code confidently.

## Prerequisites

Before getting started, ensure you have:

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.

As kluster.ai services work via MCP, the API key is created and configured for you when setting up the relevant extensions.
## Setup instructions

### IDE extensions

=== "VS Code / Codex VS Code"

    1. Click the **Add to VS Code** button below:

         [:octicons-arrow-right-24: Add to VS Code](vscode:extension/klusterai.kluster-verify-code){target=\_blank .md-button .md-button--primary}
    2. VS Code will open and display the extension.

    3. Click **Install** to get the extension.

        ![Install Extension](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-1.webp)

    Now that the extension is installed, you need to log in with your kluster.ai account:

    1. Click on **Sign in** in the bottom right corner.
       ![Sign In](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-2.webp)

    2. Choose **Open**. A browser pop-up window will take you to your kluster.ai account.

        ![Open Pop-up](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-3.webp)

    3. Click **Open Visual Studio Code**.

        ![Open Visual Studio Code](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-4.webp)

    4. Click **Open** to install the MCP with your kluster.ai API key.

        ![Open and Install MCP](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-5.webp)

    Once signed in, to enable kluster.ai in the VS Code agent chat window, take the following steps:

    1. Open a Copilot chat window and select the **Tools** button on the bottom right corner.
    2. Search for **kluster** or scroll down the list until you find **Kluster-Verify-Tool**.
    3. Check the **Kluster-Verify-Tool** box.

    ![Active MCP Tools in VS Code](/kluster-mkdocs/images/code-reviews/get-started/installation/vscode/vscode-integration-6.webp)

=== "Cursor"

    1. Click the **Add to Cursor** button below.

         [:octicons-arrow-right-24: Add to Cursor](cursor:extension/klusterai.kluster-verify-code){target=\_blank .md-button .md-button--primary}
    2. Cursor will open and prompt for extension installation.

    3. Click **Install** to add the extension into Cursor.

        ![Extension Installation Prompt in Cursor](/kluster-mkdocs/images/code-reviews/get-started/installation/cursor/cursor-integration-1.webp)

    Once installed, you can verify the setup:

    1. Open **Cursor Settings**. You can use the gear icon in the top right corner to do so.
    2. Navigate to **Tools & Integrations** → **MCP Tools**.
    3. You should see **extension-Kluster-Code-Reviews** with all tools enabled:

        - **`kluster_code_review_auto`**: Automatic code security, quality, and compliance verification.
        - **`kluster_dependency_check`**: Dependency health and risk checks.
        - **`kluster_code_review_manual`**: On-demand, user-requested per-file verification (security, quality, compliance).
        ![Active MCP Tools in Cursor](/kluster-mkdocs/images/code-reviews/get-started/installation/cursor/cursor-integration-2.webp)

=== "JetBrains"

    !!! warning "AI coding agent support"
        kluster.ai MCP integration in JetBrains requires the **Junie** AI agent. Install Junie separately from **Settings** :material-cog: → **Plugins** → **Marketplace** by searching for **Junie**. Other JetBrains AI agents are not supported.

    kluster.ai supports JetBrains IDEs such as IntelliJ IDEA and WebStorm. Open the JetBrains IDE of your choice, and go to **Settings** :material-cog: → **Plugins** → **Marketplace**.
    
    1. Search for **kluster**.
    2. Click **Install**.
    3. Click **Accept** when the third-party plugin notice appears, then restart the IDE if prompted.

        ![Install kluster.ai plugin from JetBrains Marketplace](/kluster-mkdocs/images/code-reviews/get-started/installation/jetbrains/jetbrains-integration-1.webp)

    !!! tip "Alternative: install from the JetBrains Marketplace website"
        You can also install the plugin from the [JetBrains Marketplace](https://plugins.jetbrains.com/plugin/30646-kluster-ai){target=\_blank} website. Click **Install** on the plugin page and follow the prompts to open your IDE.

    Now that the plugin is installed, you need to log in with your kluster.ai account:

    1. Click **Sign in to kluster** in the plugin panel.

        ![Sign in to kluster in JetBrains](/kluster-mkdocs/images/code-reviews/get-started/installation/jetbrains/jetbrains-integration-2.webp)

    2. A browser window opens and takes you to your kluster.ai account. Once you authorize, a success notification appears.

        ![Browser authorization success for kluster.ai](/kluster-mkdocs/images/code-reviews/get-started/installation/jetbrains/jetbrains-integration-3.webp)

    3. Return to your IDE. You are now logged in.

        ![Successfully logged in to kluster.ai in JetBrains](/kluster-mkdocs/images/code-reviews/get-started/installation/jetbrains/jetbrains-integration-4.webp)

    **Alternative: log in with an API key**

    If the browser sign-in flow is unavailable, you can log in using an API key. Retrieve your key from the [kluster.ai platform](https://platform.kluster.ai){target=\_blank} and paste it into the API key field in the plugin panel.

    Once installed, verify the setup:

    1. Open the kluster.ai plugin panel from the right sidebar.
    2. Confirm that your account is connected and the plugin is active.

        ![Active kluster.ai plugin in JetBrains](/kluster-mkdocs/images/code-reviews/get-started/installation/jetbrains/jetbrains-integration-5.webp)

=== "Windsurf"

    1. Click the **Add to Windsurf** button below.

         [:octicons-arrow-right-24: Add to Windsurf](windsurf:extension/klusterai.kluster-verify-code){target=\_blank .md-button .md-button--primary}
    2. Windsurf will open and prompt for extension installation.

    3. Click **Install** to add the extension into Windsurf.

        ![Extension Installation Prompt in Windsurf](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-1.webp)

    4. Select **Trust Publisher & Install**.

        ![Trust publisher](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-2.webp)

    Now that the extension is installed, you need to log in with your kluster.ai account:

    1. Click on **Sign in** in the bottom left corner.

        ![Sign In](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-3.webp)

    2. Choose **Open**. A browser pop-up window will take you to your kluster.ai account.

        ![Open Pop-up](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-4.webp)

    3. Click **Open Windsurf**.

        ![Open Windsurf](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-5.webp)

    4. Click **Open** to install the MCP with your kluster.ai API key.

        ![Open and Install MCP](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-6.webp)

    Once installed, verify the setup:

    1. Navigate to **Options** → **Windsurf Settings** → **MCP Servers** → **Open MCP Marketplace**.
    2. You should see **Kluster-Verify-Code** with all tools enabled.

        ![Active MCP Tools in Windsurf](/kluster-mkdocs/images/code-reviews/get-started/installation/windsurf/windsurf-integration-7.webp)

=== "Antigravity"

    1. Click the **Add to Antigravity** button below.

         [:octicons-arrow-right-24: Add to Antigravity](antigravity:extension/klusterai.kluster-verify-code){target=\_blank .md-button .md-button--primary}
    2. Antigravity will open and prompt for extension installation.

    3. Click **Install** to add the extension into Antigravity.

        ![Extension Installation Prompt in Antigravity](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-1.webp)

    Now that the extension is installed, you need to log in with your kluster.ai account:

    1. Click **Sign in** in the bottom left corner.

        ![Sign In](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-2.webp)

    2. Choose **Open**. A browser pop-up window will take you to your kluster.ai account.

        ![Open Pop-up](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-3.webp)

    3. Click **Open Antigravity**.

        ![Open Antigravity](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-4.webp)

    4. Click **Open** to install the MCP with your kluster.ai API key.

        ![Open and Install MCP](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-5.webp)

    Once installed, verify the setup:

    1. Navigate to **Settings** → **MCP Settings** → **Manage MCP Servers**.
    2. Verify that **Kluster-Verify-Code** appears with all tools enabled.

        ![Active MCP Tools in Antigravity](/kluster-mkdocs/images/code-reviews/get-started/installation/antigravity/antigravity-integration-6.webp)

### Terminal tools

=== "Claude Code"

    **Terminal installation**

    Log in to the [kluster.ai platform](https://platform.kluster.ai){target=\_blank}, and copy the Claude Code configuration snippet. This will include your API key.

    The command is similar to:

    ```bash
    npx -y @klusterai/ide-installer YOUR_API_KEY claude
    ```
    This command will:

    - Download the kluster.ai MCP server.
    - Configure Claude Code settings.
    - Set up your API key.
    - Enable all review tools.

    <div data-termynal>
      <span data-ty  ="input"> npx -y @klusterai/ide-installer YOUR_API_KEY claude</span>
      <span data-ty>🔧 Installing Kluster.ai server...</span>
      <span data-ty>✅ Installation complete!</span>
      <span data-ty>Restart Claude Code to apply the new rules</span>
      <span data-ty>Happy {K}oding ;)</span>
    </div>
    Once installed, verify the setup:

    1. Run the `/mcp` command in Claude Code.

        <div data-termynal>
          <span data-ty  ="input"> claude /mcp</span>
          <span data-ty></span>
          <span data-ty>✨ Welcome to Claude Code!</span>
          <span data-ty>/help for help, /status for your current setup</span>
          <span data-ty>cwd: /Users/kluster/code/demos/claude-code/mcp-demo</span>
          <span data-ty></span>
          <span data-ty>Tips for getting started:</span>
          <span data-ty>Ask Claude to create a new app or clone a repository</span>
          <span data-ty>Use Claude to help with file analysis, editing, bash commands and git</span>
          <span data-ty>Be as specific as you would with another engineer for the best results</span>
          <span data-ty>✔ Run /terminal-setup to set up terminal integration</span>
          <span data-ty></span>
          <span data-ty ="input"> /mcp</span>
          <span data-ty>Manage MCP servers</span>
          <span data-ty>  1. kluster-verify ✔ connected • Enter to view details</span>
          <span data-ty></span>
          <span data-ty>MCP Config locations (by scope):</span>
          <span data-ty> • User config: /Users/kluster/.claude.json</span>
          <span data-ty> • Project config (shared via .mcp.json):</span>
          <span data-ty>   /Users/kluster/code/demos/claude-code/mcp-demo/.mcp.json (file does not exist)</span>
          <span data-ty> • Local config (private to this project):</span>
          <span data-ty>   /Users/kluster/.claude.json [project: /Users/kluster/code/demos/claude-code/mcp-demo]</span>
          <span data-ty></span>
          <span data-ty>For help configuring MCP servers, see:</span>
          <span data-ty>https://docs.anthropic.com/en/docs/claude-code/mcp</span>
        </div>
    2. Select **kluster-code-reviews** in the MCP menu list and press enter to **View tools**.

        <div data-termynal>
          <span data-ty>Kluster-verify MCP Server</span>
          <span data-ty>Status: ✔ connected</span>
          <span data-ty>Command: npx</span>
          <span data-ty>Args: -y @klusterai/kluster-verify-code-mcp@latest</span>
          <span data-ty>Config location: /Users/kluster/.claude.json</span>
          <span data-ty>Capabilities: tools</span>
          <span data-ty>Tools: 3 tools</span>
          <span data-ty></span>
          <span data-ty>  1. View tools</span>
          <span data-ty>  2. Reconnect</span>
        </div>
    3. Select **View tools** to see the tools for **kluster-code-reviews** listed, including:

        - **`kluster_code_review_auto`**: Automatic code security, quality, and compliance verification.
        - **`kluster_dependency_check`**: Dependency health and risk checks.
        - **`kluster_code_review_manual`**: On-demand, user-requested per-file verification (security, quality, compliance).
        <div data-termynal>
          <span data-ty>Tools for kluster-verify (3 tools)</span>
          <span data-ty>  1. kluster_code_review_auto</span>
          <span data-ty>  2. kluster_dependency_check</span>
          <span data-ty>  3. kluster_code_review_manual</span>
        </div>
    ![Claude Code Installation Demo](/kluster-mkdocs/images/code-reviews/get-started/installation/claudecode/claude.gif)

=== "Codex CLI"

    **Terminal installation**

    Log in to the [kluster.ai platform](https://platform.kluster.ai){target=\_blank}, and copy the Codex CLI configuration snippet. This will include your API key.

    Run this command to install and configure kluster.ai for Codex CLI:

    ```bash
    npx -y @klusterai/ide-installer YOUR_API_KEY codex
    ```

    This command will:

    - Download the kluster.ai MCP server.
    - Configure Codex CLI settings.
    - Set up your API key.
    - Enable all review tools (auto, manual, and dependency check).

    <div data-termynal>
      <span data-ty  ="input"> npx -y @klusterai/ide-installer YOUR_API_KEY codex</span>
      <span data-ty>🔧 Installing Kluster.ai server...</span>
      <span data-ty>✅ Installation complete!</span>
      <span data-ty>Restart Codex CLI to apply the new rules</span>
      <span data-ty>Happy {K}oding ;)</span>
    </div>

    You can verify successful installation with the following command:

    ```bash
    codex /tools
    ```

    <div data-termynal>
      <span data-ty  ="input"> codex /tools</span>
      <span data-ty>╭───────────────────────────────────────────╮</span>
      <span data-ty>│ >_ OpenAI Codex (v0.50.0)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│</span>
      <span data-ty>│&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│</span>
      <span data-ty>│ model:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;gpt-5-codex&nbsp;&nbsp;&nbsp;/model to change │</span>
      <span data-ty>│ directory: ~/workspace/codex&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;│</span>
      <span data-ty>╰───────────────────────────────────────────╯</span>
      <span data-ty>› /tools</span>
      <span data-ty>• Available tools right now:</span>
      <span data-ty>  - shell: run terminal commands via execvp (use ["bash","-lc", "..."] and set</span>
      <span data-ty>    workdir).</span>
      <span data-ty>  - list_mcp_resources, list_mcp_resource_templates, read_mcp_resource: browse/</span>
      <span data-ty>    read context shared by MCP servers.</span>
      <span data-ty>  - update_plan: maintain a task plan (skip for very simple tasks, never single-</span>
      <span data-ty>    step).</span>
      <span data-ty>  - apply_patch: edit files via unified diff patches.</span>
      <span data-ty>  - view_image: attach a local image into the conversation.</span>
      <span data-ty>  - Kluster verification tools (mandatory after any code change):</span>
      <span data-ty>      - mcp__kluster-verify__kluster_code_review_auto</span>
      <span data-ty>      - mcp__kluster-verify__kluster_code_review_manual (manual review when</span>
      <span data-ty>        explicitly requested)</span>
      <span data-ty>      - mcp__kluster-verify__kluster_dependency_check (before dependency</span>
      <span data-ty>        operations)</span>
    </div>
    Upon successful installation, all kluster review tools will appear in the tools list, including auto, manual, and dependency check.

    ![Codex CLI Installation Demo](/kluster-mkdocs/images/code-reviews/get-started/installation/codex-cli/codex-cli.gif)

=== "CLI (Standalone)"

    kluster-cli is a standalone command-line tool that works without an IDE or AI assistant. Install it directly on macOS, Linux, or Windows.

    **macOS / Linux / WSL:**

    ```bash
    curl -fsSL https://cli.kluster.ai/install.sh | sh
    ```

    **Windows PowerShell:**

    ```powershell
    irm https://cli.kluster.ai/install.ps1 | iex
    ```

    After installing, authenticate with your API key:

    ```bash
    kluster login
    ```

    For shell completions, updates, and more, see the full [CLI installation guide](/kluster-mkdocs/code-reviews/cli/installation/).

    [:octicons-arrow-right-24: CLI quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/)

## Next steps

- **[Human-written code](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)**: Learn about on-demand reviews in your editor
- **[AI-generated code](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)**: Learn about automatic reviews for AI-assisted coding
- **[Pick your workflow](/kluster-mkdocs/code-reviews/get-started/pick-your-workflow/)**: Decide which mode fits your workflow


---

Page Title: MCP Tools Reference

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-reference-mcp-tools.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/reference/mcp-tools/
- Summary: Learn how kluster.ai Code MCP tools work, including parameters, response formats, issue categories, and settings for real-time code reviews.
- Word Count: 573; Token Estimate: 1031
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:f8225ffd93f2e51ef6fe60c33a5db0965110a42ca011c802d8289ee0d5c77769

# MCP Tools Reference

The [kluster.ai](https://www.kluster.ai/){target=\_blank} Code MCP server provides review tools for checking code quality and security. These tools enable real-time code reviews directly within your IDE through MCP integration.

## Available tools

- **`kluster_code_review_auto`**: Automatically reviews code quality and detects bugs, including logic errors, security issues, and performance problems. Triggers automatically when code is generated or modified. Best for real-time reviews during active coding sessions, analyzing changes in context of the full conversation and related files.
- **`kluster_dependency_check`**: Validates the security and compliance of packages and dependencies. Triggers automatically before package installations or when package files are updated. Best for preventing vulnerable or non-compliant third-party libraries from entering your codebase before installation.
- **`kluster_code_review_manual`**: Manually reviews specific files when explicitly requested by the user (e.g., "review this file", "check for bugs"). Best for auditing existing code, reviewing specific modules, or getting fix recommendations for individual files.

This page documents the parameters and response formats you'll see when using these tools in Cursor, Claude Code, or any MCP-compatible client.

## Parameters

=== "Automatic Reviews and Dependency Check"

    These tools analyze code changes and dependencies to detect bugs, security vulnerabilities, and other quality issues. Used for AI-generated code.

    ???+ interface "Parameters"

        `code_diff` ++"string"++ <span class="required" markdown>++"required"++</span>

        Unified diff format showing the actual changes (additions and subtractions) made to files. Use standard diff format with `--- filename` and `+++ filename` headers, followed by `@@ line numbers @@`, and `+` for additions, `-` for deletions. In MCP environments, this is often auto-extracted from IDE history.

        ---

        `user_requests` ++"string"++ <span class="required" markdown>++"required"++</span>

        A chronological sequence of all user messages and requests in this conversation thread, with the current request (that triggered this assistant turn) clearly marked. Format: Previous requests as numbered list, then current request marked with `>>> CURRENT REQUEST: [request text]`. In MCP environments, this is often auto-extracted from conversation history.

        ---

        `modified_files_path` ++"string"++ <span class="required" markdown>++"required"++</span>

        Full absolute paths of modified files separated by `;`.

        ---

        `chat_id` ++"string"++ <span class="optional" markdown>++"optional"++</span>

        Session identifier returned by previous tool calls. Used to maintain context across multiple review requests.

=== "On-demand Review Tool"

    The on-demand review tool is triggered when explicitly requested. Used for both AI-generated code (when you ask your AI to review code) and human-written code (when you use the extension UI).

    ???+ interface "Parameters"

        `user_requests` ++"string"++ <span class="required" markdown>++"required"++</span>

        Chronological sequence of user messages with current request marked as `>>> CURRENT REQUEST:`. Unlike automatic reviews, this parameter is NOT auto-extracted in MCP environments and must be explicitly provided.

        ---

        `modified_file_path` ++"string"++ <span class="required" markdown>++"required"++</span>

        Full absolute path of the single file to review. This tool can only check one file per call.

        ---

        `need_fixes` ++"boolean"++ <span class="required" markdown>++"required"++</span>

        Set to `true` if user requested fixes, `false` if only requesting issue detection.

        ---

        `chat_id` ++"string"++ <span class="optional" markdown>++"optional"++</span>

        Session identifier returned by previous tool calls. Used to maintain context across multiple review requests.

## Response format

All code review tools return the same response structure. See the [Response Schema](/kluster-mkdocs/code-reviews/reference/response-schema/) for complete details.

## Next steps

- **[Response Schema](/kluster-mkdocs/code-reviews/reference/response-schema/)**: Understand the response format in detail
- **[Configure settings](/kluster-mkdocs/code-reviews/configuration/options/)**: Customize review behavior for your needs
- **[Installation](/kluster-mkdocs/code-reviews/get-started/installation/)**: Set up kluster.ai in your IDE


---

Page Title: On-demand reviews for human-written code

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-ide-reviews-human-written-code-on-demand-reviews.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/ide-reviews/human-written-code/on-demand-reviews/
- Summary: Trigger on-demand code reviews in your IDE using right-click, hint buttons, or pre-commit scanning to verify code quality on your own terms.
- Word Count: 900; Token Estimate: 1600
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:955fc09979beb0beb406b5c7ddfe96ffdd8e1b4ca0cdf71d9b5acd6079d8c4d2

# On-demand reviews 

With [kluster.ai](https://www.kluster.ai/){target=\_blank}, you can trigger reviews three ways: right-click any selection, use hint buttons, or scan uncommitted changes.

!!! tip "Exclude files with .klusterignore"
    If there are files or folders you never want kluster.ai to review (generated code, build output, vendored dependencies), add them to a [`.klusterignore`](/kluster-mkdocs/code-reviews/configuration/klusterignore/) file. On-demand IDE reviews respect `.klusterignore`.

## Prerequisites

Before getting started, ensure you have:

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.
- **kluster.ai installed in your IDE**: Follow the [Installation guide](/kluster-mkdocs/code-reviews/get-started/installation/) to set it up in your favourite IDE.
<div class="embed-container">
    <iframe
        src="https://www.youtube.com/embed/rpWt9sXAqWY"
        title="Human-written code reviews with kluster.ai"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
        loading="lazy">
    </iframe>
</div>

## How on-demand reviews work

1.  **You write code**: Work in your editor as usual.
2.  **You trigger review**: Right-click, use a hint button, or click in the sidebar.
3.  **kluster.ai analyzes**: Results appear with issues and suggested fixes.

## Sidebar review

Open the kluster.ai extension to access the **On-Demand Review** section in the sidebar. Use the **Mode** dropdown to choose what to review:

- **Review current file**: Verifies only the file currently open in the editor.
- **Review uncommitted changes**: Verifies all uncommitted changes across multiple files.
- **Review all branch changes**: Verifies all changes compared against the selected base branch.

![On-Demand Review section showing the Mode dropdown options](/kluster-mkdocs/images/code-reviews/ide-reviews/human-written-code/on-demand-reviews/manual-review-this-code-extension.webp)

Then choose your analysis depth for your code reviews:

- **Instant**: Completes in about five seconds. Detects most issues and is suited for fast review and iteration cycles.
- **Deep**: Takes up to a few minutes. Conducts deeper analysis to uncover even subtle edge cases, ideal for critical code and final reviews.
![On-Demand Review section showing Instant Review and Deep Review buttons](/kluster-mkdocs/images/code-reviews/ide-reviews/human-written-code/on-demand-reviews/manual-review-this-code-extension-deep-vs-instant.webp)

!!! info "Accessing On-Demand Review"
    You can also access On-Demand Review from the **Home** and **Git** tabs. Expand the kluster.ai section if collapsed.

After the review completes, kluster.ai displays any issues found. For each issue, you have three actions:

- **Fix with AI**: Generates an AI-powered fix suggestion that you can apply with one click.
- **Snooze**: Temporarily hides the issue for a selected duration (1 day, 7 days, or 30 days). The issue reappears automatically after the snooze period expires.
- **Ignore**: Permanently dismisses the issue. It will not reappear in future reviews.

![Review results showing issues found with Fix with AI, Snooze, and Ignore actions](/kluster-mkdocs/images/code-reviews/ide-reviews/human-written-code/on-demand-reviews/manual-review-this-code-extension-results.webp)

!!! tip "When to snooze vs. ignore"
    Use **Snooze** for issues you plan to address later but don't want cluttering your current review. Use **Ignore** for false positives or accepted risks that don't need further attention.

## Code block review

Select any code in your editor, right-click, and choose **Review with kluster.ai** (or press `Ctrl+Shift+K`). This is useful for:

- Verifying a specific function or block you just wrote.
- Checking code during merge conflict resolution.
- Getting a quick security check before moving on.

![Right-click to review selected code](/kluster-mkdocs/images/code-reviews/ide-reviews/human-written-code/on-demand-reviews/manual-review-this-code.webp)

!!! info "Hint button"
    When you select code, a hint button also appears next to your selection to trigger the review. This hint button is not yet available in Cursor—use the right-click menu or keyboard shortcut instead.

## Compatible with

<div class="grid cards" markdown>

-   :simple-cursor: **Cursor**

    ---

    AI-native code editor with built-in kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Cursor](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :material-microsoft-visual-studio-code: **VS Code**

    ---

    Lightweight editor with kluster.ai extension and Copilot integration.

    [:octicons-arrow-right-24: Install for VS Code](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-windsurf: **Windsurf**

    ---

    AI-powered IDE by Codeium with kluster.ai extension support.

    [:octicons-arrow-right-24: Install for Windsurf](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :antigravity-antigravity: **Antigravity**

    ---

    Next-generation IDE with native MCP integration for kluster.ai.

    [:octicons-arrow-right-24: Install for Antigravity](/kluster-mkdocs/code-reviews/get-started/installation/)

-   :simple-jetbrains: **JetBrains**

    ---

    JetBrains IDEs (IntelliJ IDEA, WebStorm, and others) with kluster.ai plugin support.

    [:octicons-arrow-right-24: Install for JetBrains](/kluster-mkdocs/code-reviews/get-started/installation/)

</div>

## Configuration

You can customize how on-demand reviews work in your [configuration options](/kluster-mkdocs/code-reviews/configuration/options/):

- **Analysis level**: Set default depth for Instant vs Deep reviews.
- **Enabled tools**: Toggle Code Review and Dependency Analysis on/off.
- **Sensitivity**: Adjust how strictly issues are flagged (Low → Critical).
- **Bug check types**: Select which issue types to check (Security, Logic, Performance, etc.).

## Next steps

- **[MCP Tools Reference](/kluster-mkdocs/code-reviews/reference/mcp-tools/)**: Deep dive into all MCP tools and parameters.
- **[Configuration Options](/kluster-mkdocs/code-reviews/configuration/options/)**: Customize Code Reviews behavior for your workflow.


---

Page Title: Options

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-configuration-options.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/configuration/options/
- Summary: Configure kluster.ai Code Review settings, from analysis depth and sensitivity levels to issue types and enabled tools used to verify code across your workflow.
- Word Count: 602; Token Estimate: 1034
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:09fbaa3fd9d7cbfd885d956d37864a65726e65e3b36bac773791f938e7a30e12

# Options

You can customize the [kluster.ai](https://www.kluster.ai/){target=\_blank} Code Reviews behavior through the platform settings or directly in your IDE. The options page is available in the left-hand menu under **Review options**, where you can configure sensitivity levels for issue reporting, select which types of bug checks to run, and enable or disable specific MCP tools to match your development workflow.

![Code Review Options interface](/kluster-mkdocs/images/code-reviews/configuration/configuration-01.webp)

## Sensitivity settings

Configure the minimum sensitivity level for the real-time Code Reviews issue reporting. Set your threshold based on your team's requirements:

- **Low**: Detects even the smallest potential issues.
- **Medium**: Suitable for projects requiring strong security and high code quality.
- **High**: (Recommended) Balances strong protection against LLM hallucination and security issues with performance.
- **Critical**: Focuses only on critical issues for faster iteration and smoother coding experience.

!!! info "Choosing a sensitivity level"
    The ideal setting depends on your use case. In general, a **High** level is a good starting point, but you might want to set it to **Medium** for production workflows.

## Code review scope

Select which types of issues real-time Code Review detects during analysis. Each type specifies a category of issues the system can identify.

|     Type      |           Description           |                Example                |
|:-------------:|:-------------------------------:|:-------------------------------------:|
|   **Intent**    | Code doesn't match user request | User asked for sorting, got filtering |
|  **Semantic**   |    Meaning and type errors      |        Wrong variable type used       |
|  **Knowledge**  |    Best practice violations     |       Not following conventions       |
| **Performance** |       Performance issues        |        Inefficient algorithms         |
|   **Quality**   |      Code quality problems      |        Poor naming, complexity        |
|   **Logical**   |     Control flow errors         |           Off-by-one errors           |
|  **Security**   |    Security vulnerabilities     |          SQL injection risks          |

## Enabled tools

Control which review tools run in your development environment. Enable or disable each tool based on your project's specific needs and workflow.

- **Real-time Code Review**: For code quality reviews.
- **Dependency Analysis**: For package and dependency security.
- **Ambient Background Reviews (Beta, Enterprise plan)**: Automatic reviews that run in the background after you pause typing.

## Analysis level

Control review depth to balance between speed and thoroughness. You can configure different analysis levels for human-driven and AI-driven development workflows.

![Analysis Level settings showing options for Human-Driven and AI-Driven Development](/kluster-mkdocs/images/code-reviews/configuration/configuration-02.webp)

- **Instant**: Completes in about five seconds. Detects most issues and is suited for fast review and iteration cycles.
- **Deep**: Takes up to a few minutes. Conducts deeper analysis to uncover even subtle edge cases, ideal for critical code and final reviews.
### Human-driven development

Configure analysis depth for reviews you trigger directly in your IDE:

- **When I click Review button in IDE**: Runs an on-demand review that applies to the current file, uncommitted changes, or the active branch.
- **When I type code**: Reviews code continuously as you write, automatically analyzing changes and highlighting potential issues.

### AI-driven development

Configure analysis depth for reviews triggered through AI assistants:

- **When AI agent writes code**: Automatically reviews code generated by an AI assistant as it is produced.
- **When I ask AI agent to review code**: Runs a review when you explicitly request a review from an AI assistant.

The default configuration uses **Deep** for human-driven workflows and **Instant** for AI-driven workflows. For critical code, choose **Deep** regardless of workflow—use it for final reviews, production changes, and any time correctness matters more than speed.

## Next steps

- [Create custom rules](/kluster-mkdocs/code-reviews/configuration/rules/): Add project-specific development standards.
- [View MCP tools reference](/kluster-mkdocs/code-reviews/reference/mcp-tools/): Understand the technical API details.
- [Installation guide](/kluster-mkdocs/code-reviews/get-started/installation/): Set up Code Reviews in your IDE.


---

Page Title: Pick Your Code Review Workflow

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-get-started-pick-your-workflow.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/get-started/pick-your-workflow/
- Summary: Compare the supported Code Reviews modes—human-written, AI-generated, CLI, and repo-wide—and pick the workflow that fits how you write code.
- Word Count: 1069; Token Estimate: 1653
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:4aacc383fb52d19c3d020e3ca7c99e095eeb8f952eee85ad7c5846457077d82c

# Pick your workflow

Code Reviews offers four distinct modes that adapt to how you work. Whether you're coding with an AI assistant, writing code directly, reviewing from the terminal, or analyzing your entire codebase, this guide helps you understand which mode fits your workflow—and why many developers use more than one.

## Choose your mode

<div class="grid cards" markdown>

-   **Human-written code**

    ---

    For developers writing code directly. Review any code on-demand with a right-click, keyboard shortcut, or sidebar button. No AI assistant needed—just you and your editor.

    [:octicons-arrow-right-24: Learn more](#human-written-code)

-   **AI-generated code**

    ---

    For developers using AI coding assistants. Your code is reviewed automatically every time your AI generates or modifies code—no manual steps required.

    [:octicons-arrow-right-24: Learn more](#ai-generated-code)

-   **CLI**

    ---

    For terminal-based workflows and automation. Review code from the command line, automate with git hooks, or integrate into CI/CD pipelines.

    [:octicons-arrow-right-24: Learn more](#cli)

-   **Repo reviews**

    ---

    For analyzing your entire codebase. Find bugs that emerge from interactions across modules—issues that survive individual PR reviews because they're only visible at the system level.

    [:octicons-arrow-right-24: Learn more](#repo-reviews)

</div>

## Human-written code

Human-written code reviews give you direct control over when reviews happen. Select any code in your editor and trigger a review instantly—no AI assistant required. This mode is built into the kluster.ai extension and provides three ways to review: right-click menu, keyboard shortcut, or the extension sidebar.

Use it to review code you wrote yourself, audit files before committing, or check legacy code you inherited. The reviews run the same comprehensive analysis as AI-generated code reviews, just triggered manually instead of automatically.

**Compatible with**: Cursor, VS Code, Windsurf, Antigravity, JetBrains (IDEs only).

!!! info "Not available for CLI tools"
    Human-written code reviews require an IDE extension. For CLI tools like Claude Code or Codex CLI, use AI-generated code reviews instead.

[:octicons-arrow-right-24: Get started with human-written code reviews](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)


## AI-generated code

AI-generated code reviews integrate directly with your AI coding assistant. When the AI generates or modifies code, [kluster.ai](https://www.kluster.ai/){target=\_blank} automatically analyzes the changes in real-time. You can also ask your AI to review existing files on demand—just say "review this file" and the AI triggers an on-demand review.

This mode is designed for developers who code with AI assistants like Claude Code, Cursor, or Copilot. The review happens seamlessly in the background, catching security vulnerabilities, logic errors, and quality issues before they become problems.

**Compatible with**:

- **IDE extensions**: Cursor, VS Code, Windsurf, Antigravity, JetBrains.
- **CLI tools**: Claude Code, Codex CLI.

[:octicons-arrow-right-24: Get started with AI-generated code reviews](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)


## CLI

The kluster-cli tool brings code reviews to your terminal. Review staged changes, diffs against branches, or individual files—all without opening an IDE. Install git hooks to automate reviews on every commit or push, or use JSON output to integrate reviews into scripts and CI/CD pipelines.

Use it when you prefer terminal workflows, need to automate reviews in git hooks, or want to integrate code reviews into CI/CD.

**Available on**: macOS, Linux, Windows.

[:octicons-arrow-right-24: Get started with CLI](/kluster-mkdocs/code-reviews/cli/quickstart/)


## Repo reviews

Repo reviews take a fundamentally different approach: instead of reviewing individual changes, it analyzes your entire repository as a complete system. This reveals bugs and risks that don't belong to any single PR or file—issues that only become visible when you examine how multiple parts of your code interact.

Use repo reviews to catch problems that slip through PR-level reviews:

- **Cross-module interactions**: Code paths that work in isolation but break when components interact.
- **System-wide vulnerabilities**: Security checks that exist in some code paths but are bypassed in others.
- **State management issues**: State that becomes inconsistent under edge cases like retries or partial failures.
- **Assumption violations**: Logic that depends on constraints enforced elsewhere in the codebase.

Repo reviews complement your existing review workflow. Run them periodically to surface issues that already exist in your codebase—problems that would otherwise remain hidden until they cause production incidents.

**Available on**: Web dashboard and `kluster-cli` (requires GitHub, GitLab, or Bitbucket connection).

!!! note "Usage limits"
    Pro plans include 1 repo review per month. Enterprise plans include higher limits. [Contact us](https://www.kluster.ai/contact){target=\_blank} to learn more.

[:octicons-arrow-right-24: Get started with repo reviews](/kluster-mkdocs/code-reviews/repo-reviews/quickstart/)


## Using multiple modes

Most teams combine multiple review modes:

- **Human-written code reviews**: For reviewing code you write directly in your editor.
- **AI-generated code reviews**: For catching issues as your AI assistant generates code.
- **CLI**: For terminal workflows, git hook automation, and CI/CD integration.
- **Repo reviews**: For periodic system-wide analysis to catch cross-module bugs.

If you use Cursor, VS Code, Windsurf, Antigravity, or JetBrains, you get both human-written and AI-generated code reviews in a single installation—switch seamlessly between AI-assisted coding and manual reviews without changing tools.

Add CLI hooks to enforce reviews on every push, and run repo reviews periodically as a safety net to catch system-wide issues that survive individual code reviews.

## Enrich reviews with External Knowledge

Connect kluster to external tools like Jira so your code reviews include project requirements and ticket specifications. When kluster knows what you're building, it can verify that your implementation matches the spec — not just that the code is correct.

[:octicons-arrow-right-24: Set up External Knowledge](/kluster-mkdocs/code-reviews/external-knowledge/quickstart/)

## Next steps

- **[Human-written code](/kluster-mkdocs/code-reviews/ide-reviews/human-written-code/on-demand-reviews/)**: Set up on-demand reviews in your editor.
- **[AI-generated code](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)**: Set up automatic reviews for AI-assisted coding.
- **[CLI quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/)**: Review code from the terminal.
- **[Repo reviews quickstart](/kluster-mkdocs/code-reviews/repo-reviews/quickstart/)**: Run your first system-wide codebase analysis.
- **[External Knowledge quickstart](/kluster-mkdocs/code-reviews/external-knowledge/quickstart/)**: Connect kluster to Jira for context-aware reviews.


---

Page Title: Repo Reviews Quickstart

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-repo-reviews-quickstart.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/repo-reviews/quickstart/
- Summary: Learn how to run system-wide codebase analysis with kluster.ai Repo Reviews to find cross-module bugs that slip through PR-level reviews.
- Word Count: 743; Token Estimate: 1285
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:accaed64f0cd192a8542a3c13d60303c6a46d1c827c070ebfeb011185af98441

# Repo Reviews quickstart

Learn how to run system-wide codebase analysis with [kluster.ai](https://www.kluster.ai/){target=\_blank} Repo Reviews. Connect your repository, wait for the deep scan to complete, and review cross-module bugs that slip through PR-level reviews.

!!! tip "Prefer terminal workflows?"
    You can also run repo reviews from CLI with `kluster review repo start` and inspect results with `kluster review repo show`. See [Repo reviews from CLI](/kluster-mkdocs/code-reviews/cli/repo-reviews/).

<div class="embed-container">
    <iframe
        src="https://www.youtube.com/embed/qz32GZkGkqc"
        title="Repo Reviews with kluster.ai"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
        loading="lazy">
    </iframe>
</div>

## Prerequisites

Before getting started, ensure you have:

- **A kluster.ai account**: Sign up on the [kluster.ai platform](https://platform.kluster.ai/signup){target=\_blank} if you don't have one.
- **A connected repository**: You'll need to connect your GitHub, GitLab, or Bitbucket repository through the dashboard.

## How repo reviews work

Repo reviews analyze your entire codebase as a system instead of reviewing individual changes. When multiple parts of your code interact, issues emerge that don't show up in PR-level reviews.

1. **Connect your repository**: Link your GitHub, GitLab, or Bitbucket repository to kluster.ai.
2. **Scan starts automatically**: Wait for the deep analysis to complete.
3. **Review the findings**: Examine issues grouped by severity and type.

This catches cross-module bugs, state inconsistencies, bypassed validation checks, and other system-wide problems that slip through regular code reviews.

## Running your first repo review

### 1. Connect your repository

Go to the [Repo Reviews dashboard](https://platform.kluster.ai/repo-reviews){target=\_blank} and click **Connect Repository**.

![Repo Reviews dashboard with Connect Repository button](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-1.webp)

Select your Git provider (GitHub, GitLab, or Bitbucket):

![Select Git provider modal](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-2.webp)

Then choose the repository you want to analyze:

![Select repository from dropdown](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-3.webp)

### 2. Scan repo

Once your repository is connected, the analysis starts automatically and shows **"Review in progress..."**. The scan runs a deep analysis of your codebase. Depending on repository size, this takes several minutes. You'll receive an email notification once it's done.

You can close the page and come back later.

### 3. Review the results

When the scan finishes, you'll see a list of issues found in your codebase:

![Repo review results showing list of issues](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-4.webp)

Each issue displays:

- **Description**: Summary of the problem.
- **Severity**: High, Medium, or Low (shown with color badges).
- **Type**: The category of issue (Security, Logical, Performance, Knowledge, etc.).
- **Priority**: P0-P5 ranking for triage.

### 4. Examine issue details

Click a given bug or issue to learn more. The detail view includes:

- **Description**: What the problem is.
- **Explanation**: Why this is a problem and how it impacts your system.
- **Recommended Actions**: Steps to fix the issue.

![Issue detail view with description, explanation, and recommended actions](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-5.webp)

### 5. Take action

For each issue, you have four actions:

- **Copy**: Copy the issue details to share or save.
- **Fix with AI**: Get a prompt to paste into your AI assistant (Claude, Cursor, etc.) to fix it automatically.
- **Snooze**: Temporarily hides the issue for a selected duration (1 day, 7 days, or 30 days). The issue reappears automatically after the snooze period expires.
- **Ignore**: Permanently dismisses the issue. It will not reappear in future reviews.

![Take action on the bugs found by clicking one of the available actions](/kluster-mkdocs/images/code-reviews/repo-reviews/repo-reviews-setup-6.webp)

!!! tip "When to snooze vs. ignore"
    Use **Snooze** for issues you plan to address later but don't want cluttering your current review. Use **Ignore** for false positives or accepted risks that don't need further attention.

## Next steps

- **[Pick your workflow](/kluster-mkdocs/code-reviews/get-started/pick-your-workflow/)**: Learn when to use repo reviews vs. other review modes.
- **[Repo reviews from CLI](/kluster-mkdocs/code-reviews/cli/repo-reviews/)**: Trigger and inspect repo reviews from the terminal.
- **[Review modes](/kluster-mkdocs/code-reviews/review-modes/)**: Understand all available review types.
- **[FAQ](/kluster-mkdocs/code-reviews/faq/)**: Common questions about kluster.ai code reviews.


---

Page Title: Response Schema

- Resolved Markdown: https://docs.kluster.ai/ai/pages/code-reviews-reference-response-schema.md
- Canonical (HTML): https://docs.kluster.ai/code-reviews/reference/response-schema/
- Summary: Understand the response format from kluster.ai Code Reviews—issue structure, severity levels, priority system, and suggested fixes.
- Word Count: 481; Token Estimate: 1064
- Last Updated: 2026-03-27T17:26:06+00:00
- Version Hash: sha256:4db257462b049ef7737138bad61526455ec7ba032c7be72fa0b536439a31b2a0

# Response Schema

All kluster.ai code review tools return the same response structure. This page documents the fields you'll see in review responses.

## Response fields

- **`isCodeCorrect`**: Boolean indicating if the code has issues.
- **`explanation`**: Summary of all issues found.
- **`issues`**: Array of detected problems with:
  - **`type`**: Issue category (intent, semantic, knowledge, performance, quality, logical, security).
  - **`severity`**: Impact level (critical, high, medium, low).
  - **`priority`**: Execution priority (P0-P5).
  - **`description`**: Brief issue summary.
  - **`explanation`**: Detailed issue explanation.
  - **`actions`**: Recommended fixes.
- **`priority_instructions`**: Execution rules for addressing issues.
- **`agent_todo_list`**: Prioritized list of fixes to apply.
- **`chat_id`**: Session identifier for maintaining context across requests.

## Example response

```json
{
    "isCodeCorrect": false,
    "explanation": "Found 1 issue. 1 critical issue needs immediate attention.\n\nTODO:\n1. [CRITICAL] The implementation introduces a critical SQL injection vulnerability.",
    "issues": [
        {
            "type": "intent",
            "severity": "critical",
            "priority": "P0",
            "description": "The implementation introduces a critical SQL injection vulnerability, which is an unacceptable security risk.",
            "explanation": "The code constructs an SQL query using string concatenation with user input, which is the classic pattern for SQL injection. A function designed for database interaction should use parameterized queries.",
            "actions": "Use parameterized queries or prepared statements to safely handle user input. For example: db.query('SELECT * FROM users WHERE id = ?', [userId])"
        }
    ],
    "priority_instructions": "**PRIORITY EXECUTION RULES:**\n1. **INTENT Critical/High (P0-P1) get special priority**\n2. **All other issues sorted by severity** - Critical (P2) > High (P3) > Medium (P4) > Low (P5)\n3. **Never let lower priority issues override higher priority changes**",
    "agent_todo_list": [
        "**EXECUTE IN THIS EXACT ORDER:**",
        "",
        "**Priority P0 - INTENT CRITICAL (HIGHEST PRIORITY):**",
        "P0.1: The implementation introduces a critical SQL injection vulnerability - Use parameterized queries or prepared statements."
    ],
    "chat_id": "i8ct930591"
}
```

## Issue types

| Type | Description | Example |
|------|-------------|---------|
| `intent` | Code doesn't match user request | Asked for sorting, got filtering |
| `semantic` | Meaning and type errors | Wrong variable type used |
| `knowledge` | Best practice violations | Not following conventions |
| `performance` | Performance issues | Inefficient algorithms |
| `quality` | Code quality problems | Poor naming, complexity |
| `logical` | Control flow errors | Off-by-one errors |
| `security` | Security vulnerabilities | SQL injection risks |

## Severity levels

| Level | Meaning | Action |
|-------|---------|--------|
| `critical` | Security vulnerability or breaking issue | Fix immediately |
| `high` | Significant bug or security concern | Fix before production |
| `medium` | Quality issue or minor bug | Should fix |
| `low` | Style or minor improvement | Optional fix |

## Priority system

Code review assigns priority levels to detected issues, helping you focus on the most critical problems first. The system automatically prioritizes based on issue type and severity.

| Priority | Meaning |
|----------|---------|
| **P0-P1** | Intent issues (highest priority) - code doesn't match request |
| **P2** | Critical severity - must fix immediately |
| **P3** | High severity - should fix soon |
| **P4** | Medium severity - nice to fix |
| **P5** | Low severity - optional improvements |

## Next steps

- **[MCP Tools Reference](/kluster-mkdocs/code-reviews/reference/mcp-tools/)**: Learn about tool parameters
- **[Configure settings](/kluster-mkdocs/code-reviews/configuration/options/)**: Customize what issues get flagged
- **[AI-generated code](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)**: Learn how reviews work with AI assistants
