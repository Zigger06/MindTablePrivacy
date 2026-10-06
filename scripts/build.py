#!/usr/bin/env python3
"""Build crawlable, no-JavaScript-required policy pages with Python's standard library."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://zigger06.github.io/MindTablePrivacy/"
PATHS = {"ru": "", "en": "en/", "tg": "tg/"}
LANGUAGES = {"ru": "РУС", "en": "ENG", "tg": "ТОҶ"}
ICONS = [
    '<path d="M8 11V8a4 4 0 0 1 8 0v3M6 11h12v9H6z"/>',
    '<path d="M2 8a15 15 0 0 1 20 0M5 12a10 10 0 0 1 14 0M8 16a5 5 0 0 1 8 0"/><circle cx="12" cy="20" r=".5"/>',
    '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6zM8 12l3 3 5-6"/>',
]


def esc(value):
    return html.escape(value, quote=True)


def render(lang, data):
    prefix = "" if lang == "ru" else "../"
    language_nav = "".join(
        f'<a href="{prefix}{PATHS[code]}index.html" lang="{code}" hreflang="{code}"'
        f'{" aria-current=\"page\"" if code == lang else ""}>{label}</a>'
        for code, label in LANGUAGES.items()
    )
    # Policy HTML is authored in this repository, never interpolated from visitor input.
    toc = "".join(
        f'<li><a href="#{esc(section["id"])}"><span class="toc-number">{i:02}</span>'
        f'<span>{esc(section["title"])}</span></a></li>'
        for i, section in enumerate(data["sections"], 1)
    )
    sections = "".join(
        f'<section class="policy-section" id="{esc(section["id"])}" aria-labelledby="heading-{esc(section["id"])}">'
        f'<div class="section-heading"><span class="section-number" aria-hidden="true">{i:02}</span>'
        f'<h2 id="heading-{esc(section["id"])}">{esc(section["title"])}</h2></div>'
        f'{section["body"]}</section>'
        for i, section in enumerate(data["sections"], 1)
    )
    summaries = "".join(
        f'<div class="summary-item"><span class="summary-icon" aria-hidden="true">'
        f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[i]}</svg></span>'
        f'<h2>{esc(card["title"])}</h2><p>{esc(card["text"])}</p></div>'
        for i, card in enumerate(data["summary"])
    )
    alternates = "".join(f'<link rel="alternate" hreflang="{code}" href="{BASE}{path}">\n' for code, path in PATHS.items())
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{esc(data['description'])}">
  <meta name="theme-color" content="#0a2032">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'none'; object-src 'none'; base-uri 'self'; form-action 'none'">
  <title>{esc(data['title'])} — MindTable</title>
  <link rel="canonical" href="{BASE}{PATHS[lang]}">
  {alternates}<link rel="alternate" hreflang="x-default" href="{BASE}en/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(data['title'])} — MindTable">
  <meta property="og:description" content="{esc(data['description'])}">
  <meta property="og:url" content="{BASE}{PATHS[lang]}">
  <link rel="icon" type="image/svg+xml" href="{prefix}assets/mark.svg">
  <link rel="stylesheet" href="{prefix}assets/style.css">
  <script src="{prefix}assets/site.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#policy">{esc(data['skip'])}</a>
  <header class="site-header">
    <div class="container header-row">
      <a class="brand" href="{prefix}index.html" aria-label="MindTable"><img src="{prefix}assets/mark.svg" width="40" height="40" alt="">MINDTABLE</a>
      <nav class="language-nav" aria-label="{esc(data['language_label'])}">{language_nav}</nav>
    </div>
  </header>
  <main id="main">
    <div class="hero">
      <div class="container hero-grid">
        <div><p class="eyebrow">{esc(data['eyebrow'])}</p><h1>{esc(data['title'])}</h1><p class="hero-description">{esc(data['description'])}</p></div>
        <div class="document-meta"><p><span class="meta-label">{esc(data['effective_label'])}</span><time class="meta-date" datetime="2026-10-06">{esc(data['date'])}</time></p><p class="meta-version">{esc(data['version'])}</p></div>
      </div>
    </div>
    <div class="container overview" aria-label="{esc(data['summary_label'])}"><div class="summary-grid">{summaries}</div></div>
    <div class="container document-layout">
      <aside class="sidebar">
        <nav aria-labelledby="toc-label"><p class="toc-heading" id="toc-label">{esc(data['toc_label'])}</p><ol class="toc">{toc}</ol></nav>
        <div class="sidebar-actions"><button class="outline-button" type="button" data-print hidden>{esc(data['print'])}</button><a class="outline-button" href="#contact">{esc(data['contact_button'])}</a></div>
      </aside>
      <article class="policy-document" id="policy" aria-label="{esc(data['title'])}">
        <p class="document-intro">{data['intro']}</p>
        {sections}
      </article>
    </div>
  </main>
  <footer class="site-footer"><div class="container footer-row"><p>© 2026 MindTable · Zigger06</p><p>{esc(data['footer'])} · <a href="https://github.com/Zigger06/MindTablePrivacy">{esc(data['history'])}</a></p></div></footer>
</body>
</html>
'''


def main():
    content = json.loads((ROOT / "content/policy.json").read_text(encoding="utf-8"))
    expected_ids = None
    for lang in PATHS:
        data = content[lang]
        ids = [section["id"] for section in data["sections"]]
        assert len(ids) == len(set(ids)) == 14, "Each language must contain 14 unique policy sections."
        expected_ids = expected_ids or ids
        assert ids == expected_ids, "Translated policies must retain matching sections."
        target = ROOT / PATHS[lang] / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(lang, data), encoding="utf-8")
        print(f"Built {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
