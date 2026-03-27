---
category: Reference
includes_base_categories: false
base_categories: []
word_count: 1754
token_estimate: 3795
page_count: 3
build_timestamp: '2026-03-27T17:27:40.236808+00:00'
version_hash: sha256:00b9e4aaeecb935f300da15ff1a54a4c37b81f770ff2b021587c7ce19ebba19b
---

# Begin New Bundle: Reference


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
