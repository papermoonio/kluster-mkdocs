"""MkDocs hook to restore breadcrumbs for orphan pages.

Assigns `page.parent` to pages not included in nav,
allowing Material to render native breadcrumbs via `page.ancestors`.

"""

from __future__ import annotations

from typing import Dict

from mkdocs.structure.pages import Page


_PAGE_BY_SRC: Dict[str, Page] = {}


def on_nav(nav, *, config, **kwargs):
    """Index pages that are present in nav by src path."""
    del config, kwargs

    global _PAGE_BY_SRC
    _PAGE_BY_SRC = {}

    for nav_page in getattr(nav, "pages", []):
        src_uri = _normalize_page_src(nav_page)
        if src_uri:
            _PAGE_BY_SRC[src_uri] = nav_page

    return nav


def on_page_context(context, page, *, config, nav, **kwargs):
    """Assign a nav parent for orphan pages so native breadcrumbs can render."""
    del config, nav, kwargs

    src_uri = _normalize_page_src(page)
    if not src_uri:
        return context

    if src_uri in _PAGE_BY_SRC:
        return context

    parent_src = _resolve_parent_src(src_uri)
    parent_page = _PAGE_BY_SRC.get(parent_src)
    if parent_page:
        page.parent = parent_page

    return context


def _normalize_page_src(page: Page | None) -> str:
    if not page or not getattr(page, "file", None):
        return ""

    src = getattr(page.file, "src_uri", None) or getattr(page.file, "src_path", "")
    return str(src).replace("\\", "/")


def _resolve_parent_src(src_uri: str) -> str:
    """Find nearest parent landing page present in nav."""
    if not src_uri or "/" not in src_uri:
        return ""

    current_dir = src_uri.rsplit("/", 1)[0]

    while current_dir:
        for candidate in (f"{current_dir}.md", f"{current_dir}/index.md"):
            if candidate != src_uri and candidate in _PAGE_BY_SRC:
                return candidate

        if "/" not in current_dir:
            break
        current_dir = current_dir.rsplit("/", 1)[0]

    return ""
