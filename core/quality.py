"""Automatic quality gate.

Runs on every article before it is published. If anything fails, the article
is saved to _drafts/ (not published) and the bot moves on to the next item.
This is what replaces manual review.
"""
import re
from datetime import datetime

from .textutil import html_to_text

BANNED_PHRASES = [
    "as an ai", "as a language model", "i cannot", "i can't", "i'm unable",
    "lorem ipsum", "[insert", "[your", "[source", "placeholder",
]

RISKY_HEALTH_CLAIMS = re.compile(
    r"\b(cures?|cured|miracle|guaranteed?|100% safe|no side effects|doctors hate)\b", re.I
)

_NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def _numbers(text):
    return {m.replace(",", "").rstrip(".") for m in _NUMBER.findall(text)}


def unsupported_numbers(article_text, source_text):
    """Numbers with 3+ digits that appear in the article but nowhere in the source."""
    known = _numbers(source_text)
    year = datetime.now().year
    allowed_years = {str(year), str(year + 1)}
    bad = []
    for number in sorted(_numbers(article_text)):
        digits = number.replace(".", "")
        if len(digits) < 3 or number in known or number in allowed_years:
            continue
        bad.append(number)
    return bad


def check(niche, article_html, source_text, title):
    """Return (ok, reasons)."""
    reasons = []
    text = html_to_text(article_html)
    low = text.lower()

    words = len(text.split())
    if words < niche.min_words:
        reasons.append(f"too short ({words} words, need {niche.min_words})")
    if not re.search(r"<(p|li)\b", article_html, re.I):
        reasons.append("no paragraphs or list items")

    for phrase in BANNED_PHRASES:
        if phrase in low:
            reasons.append(f"contains '{phrase}'")
    if "**" in article_html or re.search(r"(?m)^\s*#{1,3}\s", article_html):
        reasons.append("leftover markdown")
    if low.count("not specified") > 6:
        reasons.append("too many 'not specified' (source too thin)")

    if niche.name == "health" and RISKY_HEALTH_CLAIMS.search(text):
        reasons.append("risky health claim wording")

    if niche.verify_numbers:
        bad = unsupported_numbers(text, source_text + " " + title)
        if bad:
            reasons.append("numbers not found in source: " + ", ".join(bad[:6]))

    return (not reasons), reasons


def check_title(niche, seo_title, source_text, original_title):
    """Check an AI-written, search-style title. Returns (ok, reasons).
    If this fails the pipeline simply keeps the original headline, so a bad
    title never blocks an otherwise good article."""
    reasons = []
    t = (seo_title or "").strip()
    if not 25 <= len(t) <= 75:
        reasons.append(f"title length {len(t)} (need 25-75)")
    low = t.lower()
    for phrase in BANNED_PHRASES:
        if phrase in low:
            reasons.append(f"title contains '{phrase}'")
    if re.search(r"[<>\[\]{}*#]|https?://", t):
        reasons.append("title contains markup or a link")
    bad = unsupported_numbers(t, source_text + " " + original_title)
    if bad:
        reasons.append("title numbers not found in source: " + ", ".join(bad[:4]))
    return (not reasons), reasons