import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone

QUERIES = [
    ("AI & Automation", "topic:ai-agent+stars:>200"),
    ("Developer & CLI Tools", "topic:cli-tool+stars:>100"),
    ("Workflow & Web Utilities", "topic:browser-automation+stars:>100"),
    ("Open-Source Productivity", "topic:productivity+topic:open-source+stars:>300")
]

DB_FILE = "tools_database.json"
OUTPUT_MD = "DISCOVERED_TOOLS.md"

def fetch_repos(query):
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=10"
    headers = {"User-Agent": "Free-Tool-Scout-Bot"}
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        headers["Authorization"] = f"token {github_token}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            return data.get("items", [])
    except Exception as e:
        print(f"Error fetching query '{query}': {e}")
        return []

def main():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                db = json.load(f)
            except Exception:
                db = {}
    else:
        db = {}

    new_count = 0
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    for category, query in QUERIES:
        items = fetch_repos(query)
        for item in items:
            repo_id = item["full_name"]
            if repo_id not in db:
                db[repo_id] = {
                    "name": item.get("name"),
                    "full_name": repo_id,
                    "url": item.get("html_url"),
                    "description": item.get("description") or "No description provided.",
                    "stars": item.get("stargazers_count", 0),
                    "language": item.get("language") or "N/A",
                    "category": category,
                    "first_seen": now_utc
                }
                new_count += 1

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

    # Generate Markdown summary
    md_content = [
        "# 🛠️ 24/7 Discovered Free & Open-Source Tools\n",
        f"Last updated: **{now_utc}** | Total scouted: **{len(db)}** | New this run: **{new_count}**\n\n",
        "| Tool | Category | Language | Stars | Description |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]

    # Sort tools by stars descending
    sorted_tools = sorted(db.values(), key=lambda x: x.get("stars", 0), reverse=True)
    for tool in sorted_tools:
        name_link = f"[{tool['name']}]({tool['url']})"
        desc = (tool['description'] or '').replace("|", "\\|").replace("\n", " ")
        md_content.append(f"| **{name_link}** | {tool['category']} | {tool['language']} | ⭐ {tool['stars']} | {desc} |")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content) + "\n")

    print(f"Scout complete. Total tools in database: {len(db)} (New: {new_count})")

if __name__ == "__main__":
    main()
