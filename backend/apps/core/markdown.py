"""Markdown rendering for author content, announcements and comments.

All user-authored markdown goes through ``render_markdown``: markdown-it renders
it (raw HTML disabled) and nh3 strips anything outside the allow-list, so a
package or announcement can never inject script into a student's page.
"""

import nh3
from markdown_it import MarkdownIt

_md = MarkdownIt("commonmark", {"html": False, "linkify": False, "typographer": True}).enable(
    ["table", "strikethrough"]
)

ALLOWED_TAGS = {
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "code",
    "del",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "sub",
    "sup",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
}
ALLOWED_ATTRIBUTES = {
    "a": {"href", "title"},
    "img": {"src", "alt", "title", "width", "height"},
    "code": {"class"},
    "th": {"align"},
    "td": {"align"},
}
URL_SCHEMES = {"http", "https", "mailto"}


def sanitize_html(html: str) -> str:
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        url_schemes=URL_SCHEMES,
        link_rel="noopener noreferrer nofollow",
    )


def render_markdown(source: str) -> str:
    """Render markdown to safe HTML."""
    return sanitize_html(_md.render(source or ""))
