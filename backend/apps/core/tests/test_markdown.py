from apps.core.markdown import render_markdown


def test_renders_basic_markdown():
    html = render_markdown("# Title\n\nSome **bold** text.")
    assert "<h1>Title</h1>" in html
    assert "<strong>bold</strong>" in html


def test_tables_render():
    html = render_markdown("| a | b |\n|---|---|\n| 1 | 2 |")
    assert "<table>" in html and "<td>1</td>" in html


def test_raw_html_is_not_rendered():
    html = render_markdown("<script>alert(1)</script>\n\n<b onclick='x()'>hi</b>")
    assert "<script" not in html  # shown as escaped text, never as a tag
    assert "<b " not in html
    assert "&lt;script&gt;" in html


def test_javascript_links_are_removed():
    html = render_markdown("[click](javascript:alert(1))")
    assert "href" not in html


def test_links_get_safe_rel():
    html = render_markdown("[CHIPS](https://hbcuchip.org)")
    assert 'href="https://hbcuchip.org"' in html
    assert "noopener" in html


def test_empty_source():
    assert render_markdown("") == ""
