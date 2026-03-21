"""MkDocs hook to restore breadcrumbs for orphan pages.

Assigns `page.parent` to pages not included in nav,
allowing Material to render native breadcrumbs via `page.ancestors`.
If `page.ancestors`is empty use `page.url` to create the path.

"""

from __future__ import annotations

from typing import Dict
from typing import Optional

from mkdocs.structure.nav import Link
from mkdocs.structure.pages import Page


_PAGE_BY_SRC: Dict[str, Page] = {}


def on_nav(nav, *, config, **kwargs):
    """Index nav pages by source path."""
    del config, kwargs

    global _PAGE_BY_SRC
    _PAGE_BY_SRC = {}

    for nav_page in getattr(nav, "pages", []):
        src_uri = _normalize_page_src(nav_page)
        if src_uri:
            _PAGE_BY_SRC[src_uri] = nav_page

    return nav


def on_page_context(context, page, *, config, nav, **kwargs):
    """Assign a parent chain for orphan pages so native breadcrumbs can render."""
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

    page_url = _normalize_page_url(getattr(page, "url", ""))
    synthetic_parent = _build_synthetic_parent(src_uri, page_url)
    if synthetic_parent:
        page.parent = synthetic_parent

    return context


def _normalize_page_src(page: Page | None) -> str:
    if not page or not getattr(page, "file", None):
        return ""

    src = getattr(page.file, "src_uri", None) or getattr(page.file, "src_path", "")
    return _normalize_src(src)


def _normalize_src(src: str) -> str:
    return str(src).replace("\\", "/").lstrip("/")


def _normalize_page_url(page_url: str) -> str:
    url = str(page_url or "").strip()
    if not url:
        return ""
    url = "/" + url.lstrip("/")
    if not url.endswith("/"):
        url += "/"
    return url


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


def _build_synthetic_parent(src_uri: str, page_url: str):
    page_dir = _src_dir(src_uri)
    if not page_dir:
        return None

    anchor_dir, anchor_page = _find_anchor(page_dir)
    if not anchor_page:
        return None

    anchor_node = _resolve_anchor_node(anchor_dir, anchor_page)
    if not anchor_node:
        return None

    missing_dirs = _missing_dirs(anchor_dir, page_dir)
    if not missing_dirs:
        return None

    current_parent = anchor_node
    traversed = anchor_dir
    for rel_dir in missing_dirs:
        full_dir = f"{traversed}/{rel_dir}" if traversed else rel_dir
        url = _url_prefix_for_dir(full_dir, page_url)
        if not url:
            return None

        link = Link(title=_humanize_segment(rel_dir), url=url)
        link.parent = current_parent
        current_parent = link
        traversed = full_dir

    return current_parent


def _find_anchor(page_dir: str) -> tuple[str, Optional[Page]]:
    """Find nearest ancestor directory that has at least one page in nav."""
    current = page_dir
    while current:
        page = _first_nav_page_for_dir(current)
        if page:
            return current, page
        if "/" not in current:
            break
        current = current.rsplit("/", 1)[0]
    return "", None


def _first_nav_page_for_dir(dir_path: str) -> Optional[Page]:
    prefix = f"{dir_path}/"
    candidates = [
        page
        for src, page in _PAGE_BY_SRC.items()
        if src.startswith(prefix) or src in (f"{dir_path}.md", f"{dir_path}/index.md")
    ]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: _normalize_page_src(p))[0]


def _resolve_anchor_node(anchor_dir: str, anchor_page: Page):
    page_src = _normalize_page_src(anchor_page)
    if not page_src:
        return getattr(anchor_page, "parent", None) or anchor_page

    anchor_depth = len(anchor_dir.split("/")) if anchor_dir else 0
    page_depth = len(page_src.split("/"))
    steps_up = max(0, page_depth - anchor_depth)

    chain = [anchor_page, *anchor_page.ancestors]
    if not chain:
        return None

    index = min(steps_up, len(chain) - 1)
    return chain[index]


def _missing_dirs(anchor_dir: str, page_dir: str) -> list[str]:
    page_parts = page_dir.split("/") if page_dir else []
    anchor_parts = anchor_dir.split("/") if anchor_dir else []
    return page_parts[len(anchor_parts) :]


def _url_prefix_for_dir(dir_path: str, page_url: str) -> str:
    """Build directory URL from the current orphan page URL."""
    if not page_url:
        return ""

    dir_parts = [p for p in dir_path.split("/") if p]
    page_parts = _url_segments(page_url)
    if not dir_parts:
        return "/"
    if len(page_parts) < len(dir_parts):
        return ""
    if page_parts[: len(dir_parts)] != dir_parts:
        return ""

    return "/" + "/".join(dir_parts) + "/"


def _url_segments(url_path: str) -> list[str]:
    return [segment for segment in str(url_path).strip("/").split("/") if segment]


def _humanize_segment(segment: str) -> str:
    cleaned = segment.replace("-", " ").replace("_", " ").strip()
    return cleaned.title() if cleaned else segment


def _src_dir(src_uri: str) -> str:
    if "/" not in src_uri:
        return ""
    return src_uri.rsplit("/", 1)[0]
