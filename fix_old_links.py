import os
import re

def fix_links_in_file(filepath, old_link_pattern, new_link_replacement):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content, count = re.subn(old_link_pattern, new_link_replacement, content)
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed {count} links in {filepath}")
    return count

def main():
    # Example: Replace 'oldsite.com/article/' with 'newsite.com/news/' in all .md files in 'articles' folder
    articles_dir = os.path.join(os.path.dirname(__file__), 'articles')
    old_link_pattern = r'https://oldsite\\.com/article/'
    new_link_replacement = 'https://newsite.com/news/'
    total = 0
    if os.path.isdir(articles_dir):
        for root, _, files in os.walk(articles_dir):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    total += fix_links_in_file(path, old_link_pattern, new_link_replacement)
    print(f"Total links fixed: {total}")

if __name__ == "__main__":
    main()