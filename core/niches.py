"""One entry per niche. To add a 7th niche, add one more Niche(...) below
and copy one of the files in scripts/. No other code needs to change.

Feeds are checked in order, top to bottom (first = highest priority).

Feeds use Bing News search instead of Google News search. Google News wraps
every link through a redirect that needs a decode step, and that decode
step is frequently blocked from shared cloud IPs (GitHub Actions included).
Bing News gives the real publisher link directly, so no decode step is
needed and articles stop being skipped as "too thin".
"""
from dataclasses import dataclass
from urllib.parse import quote


def bing_news(query, freshness="week", market="en-US"):
    """Build a Bing News RSS search URL. freshness: 'day', 'week' or None."""
    codes = {"day": '"7"', "week": '"8"'}
    url = f"https://www.bing.com/news/search?q={quote(query)}&format=RSS&mkt={market}"
    if freshness in codes:
        url += f"&qft=interval%3d{codes[freshness]}"
    return url


@dataclass(frozen=True)
class Niche:
    name: str               # short id, used in file names: jobs, news ...
    label: str              # shown on the dashboard: JOBS, NEWS ...
    emoji: str
    folder: str             # where article pages are saved
    page: str               # category page that receives the new card
    rss_file: str
    legacy_file: str        # your old posted_*.txt (imported once)
    feeds: list
    role: str               # who the AI pretends to be
    instructions: str       # niche-specific writing rules
    image_style: str        # style words for AI-generated fallback images
    image_query: str        # search words for Unsplash
    button_text: str        # button under the article
    card_button: str        # button text on the category-page card
    telegram_heading: str
    rss_heading: str
    rss_title: str
    rss_description: str
    disclaimer: str = ""
    image_from_title: bool = True   # False = generic image (no names from headline)
    verify_numbers: bool = True     # reject articles with numbers not found in the source
    min_source_chars: int = 400     # skip items whose source text is thinner than this
    min_words: int = 150
    max_words: int = 400
    risk: str = "normal"            # "high" = stricter niche (jobs, scholarships, health)
    schema_type: str = "Article"    # Default schema type for SEO


JOBS = Niche(
    name="jobs", label="JOBS", emoji="💼",
    folder="jobs", page="jobs.html", rss_file="rss_jobs.xml", legacy_file="posted_jobs.txt",
    feeds=[
        # Pakistan govt and high demand
        bing_news("government jobs pakistan", "day"),
        bing_news("fpsc jobs pakistan", "day"),
        bing_news("pakistan army jobs", "day"),
        bing_news("wapda jobs pakistan", "day"),
        bing_news("nadra jobs pakistan", "day"),
        # Pakistan provincial and general
        bing_news("ppsc jobs lahore"),
        bing_news("spsc jobs sindh"),
        bing_news("private jobs pakistan"),
        bing_news("banking jobs pakistan"),
        bing_news("it jobs pakistan"),
        # International and remote
        bing_news("jobs in usa visa sponsorship", "day"),
        bing_news("tier 2 visa jobs uk", "day"),
        bing_news("lmia jobs canada", "day"),
        bing_news("remote software engineer jobs"),
        bing_news("jobs in dubai uae", "day"),
    ],
    role="an expert career consultant who writes accurate, easy-to-read job alerts",
    instructions=(
        "Use headings such as 'Role Overview', 'Eligibility Criteria', 'Key Details' and "
        "'How to Apply'. Only list eligibility, salary, deadline, location or number of posts "
        "if the SOURCE states them. A friendly, encouraging tone is fine, but stay factual."
    ),
    image_style="professional corporate office workplace realistic photography",
    image_query="office workplace professional",
    button_text="💼 Click Here to Apply (Official Website)",
    card_button="View Job Details",
    telegram_heading="NEW JOB OPPORTUNITY",
    rss_heading="New Job Alert",
    rss_title="Trendify Portal - Jobs",
    rss_description="Latest Government, Private & International Jobs",
    disclaimer="Always confirm deadlines and requirements on the official notice before applying.",
    min_source_chars=400, risk="high",
)

NEWS = Niche(
    name="news", label="NEWS", emoji="📰",
    folder="news", page="news.html", rss_file="rss_news.xml", legacy_file="posted_news.txt",
    feeds=[
        "https://www.dawn.com/feeds/home",
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        bing_news("pakistan breaking news", "day"),
    ],
    role="a careful news editor who summarises reports accurately and neutrally",
    instructions=(
        "Write a neutral news summary in your own words. Attribute claims to the publisher "
        "(for example 'according to Dawn'). Use headings such as 'What happened', 'Key facts' "
        "and 'Why it matters'. Do not add opinions or predictions."
    ),
    image_style="modern newsroom broadcast studio, abstract world news illustration, no text, no faces",
    image_query="newspaper press abstract",
    button_text="📰 Read the Original Report",
    card_button="Read Full Story",
    telegram_heading="BREAKING NEWS",
    rss_heading="Latest News",
    rss_title="Trendify Portal - News",
    rss_description="Pakistani and global news",
    image_from_title=False, min_source_chars=400,
)

DRAMAS = Niche(
    name="dramas", label="DRAMAS", emoji="🎭",
    folder="dramas", page="dramas.html", rss_file="rss_dramas.xml", legacy_file="posted_dramas.txt",
    feeds=[
        bing_news("kurulus osman mehmed fetihler sultani"),
        bing_news("turkish historical drama"),
        bing_news("netflix new series release", "day"),
        bing_news("turkish drama series trailer"),
    ],
    role="an entertainment writer covering Turkish historical dramas and streaming series",
    instructions=(
        "Use headings such as 'What's new', 'About the series' and 'What to expect'. "
        "Do not invent cast names, episode counts, air dates or plot details that are not in the SOURCE."
    ),
    image_style="cinematic medieval historical drama scene, dramatic lighting, illustration, no text, no real people",
    image_query="cinematic historical castle",
    button_text="🎬 Read the Source Article",
    card_button="Read More",
    telegram_heading="NEW DRAMA UPDATE",
    rss_heading="Drama Update",
    rss_title="Trendify Portal - Dramas",
    rss_description="Turkish historical dramas, Netflix and trailers",
    image_from_title=False, verify_numbers=False, min_source_chars=300,
)

SCHOLARSHIPS = Niche(
    name="scholarships", label="SCHOLARSHIPS", emoji="🎓",
    folder="scholarships", page="scholarships.html", rss_file="rss_scholarships.xml",
    legacy_file="posted_scholarships.txt",
    feeds=[
        bing_news("fully funded scholarships 2026", "day"),
        bing_news("scholarships for pakistani students", "day"),
        bing_news("hec scholarship pakistan"),
        bing_news("chevening fulbright daad erasmus scholarship"),
    ],
    role="an education advisor who writes accurate scholarship guides",
    instructions=(
        "Use headings such as 'Scholarship Overview', 'Who Can Apply', 'Benefits' and "
        "'How to Apply'. Only mention funding amounts, deadlines, countries or eligibility "
        "if the SOURCE states them."
    ),
    image_style="university campus students graduation realistic photography",
    image_query="university students campus",
    button_text="🎓 Official Details & Apply",
    card_button="View Scholarship",
    telegram_heading="NEW SCHOLARSHIP",
    rss_heading="Scholarship Alert",
    rss_title="Trendify Portal - Scholarships",
    rss_description="Fully funded and local scholarships",
    disclaimer="Always confirm deadlines and eligibility on the official scholarship website.",
    min_source_chars=400, risk="high",
)

HEALTH = Niche(
    name="health", label="HEALTH", emoji="🩺",
    folder="health", page="health.html", rss_file="rss_health.xml", legacy_file="posted_health.txt",
    feeds=[
        "https://www.nih.gov/news-releases/feed.xml",
        "https://www.health.harvard.edu/authors/harvard-health-publishing-staff/feed/rss",
        bing_news("senior health nutrition wellness study"),
        bing_news("healthy aging exercise older adults"),
    ],
    role="a careful health writer producing general wellness information for adults over 60",
    instructions=(
        "This is general education only. Do not diagnose, and do not give treatment, dosage or "
        "medication advice. Never claim that anything cures or prevents a disease. Use cautious "
        "wording such as 'research suggests' and name the source organisation. Use headings such as "
        "'Key Takeaways', 'What the Source Says' and 'Practical Notes'. End with a sentence "
        "recommending readers talk to their doctor."
    ),
    image_style="healthy active senior couple, fresh healthy food, bright natural light, realistic photography",
    image_query="healthy seniors nutrition",
    button_text="🩺 Read the Original Source",
    card_button="Read Health Guide",
    telegram_heading="SENIOR HEALTH TIP",
    rss_heading="Senior Health",
    rss_title="Trendify Portal - Health",
    rss_description="Wellness and nutrition information for seniors",
    disclaimer="This article is for general information only and is not medical advice. Talk to your doctor before making health decisions.",
    image_from_title=False, min_source_chars=800, min_words=200, risk="high",
)

HISTORY = Niche(
    name="history", label="HISTORY", emoji="🦖",
    folder="history", page="history.html", rss_file="rss_history.xml", legacy_file="posted_history.txt",
    feeds=[
        bing_news("dinosaur fossil discovery", "day"),
        bing_news("t rex brachiosaurus paleontology"),
        bing_news("ancient civilization archaeology discovery"),
        bing_news("prehistoric animals new study"),
    ],
    role="a science and history writer who explains discoveries about prehistoric life and the ancient world",
    instructions=(
        "Use headings such as 'The Discovery', 'What Scientists Found' and 'Why It Matters'. "
        "Do not state ages, sizes or dates that are not in the SOURCE."
    ),
    image_style="prehistoric landscape with dinosaurs, natural history museum illustration, no text",
    image_query="fossil museum dinosaur",
    button_text="📚 Read More at the Source",
    card_button="Read More",
    telegram_heading="HISTORY & DISCOVERY",
    rss_heading="History Update",
    rss_title="Trendify Portal - History",
    rss_description="Prehistoric wildlife and ancient history",
    image_from_title=False, verify_numbers=False, min_source_chars=400,
)

NICHES = {n.name: n for n in (NEWS, JOBS, DRAMAS, SCHOLARSHIPS, HEALTH, HISTORY)}
