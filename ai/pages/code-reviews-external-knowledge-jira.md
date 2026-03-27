---
title: Set Up Jira Integration for Code Reviews
description: Connect Jira to kluster.ai to review code against ticket requirements. Set up Jira Cloud or self-hosted Jira and learn how ticket context flows into reviews.
categories:
- External Knowledge
url: https://docs.kluster.ai/code-reviews/external-knowledge/jira/
word_count: 1632
token_estimate: 3120
version_hash: sha256:9c20e95b73a751480df38b48d7f52552ab8b9c6628304b9c0eebd3324b4dcd2b
last_updated: '2026-03-27T17:26:06+00:00'
---

# Jira integration

The Jira integration connects your Jira project to [kluster.ai](https://www.kluster.ai/){target=\_blank} Code Reviews, allowing kluster to use ticket details as context during code reviews. When connected, kluster can verify whether your code matches the requirements defined in a Jira ticket, catching gaps between the specification and the implementation.

For example, if a Jira ticket specifies that a function must accept command-line arguments and support multiple algorithms, kluster flags missing requirements in your code. This turns code review into a requirements-aware process rather than a purely syntactic or security-focused check.

## Connect Jira

You can connect Jira from the [External Knowledge](https://platform.kluster.ai/external-knowledge){target=\_blank} page on the kluster.ai platform. The setup process depends on whether you use cloud-hosted Jira or a self-hosted (IT-managed) instance.

### Jira Cloud (OAuth)

For Jira Cloud instances, kluster uses an OAuth wizard for authentication.

1. Navigate to [External Knowledge](https://platform.kluster.ai/external-knowledge){target=\_blank} in the kluster.ai platform. Jira appears as an available source.

    ![External Knowledge page showing Jira as a source option](/kluster-mkdocs/images/code-reviews/external-knowledge/external-knowledge-jira-01.webp)

2. Click **Connect** next to Jira. This launches the Jira OAuth authorization wizard.

    ![Jira OAuth wizard connection notification](/kluster-mkdocs/images/code-reviews/external-knowledge/external-knowledge-jira-02.webp)

3. Accept the connection notification in the wizard to grant kluster access to your Jira instance.

4. Once the authorization completes, the Jira integration status changes to **Connected**. A list of Jira projects from your instance appears. Enable or disable specific projects to control which ticket data kluster can access during code reviews.

    ![Jira integration showing as Connected, select project](/kluster-mkdocs/images/code-reviews/external-knowledge/external-knowledge-jira-03.webp)

!!! tip "Restrict access to sensitive projects"
    If your Jira instance contains internal security, IT, or HR projects, disable them from the project list. This prevents their ticket details from being included in code review context.

### Self-hosted Jira (API token)

For self-hosted or IT-managed Jira instances that do not support OAuth, you can connect using an API token instead.

1. Navigate to [External Knowledge](https://platform.kluster.ai/external-knowledge){target=\_blank} in the kluster.ai platform.

2. Click the **Connect Jira** dropdown, and select **Connect via API token**.

    ![Connecting via API token](/kluster-mkdocs/images/code-reviews/external-knowledge/external-knowledge-jira-04.webp)

3. Fill in the self-hosted or IT-managed Jira instance details. Click **Connect** to complete the setup.

    ![Self-hosted Jira API token connection screen](/kluster-mkdocs/images/code-reviews/external-knowledge/external-knowledge-jira-05.webp)

## How Jira context flows into reviews

Once connected, kluster identifies Jira tickets by their **ticket ID** (e.g., `KAN-2`). The ticket context is automatically included in a code review when any of the following conditions are met:

- **Branch name contains the ticket ID**: For example, a branch named `feature/KAN-2` triggers kluster to pull in the requirements from ticket `KAN-2`.
- **Ticket ID is mentioned in the chat prompt**: Including the ticket ID in your message to the AI assistant (e.g., "Create a Python script that prints Pi (Ticket KAN-2)") links the review to that ticket.

How kluster detects the ticket depends on your tool:

| Tool | How the ticket is detected |
|------|---------------------------|
| Cursor, VS Code, Windsurf, JetBrains, Antigravity | Branch name is detected automatically — check out a branch like `feat/KAN-2` and kluster picks it up. |
| Claude Code, Codex CLI | Branch is not detected automatically — include the ticket ID in your prompt or paste the ticket link. |

!!! note "When Jira context is not included"
    If your branch has a generic name like `main` or `develop` and the ticket ID is not mentioned anywhere in the prompt, kluster does not include Jira context in the review. To ensure ticket requirements are checked, reference the ticket ID explicitly in the branch name or in the prompt.

Once kluster starts a code review process, it will check the intent of the Jira ticket associated with the request. It will then suggest the intent of the Jira ticket to the AI tool being used, so that it is automatically applied.

## Example workflow

The following example illustrates how kluster uses Jira ticket context to validate code against requirements.

Assume a Jira ticket **KAN-2** specifies the following requirements:

```text
- Output must be formatted as `The PI: {number}`.
- At least two methods of calculating Pi must be implemented.
- The script must accept command-line arguments to select the algorithm.
```

A developer creates a branch named `feat/KAN-2` and asks their AI assistant (Claude in this example) to "write code that returns pi in Python." 

<div data-termynal>
  <span data-ty>╭─── Claude Code v2.1.63 ────────────────────────────╮</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│               Welcome back kluster.ai!             │</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│                     ▐▛███▜▌                        │</span>
  <span data-ty>│                    ▝▜█████▛▘                       │</span>
  <span data-ty>│                      ▘▘ ▝▝                         │</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│  Opus 4.6 · Claude Max · kluster's Organization    │</span>
  <span data-ty>│                      /workspace                    │</span>
  <span data-ty>╰────────────────────────────────────────────────────╯</span>
  <span data-ty></span>
  <span data-ty="input" data-ty-prompt="❯ "> Create a Python script that prints Pi (Ticket KAN-2)</span>
  <span data-ty></span>
  <span data-ty>● I'll create a simple Python script that prints Pi.</span>
  <span data-ty></span>
  <span data-ty>  ⎿  Write(print_pi.py)</span>
</div>
The AI generates a basic script that prints Pi using a single method.

Because kluster has access to the Jira ticket, it compares the generated code against the ticket requirements and flags the following gaps:

- The output format does not match `The PI: {number}`.
- Only one calculation method is implemented instead of two.
- No argument parsing is included.

kluster then asks the developer whether to fix the code to comply with the Jira ticket requirements. This prevents under-implemented features from being committed without review.

<div data-termynal>
  <span data-ty>╭─── Claude Code v2.1.63 ────────────────────────────╮</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│               Welcome back kluster.ai!             │</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│                     ▐▛███▜▌                        │</span>
  <span data-ty>│                    ▝▜█████▛▘                       │</span>
  <span data-ty>│                      ▘▘ ▝▝                         │</span>
  <span data-ty>│                                                    │</span>
  <span data-ty>│  Opus 4.6 · Claude Max · kluster's Organization    │</span>
  <span data-ty>│                      /workspace                    │</span>
  <span data-ty>╰────────────────────────────────────────────────────╯</span>
  <span data-ty></span>
  <span data-ty>● kluster-verify — kluster_code_review_auto (MCP)</span>
  <span data-ty>  (modified_files_path: "/workspace/print_pi.py")</span>
  <span data-ty></span>
  <span data-ty>  ⎿  {</span>
  <span data-ty>       "isCodeCorrect": false,</span>
  <span data-ty>       "explanation": "Found 1 issue. [HIGH] The script</span>
  <span data-ty>       fails to implement requirements from KAN-2."</span>
  <span data-ty>     }</span>
  <span data-ty></span>
  <span data-ty>⚠️  kluster.ai clarification required — The review found</span>
  <span data-ty>  that Jira ticket KAN-2 has specific requirements:</span>
  <span data-ty></span>
  <span data-ty>  1. Output formatted as "The PI: {number}"</span>
  <span data-ty>  2. At least 2 methods of calculating Pi</span>
  <span data-ty>  3. Argument parsing to select the algorithm</span>
  <span data-ty></span>
  <span data-ty>  Would you like me to update the script to meet all</span>
  <span data-ty>  KAN-2 requirements?</span>
  <span data-ty></span>
  <span data-ty="input" data-ty-prompt="❯ "> yes</span>
  <span data-ty></span>
  <span data-ty>● Updating print_pi.py to meet all KAN-2 requirements...</span>
  <span data-ty></span>
  <span data-ty>  ⎿  Write(print_pi.py)</span>
  <span data-ty></span>
  <span data-ty>● kluster-verify — kluster_code_review_auto (MCP)</span>
  <span data-ty>  (modified_files_path: "/workspace/print_pi.py")</span>
  <span data-ty></span>
  <span data-ty>  ⎿  {</span>
  <span data-ty>       "isCodeCorrect": true,</span>
  <span data-ty>       "explanation": "No issues found. Code analysis</span>
  <span data-ty>       complete.",</span>
  <span data-ty>     … +11 lines (ctrl+o to expand)</span>
  <span data-ty>     }</span>
  <span data-ty></span>
  <span data-ty>● Script is updated and passing all checks. It now</span>
  <span data-ty>  includes:</span>
  <span data-ty></span>
  <span data-ty>  - builtin method — uses math.pi</span>
  <span data-ty>  - leibniz method — approximates Pi via Leibniz series</span>
  <span data-ty>  - --method argument to select the algorithm</span>
  <span data-ty>  - Output formatted as The PI: {number}</span>
  <span data-ty></span>
  <span data-ty>  ---</span>
  <span data-ty>  🔍 kluster.ai Review Summary</span>
  <span data-ty></span>
  <span data-ty>  📋 kluster feedback</span>
  <span data-ty></span>
  <span data-ty>  - 1 high-severity issue in initial review: script</span>
  <span data-ty>    didn't meet KAN-2 requirements (missing output format,</span>
  <span data-ty>    multiple methods, and argument parsing).</span>
  <span data-ty>  - Final review: 0 issues — all requirements satisfied.</span>
  <span data-ty>  - 📚 External knowledge used: Jira ticket KAN-2</span>
  <span data-ty></span>
  <span data-ty>  ✅ Issues found and fixed</span>
  <span data-ty></span>
  <span data-ty>  Updated script includes two Pi methods (builtin and</span>
  <span data-ty>  leibniz), argparse for algorithm selection, and</span>
  <span data-ty>  The PI: {number} output format per KAN-2.</span>
  <span data-ty></span>
  <span data-ty>  ⚠️  Impact Assessment: Without these fixes, the script</span>
  <span data-ty>  would not have met the ticket requirements.</span>
</div>
After the AI coding agent finishes the implementation, kluster performs a follow-up review to verify that the code matches the intent from the Jira ticket requirements. If it does, kluster states that no issues were found in the code.

## Next steps

- **[Configuration options](/kluster-mkdocs/code-reviews/configuration/options/)**: Adjust sensitivity, analysis depth, and enabled tools.
- **[Custom rules](/kluster-mkdocs/code-reviews/configuration/rules/)**: Define additional project-specific review standards.
- **[Automatic reviews](/kluster-mkdocs/code-reviews/ide-reviews/ai-generated-code/automatic-reviews/)**: Set up real-time reviews for AI-generated code.
