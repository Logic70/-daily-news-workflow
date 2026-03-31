#!/usr/bin/env python3
"""
RSS 生成器
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def generate_rss(news_data, date_str, base_url="https://yourusername.github.io/daily-news-workflow"):
    """生成 RSS 2.0"""
    items_xml = []

    for item in news_data.get("items", []):
        title = item.get("title", "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        desc = (item.get("description", "") or item.get("content", ""))[:500]
        desc = desc.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        link = item.get("link", "")
        pub_date = item.get("published", datetime.now().isoformat())

        item_xml = f"""
    <item>
      <title>{title}</title>
      <description>{desc}</description>
      <link>{link}</link>
      <guid isPermaLink="true">{link}</guid>
      <pubDate>{pub_date}</pubDate>
    </item>"""
        items_xml.append(item_xml)

    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>科技新闻快报</title>
    <link>{base_url}</link>
    <description>每日精选科技新闻</description>
    <language>zh-CN</language>
    <lastBuildDate>{datetime.now().isoformat()}</lastBuildDate>
    <atom:link href="{base_url}/rss.xml" rel="self" type="application/rss+xml" />
    {''.join(items_xml)}
  </channel>
</rss>
"""
    return rss


def main():
    parser = argparse.ArgumentParser(description="生成 RSS")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--base-url", default="https://yourusername.github.io/daily-news-workflow")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        news_data = json.load(f)

    date_str = news_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    rss = generate_rss(news_data, date_str, args.base_url)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss)

    print(f"✓ RSS 生成: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
