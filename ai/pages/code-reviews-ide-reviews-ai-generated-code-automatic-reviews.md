---
title: Automatic reviews for AI-generated code
description: Set up automatic code reviews and dependency checks for AI-generated code. Reviews run in real-time as your AI writes code.
categories:
- Basics
- IDE Reviews
url: https://docs.kluster.ai/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/
word_count: 772
token_estimate: 1434
version_hash: sha256:b34ae3d8c947e3933699b72280dcc6ab524e08a6210581c8293119e600b4a509
last_updated: '2026-03-27T17:26:06+00:00'
---

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
