import json

with open("wiki.json", "r", encoding="utf-8") as f:
    data = json.load(f)  

print(f"Number of articles: {len(data)}\n")

for i, article in enumerate(data[:3], start=1):
    print(f"Article {i}:")
    print("URL:", article.get("url"))
    print("Title:", article.get("title"))
    print("First 200 symbols:", article.get("text")[:200], "...\n")
