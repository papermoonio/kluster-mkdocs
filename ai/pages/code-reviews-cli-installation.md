---
title: CLI Installation
description: Install kluster-cli on macOS, Linux, or Windows. Set up shell completions, configure your PATH, and keep the CLI up to date.
categories:
- Basics
- CLI
url: https://docs.kluster.ai/code-reviews/cli/installation/
word_count: 828
token_estimate: 1827
version_hash: sha256:d1215f98100645a5d44434afdff2b1b0d8c042402d5ca72e79c8b9c04ce279ce
last_updated: '2026-03-27T17:26:06+00:00'
---

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
