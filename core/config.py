"""Central settings for all Trendify bots.

Importing this module also moves the working directory to the repo root,
so every relative path in the project (jobs/, data/, jobs.html ...) works
no matter where the script is started from.
"""
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
os.chdir(REPO_ROOT)

# ---------------------------------------------------------------- site
SITE_URL = (os.environ.get("SITE_URL") or "https://beflaz.com").rstrip("/")
SITE_NAME = "Beflaz"
TELEGRAM_CHANNEL = os.environ.get("TELEGRAM_CHANNEL") or "@trendify_news_live"

# ---------------------------------------------------------------- SEO / indexing
# A logo file you upload yourself (recommended: square, at least 112x112px,
# PNG) - used in the NewsArticle/Article structured data on every page.
SITE_LOGO_URL = os.environ.get("SITE_LOGO_URL") or f"{SITE_URL}/logo.png"

# IndexNow key: Bing/Yandex/Naver/Seznam/Yep use this to confirm you own the
# site. Set your own via the GitHub secret INDEXNOW_KEY, and create a file
# at the repo root named "<that key>.txt" containing just the key itself.
# Google does NOT participate in IndexNow (confirmed current as of 2026) -
# this speeds up the other engines, not Google; sitemap.xml + Search
# Console remain what matters for Google specifically.
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY") or ""

# ---------------------------------------------------------------- AI
# Same model name you already use. Change it in one place (or via the
# GEMINI_MODEL environment variable) and all six bots follow.
MODEL_NAME = os.environ.get("GEMINI_MODEL") or "gemini-3.6-flash"


def gemini_keys():
    """Paid key first (if you add GEMINI_API_KEY later), then your 5 old keys."""
    names = ["GEMINI_API_KEY"] + [f"GEMINI_KEY_{i}" for i in range(1, 6)]
    keys = []
    for name in names:
        value = (os.environ.get(name) or "").strip()
        if value and value not in keys:
            keys.append(value)
    return keys


# ---------------------------------------------------------------- email / telegram
GMAIL_SENDER = os.environ.get("GMAIL_SENDER") or ""
GMAIL_RECEIVER = os.environ.get("GMAIL_RECEIVER") or GMAIL_SENDER
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD") or ""
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN") or ""

# ---------------------------------------------------------------- images
# Pexels is tried first (free tier: 200 requests/hour, 20,000/month - a
# signup gives you a key instantly, no review wait). Unsplash is the
# backup (free tier is a much tighter 50 requests/hour).
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY") or ""
UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY") or ""
# When True (the default): use the publisher's own share-image (og:image)
# from the real article page, with a credit line linking back to them.
# This is the same "hotlink + credit" approach most news aggregators use,
# but it is still their image, not a license to it - it carries some
# copyright risk. Set the GitHub secret USE_SOURCE_IMAGES=false to turn
# this off and fall back to Unsplash / AI-generated images only.
USE_SOURCE_IMAGES = (os.environ.get("USE_SOURCE_IMAGES") or "true").lower() in ("1", "true", "yes")

# ---------------------------------------------------------------- scraping behaviour
USER_AGENT = f"Mozilla/5.0 (compatible; TrendifyBot/1.0; +{SITE_URL})"
ROBOTS_TOKEN = "TrendifyBot"
REQUEST_TIMEOUT = 15
ITEMS_PER_FEED = 5          # how many top entries of each feed to look at
MAX_TRIES_PER_RUN = 8       # max candidates one bot examines per run
SOURCE_TEXT_LIMIT = 6000    # characters of source text passed to the AI

# ---------------------------------------------------------------- files
SEEN_FILE = "data/seen.json"
SEEN_LIMIT = 6000           # remember the last N items
FEEDS_DIR = "data/feeds"
DRAFTS_DIR = "_drafts"      # folders starting with "_" are not published by Jekyll
LOG_FILE = "logs/system.log"
DASHBOARD_FILE = "system-logs.html"
SITEMAP_FILE = "sitemap.xml"
RSS_MAX_ITEMS = 20          # items shown in each niche's own rss_<niche>.xml
HUB_MAX_ITEMS = 60          # items remembered per niche (used by the evergreen hub pages)

# Combined feeds across ALL niches, for tools (dlvr.it, IFTTT) that need one
# feed to post everything to a single social account (e.g. one Instagram page
# covering Jobs + News + Scholarships + ...).
MASTER_RSS_FILE = "rss.xml"
INSTAGRAM_RSS_FILE = "rss_instagram.xml"
MASTER_RSS_MAX_ITEMS = 40
