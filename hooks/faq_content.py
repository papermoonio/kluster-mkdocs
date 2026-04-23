"""MkDocs hook: render FAQ pages as collapsible sections.

Pages opt in with YAML front matter:
  faq: true         -> wrap h2 sections
  faq: categorized  -> keep h2 categories, wrap h3 sections
"""

from __future__ import annotations

import re

from bs4 import BeautifulSoup
from bs4.element import PageElement, Tag


def on_page_content(html, page, *, config, files, **kwargs):
    faq = (getattr(page, "meta", {}) or {}).get("faq")
    if faq is True:
        soup = BeautifulSoup(html, "html.parser")
        return str(_wrap_heading_sections(soup, page.url, "h2"))
    if isinstance(faq, str) and faq.lower() == "categorized":
        soup = BeautifulSoup(html, "html.parser")
        return _wrap_categorized_sections(soup, page.url)
    return html


def _wrap_categorized_sections(soup: BeautifulSoup, page_url: str) -> str:
    output = BeautifulSoup("", "html.parser")
    category_count = 0

    for section in _split_sections(list(soup.contents), "h2"):
        if section.heading is None:
            _append_all(output, section.nodes)
            continue

        category_count += 1
        output.append(section.heading)
        faq_fragment = _wrap_heading_sections(
            soup,
            page_url,
            "h3",
            nodes=section.content,
            id_prefix=str(category_count),
        )
        _append_all(output, list(faq_fragment.contents))

    return str(output)


def _wrap_heading_sections(
    soup: BeautifulSoup,
    page_url: str,
    heading_name: str,
    *,
    nodes: list[PageElement] | None = None,
    id_prefix: str | None = None,
) -> BeautifulSoup:
    output = BeautifulSoup("", "html.parser")
    item_count = 0

    source_nodes = list(soup.contents) if nodes is None else nodes

    for section in _split_sections(source_nodes, heading_name):
        if section.heading is None:
            _append_all(output, section.nodes)
            continue

        item_count += 1
        details_id = _details_id(page_url, id_prefix, str(item_count))
        details = soup.new_tag(
            "details",
            attrs={"class": ["interface", "faq"], "id": details_id},
        )
        summary = soup.new_tag("summary")
        summary.append(section.heading)
        details.append(summary)
        _append_all(details, section.content)
        output.append(details)

    return output


class _Section:
    def __init__(self, heading: Tag | None, nodes: list[PageElement]) -> None:
        self.heading = heading
        self.nodes = nodes
        self.content = nodes[1:] if heading is not None else nodes


def _split_sections(nodes: list[PageElement], heading_name: str) -> list[_Section]:
    sections: list[_Section] = []
    current: list[PageElement] = []
    heading: Tag | None = None

    for node in nodes:
        if _is_heading(node, heading_name):
            if current:
                sections.append(_Section(heading, current))
            heading = node
            current = [node]
            continue
        current.append(node)

    if current:
        sections.append(_Section(heading, current))

    return sections


def _is_heading(node: PageElement, heading_name: str) -> bool:
    return isinstance(node, Tag) and node.name == heading_name


def _append_all(parent: Tag | BeautifulSoup, nodes: list[PageElement]) -> None:
    for node in nodes:
        parent.append(node)


def _details_id(page_url: str, *parts: str | None) -> str:
    raw = "-".join(["faq", page_url, *(part for part in parts if part)])
    return re.sub(r"-+", "-", re.sub(r"[/?#.\s]+", "-", raw)).strip("-")
