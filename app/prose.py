"""Tekst članka u HTML.

Ceo tekst se prvo escape-uje, pa korisnik ne može da ubaci svoj HTML.
Prazan red deli pasuse, `ovako` je kod u rečenici, a blok koda ide
između dve linije sa ```.
"""
import re

from markupsafe import Markup, escape

_INLINE = re.compile(r"`([^`\n]+)`")


def _inline(text):
    return _INLINE.sub(r"<code>\1</code>", str(escape(text)))


def render_prose(content):
    html = []
    for block in re.split(r"\n\s*\n", (content or "").replace("\r\n", "\n").strip()):
        lines = block.split("\n")
        if len(lines) >= 2 and lines[0].strip() == "```" and lines[-1].strip() == "```":
            html.append(f"<pre><code>{escape(chr(10).join(lines[1:-1]))}</code></pre>")
        elif block.strip():
            html.append("<p>" + "<br>".join(_inline(line) for line in lines) + "</p>")
    return Markup("\n".join(html))

