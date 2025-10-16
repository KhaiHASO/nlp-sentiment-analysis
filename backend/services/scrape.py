from typing import List

import httpx
from bs4 import BeautifulSoup


async def fetch_comments_from_url(url: str, css_selector: str = None, limit: int = 50) -> List[str]:
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url)
        r.raise_for_status()
        html = r.text

    soup = BeautifulSoup(html, 'html.parser')
    texts: List[str] = []

    # If user provides a selector, use it; else fallback to common comment-like containers
    selectors = [css_selector] if css_selector else [
        '.comment', '.comments', '.cmt', '.reply', '[data-test="comment"]', '.fbUserContent', 'article'
    ]

    for sel in selectors:
        if not sel:
            continue
        for el in soup.select(sel):
            txt = (el.get_text(separator=' ', strip=True) or '').strip()
            if txt and len(txt.split()) > 2:
                texts.append(txt)
            if len(texts) >= limit:
                return texts

    # Fallback: grab paragraphs
    if not texts:
        for p in soup.find_all('p'):
            txt = (p.get_text(separator=' ', strip=True) or '').strip()
            if txt and len(txt.split()) > 2:
                texts.append(txt)
            if len(texts) >= limit:
                break

    return texts


