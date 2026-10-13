"""Writes the article page, the category-page card, the RSS feed and the sitemap."""
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape
from xml.sax.saxutils import quoteattr

from . import config, notify
from .niches import NICHES
from .textutil import esc, html_to_text, shorten

CARD_MARKER = "<!-- NEW_CARD_HERE -->"


# ------------------------------------------------------------------ names and urls
def slugify(title):
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return text[:60].strip("-")


def make_filename(title, link):
    """date + readable slug + short hash: unique, safe, and works for Urdu titles too."""
    digest = hashlib.sha1((title + link).encode("utf-8")).hexdigest()[:6]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return f"{date}-{slugify(title) or 'post'}-{digest}.html"


def article_url(niche, filename):
    return f"{config.SITE_URL}/{niche.folder}/{filename}"


# ------------------------------------------------------------------ article page
def _button(niche, source_link, resolved):
    text = niche.button_text if resolved else "🔗 Read the Source Article"
    return (
        '\n<div style="text-align: center; margin-top: 40px; margin-bottom: 20px;">\n'
        f'    <a href="{esc(source_link)}" target="_blank" rel="nofollow noopener noreferrer" '
        'style="background-color: #00ffcc; color: #111; padding: 15px 30px; text-decoration: none; '
        "font-size: 18px; font-weight: bold; border-radius: 8px; display: inline-block; "
        'box-shadow: 0 4px 6px rgba(0,0,0,0.3);">\n'
        f"        {esc(text)}\n    </a>\n</div>\n"
    )


def _footer(niche, source_link, publisher, image_credit):
    date = datetime.now().strftime("%B %d, %Y")
    credit = f" &middot; {image_credit}" if image_credit else ""
    note = (
        '<p style="margin-top: 30px; font-size: 14px; color: #94a3b8;">'
        f'Source: <a href="{esc(source_link)}" target="_blank" rel="nofollow noopener noreferrer">'
        f"{esc(publisher)}</a> &middot; Published {date}{credit}</p>\n"
    )
    if niche.disclaimer:
        note += f'<p style="font-size: 13px; color: #94a3b8;"><em>{esc(niche.disclaimer)}</em></p>\n'
    return note


def build_article(niche, title, body_html, image_url, image_credit, source):
    """Write the article file. Returns (filename, public_url)."""
    filename = make_filename(title, source.link)
    folder = Path(niche.folder)
    folder.mkdir(parents=True, exist_ok=True)

    template = Path("article_template.html").read_text(encoding="utf-8")
    content = (
        body_html
        + _button(niche, source.link, source.resolved)
        + _footer(niche, source.link, source.publisher, image_credit)
    )
    page = (
        template.replace("{{TITLE}}", esc(title))
        .replace("{{IMAGE_URL}}", esc(image_url))
        .replace("{{CURRENT_TIME}}", datetime.now().strftime("%B %d, %Y"))
        .replace("{{AI_CONTENT}}", content)
    )
    (folder / filename).write_text(page, encoding="utf-8")
    return filename, article_url(niche, filename)


# ------------------------------------------------------------------ category page card
def add_card(niche, title, image_url, filename, body_html):
    page = Path(niche.page)
    if not page.exists():
        notify.log(niche.label, "WARN", f"{niche.page} not found - card not added")
        return False
    content = page.read_text(encoding="utf-8")
    if CARD_MARKER not in content:
        notify.log(niche.label, "WARN", f"{CARD_MARKER} not found in {niche.page} - card not added")
        return False
    hook = shorten(html_to_text(body_html), 130)
    card = (
        f"{CARD_MARKER}\n"
        f'        <div class="news-card">\n'
        f'            <img src="{esc(image_url)}" alt="{esc(title)}" loading="lazy">\n'
        f"            <h3>{esc(title)}</h3>\n"
        f"            <p>{esc(hook)}</p>\n"
        f'            <a href="{niche.folder}/{filename}" class="read-more">{esc(niche.card_button)}</a>\n'
        f"        </div>"
    )
    page.write_text(content.replace(CARD_MARKER, card, 1), encoding="utf-8")
    return True


# ------------------------------------------------------------------ RSS (last 20 items)
def _rss_item_xml(item):
    return (
        "  <item>\n"
        f"    <title>{xml_escape(item['title'])}</title>\n"
        f"    <description>{xml_escape(item['caption'])}</description>\n"
        f"    <link>{xml_escape(item['url'])}</link>\n"
        f"    <guid isPermaLink=\"true\">{xml_escape(item['url'])}</guid>\n"
        f"    <pubDate>{item['date']}</pubDate>\n"
        f"    <enclosure url={quoteattr(item['image'])} type=\"image/jpeg\" length=\"0\" />\n"
        "  </item>\n"
    )


def _write_rss_file(path, title, link, description, items):
    entries = "".join(_rss_item_xml(i) for i in items)
    xml = (
        '<?xml version="1.0" encoding="UTF-8" ?>\n<rss version="2.0">\n<channel>\n'
        f"  <title>{xml_escape(title)}</title>\n"
        f"  <link>{xml_escape(link)}</link>\n"
        f"  <description>{xml_escape(description)}</description>\n"
        f"{entries}</channel>\n</rss>\n"
    )
    Path(path).write_text(xml, encoding="utf-8")


def _niche_feed_path(niche_name):
    return Path(config.FEEDS_DIR) / f"{niche_name}.json"


def _read_feed_store(path):
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return []


def update_rss(niche, title, url, image_url):
    """Update this niche's own rss_<niche>.xml (last RSS_MAX_ITEMS items)."""
    store = _niche_feed_path(niche.name)
    store.parent.mkdir(parents=True, exist_ok=True)
    items = _read_feed_store(store)
    caption = f"{niche.emoji} {niche.rss_heading}: {title}\n\n🔗 Read full details at the Link in our Bio! 👇\n{url}"
    items.insert(0, {
        "title": title, "url": url, "image": image_url, "caption": caption,
        "date": format_datetime(datetime.now(timezone.utc), usegmt=True),
    })
    items = items[: config.RSS_MAX_ITEMS]
    store.write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    _write_rss_file(niche.rss_file, niche.rss_title, f"{config.SITE_URL}/", niche.rss_description, items)


def update_master_feeds():
    """Combine the latest items across EVERY niche into two feeds that carry
    everything at once: rss.xml (a general 'everything' feed, e.g. for an X
    auto-poster) and rss_instagram.xml (same items, for dlvr.it/IFTTT-style
    tools that post images to one Instagram account for the whole site).
    Reads the same per-niche stores update_rss() already writes, so this
    never re-scans HTML files and costs no extra AI or network calls.
    """
    all_items = []
    for niche in NICHES.values():
        all_items.extend(_read_feed_store(_niche_feed_path(niche.name)))

    def _sort_key(item):
        try:
            return parsedate_to_datetime(item["date"])
        except Exception:
            return datetime.min.replace(tzinfo=timezone.utc)

    all_items.sort(key=_sort_key, reverse=True)
    all_items = all_items[: config.MASTER_RSS_MAX_ITEMS]

    _write_rss_file(
        config.MASTER_RSS_FILE, f"{config.SITE_NAME} - Everything",
        f"{config.SITE_URL}/", "Latest updates from every category", all_items,
    )
    _write_rss_file(
        config.INSTAGRAM_RSS_FILE, f"{config.SITE_NAME} - Instagram Feed",
        f"{config.SITE_URL}/", "Latest updates with images, for Instagram auto-posting", all_items,
    )


# ------------------------------------------------------------------ sitemap
def update_sitemap():
    urls = [f"{config.SITE_URL}/"]
    for niche in NICHES.values():
        if Path(niche.page).exists():
            urls.append(f"{config.SITE_URL}/{niche.page}")
        for f in sorted(Path(niche.folder).glob("*.html")):
            urls.append(f"{config.SITE_URL}/{niche.folder}/{f.name}")
    body = "".join(f"  <url><loc>{xml_escape(u)}</loc></url>\n" for u in urls)
    Path(config.SITEMAP_FILE).write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "</urlset>\n",
        encoding="utf-8",
    )