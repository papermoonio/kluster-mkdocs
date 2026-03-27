---
title: Custom rules
description: Learn how to define and manage custom code review rules to enforce consistent code quality, using manual rules or learned rules from GitHub repositories.
categories:
- Configuration
url: https://docs.kluster.ai/code-reviews/configuration/rules/
word_count: 315
token_estimate: 523
version_hash: sha256:f56e57a5b2d9e4623bc255dfba5ec223f75af882e367b9bd4639473f40490b17
last_updated: '2026-03-27T17:26:06+00:00'
---

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
