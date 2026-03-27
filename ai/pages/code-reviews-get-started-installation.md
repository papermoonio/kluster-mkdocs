---
title: Install kluster.ai Code Reviews for Your IDE or CLI
description: Set up kluster.ai Code Reviews in minutes. Scan code for errors, vulnerabilities, and performance issues in Cursor, VS Code, JetBrains, and more.
categories:
- Basics
url: https://docs.kluster.ai/code-reviews/get-started/installation/
word_count: 2544
token_estimate: 5006
version_hash: sha256:0cd4c26fe0e2037f3f8f0de4ace3127191b7785252371fa545ac22cc7389db61
last_updated: '2026-03-27T17:26:06+00:00'
---

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
