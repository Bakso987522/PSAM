import html
import re

import httpx

from importer.parsers import norm

ATTACHMENT = re.compile(
    r'href="(/attachment/[0-9a-f-]+)"[^>]*?aria-label="\s*Pobierz plik (.*?)\n',
    re.DOTALL,
)
LABEL_DATE = re.compile(r"et (\d\d)-(\d\d)-(\d{4})")
USE_SUFFIX = re.compile(r"\s+zast\.?\s*(nie)?prof\.?$")


def label_index(client: httpx.Client, pages: set[str]) -> dict[str, str]:
    best = {}
    for page in sorted(pages):
        resp = client.get(page, follow_redirects=True)
        resp.raise_for_status()
        for href, title in ATTACHMENT.findall(resp.text):
            title = norm(html.unescape(title).replace("\u200b", ""))
            if " - " not in title:
                continue
            name, rest = title.rsplit(" - ", 1)
            suffix = USE_SUFFIX.search(name)
            if suffix:
                name = name[:suffix.start()]
            m = LABEL_DATE.match(rest)
            priority = (
                (1, m[3] + m[2] + m[1], not (suffix and suffix[1]))
                if m else (0, "", False)
            )
            if name not in best or priority > best[name][0]:
                best[name] = (priority, "https://www.gov.pl" + href)
    return {name: url for name, (_, url) in best.items()}