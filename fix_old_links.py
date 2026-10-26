import re
from pathlib import Path

folders = ["news", "jobs", "scholarships", "dramas", "health", "history"]
pages = ["about.html", "contact.html", "privacy-policy.html", "editorial-policy.html"]
fixed = 0

for folder in folders:
    for file in Path(folder).glob("*.html"):
        text = file.read_text(encoding="utf-8")
        new_text = text
        for page in pages:
            # Sirf un links ko theek karo jinke pehle "../" nahi laga
            new_text = re.sub(rf'href="(?!\.\./){re.escape(page)}"', f'href="../{page}"', new_text)
        if new_text != text:
            file.write_text(new_text, encoding="utf-8")
            fixed += 1

print(f"Fixed {fixed} files")