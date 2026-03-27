---
title: Repo Reviews from CLI
description: Trigger and monitor system-wide repo reviews from your terminal using kluster-cli, with a terminal-first workflow for codebase analysis.
categories:
- Repo Reviews
- CLI
url: https://docs.kluster.ai/code-reviews/cli/repo-reviews/
word_count: 524
token_estimate: 1022
version_hash: sha256:241cb460a028341382713086e4f0e2d69defc4f1469be4f724cdc4967cef3394
last_updated: '2026-03-27T17:26:06+00:00'
---

# Repo reviews from CLI

You can trigger and monitor repo reviews directly from `kluster-cli`. This gives you a terminal-first workflow for system-wide analysis without opening the dashboard.

## Prerequisites

Before using repo review commands from CLI, make sure you have:

- **kluster-cli installed and authenticated**: See [CLI quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/).
- **A connected repository**: Connect your repository in the [Repo Reviews dashboard](https://platform.kluster.ai/repo-reviews){target=\_blank}.
- **An open shell in that repository**: Run commands from the repository root.

## Start a repo review

Use this command to start a new repo-wide analysis:

```bash
kluster review repo start
```

<div data-termynal>
  <span data-ty  ="input"> verify-code-demo % kluster review repo start</span>
  <span data-ty>✓ Repo review started for verify-code-demo. You'll receive an email when the analysis is complete.</span>
</div>
The review runs asynchronously. You'll get an email when analysis is complete.

## Check review status and results

Use this command to see the latest review output any time:

```bash
kluster review repo show
```

<div data-termynal>
  <span data-ty  ="input"> verify-code-demo % kluster review repo show</span>
  <span data-ty>→ Last review: Fri, 13 Feb 2026 08:15:12 PST</span>
  <span data-ty></span>
  <span data-ty>#1 HIGH performance</span>
  <span data-ty>Unbounded in-memory storage will lead to memory exhaustion (OOM).</span>
  <span data-ty>at src/endpoints.ts:13,50</span>
  <span data-ty></span>
  <span data-ty>More details</span>
  <span data-ty>  The `reviews` array (src/endpoints.ts, line 13) is used as a global</span>
  <span data-ty>  in-memory store with no size limit, TTL, or eviction policy.</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Set a max size, use an eviction-capable cache, or move data to a</span>
  <span data-ty>  persistent database.</span>
  <span data-ty></span>
  <span data-ty>────────────────────────────────────────────────────────────────────────</span>
  <span data-ty></span>
  <span data-ty>#2 HIGH security</span>
  <span data-ty>Missing CSRF protection on state-changing POST endpoint.</span>
  <span data-ty>at src/endpoints.ts:23-62</span>
  <span data-ty></span>
  <span data-ty>More details</span>
  <span data-ty>  The '/reviews' endpoint accepts state-changing POST requests without</span>
  <span data-ty>  CSRF tokens or equivalent protections.</span>
  <span data-ty></span>
  <span data-ty>Fix</span>
  <span data-ty>  Validate CSRF tokens (or enforce SameSite/custom header protections)</span>
  <span data-ty>  on state-changing requests.</span>
  <span data-ty></span>
  <span data-ty>→ Repo Reviews establish a comprehensive understanding of your codebase,</span>
  <span data-ty>  surfacing risks, inconsistencies, and violations that can only be</span>
  <span data-ty>  detected when analyzing the code as a whole.</span>
</div>
This output shows the last review timestamp and findings grouped by severity and category.

## Next steps

- **[Repo Reviews quickstart](/kluster-mkdocs/code-reviews/repo-reviews/quickstart/)**: Learn the full dashboard workflow and issue actions.
- **[CLI quickstart](/kluster-mkdocs/code-reviews/cli/quickstart/)**: Install and authenticate kluster-cli.
- **[Review modes](/kluster-mkdocs/code-reviews/review-modes/)**: Compare repo reviews with other review workflows.
