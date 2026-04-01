#!/usr/bin/env python3
"""
新闻获取脚本 - 从多个源收集科技新闻
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def load_config():
    """从 config/news-sources.json 加载配置"""
    config_path = Path(__file__).parent.parent / "config" / "news-sources.json"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠ 无法加载配置文件: {e}，使用默认配置")
        return None


# 加载全局配置
CONFIG = load_config()


# RSS收集器
class RSSCollector:
    """从RSS源收集新闻"""

    def __init__(self, config=None):
        self.items = []
        self.errors = []
        self.config = config or CONFIG

        # 从配置加载源，如果配置不存在则使用默认
        if self.config and "sources" in self.config:
            self.sources = self.config["sources"].get("rss", [])
        else:
            # 默认源
            self.sources = [
                {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "max_items": 10},
                {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml", "max_items": 10},
                {"name": "36氪", "url": "https://36kr.com/feed", "max_items": 10},
            ]

    def collect(self, max_per_source=10):
        """从所有RSS源收集新闻"""
        try:
            import feedparser
        except ImportError:
            print("警告: feedparser未安装，跳过RSS收集")
            self.errors.append({"source": "all", "error": "feedparser未安装"})
            return self.items

        # 如果配置中有 max_items，优先使用
        for source in self.sources:
            try:
                max_items = source.get("max_items", max_per_source)
                feed = feedparser.parse(source["url"])
                for entry in feed.entries[:max_items]:
                    self.items.append({
                        "title": entry.get("title", ""),
                        "description": entry.get("summary", entry.get("description", "")),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "source": source["name"]
                    })
            except Exception as e:
                self.errors.append({"source": source["name"], "error": str(e)})

        return self.items


# API收集器
class APICollector:
    """从新闻API收集数据"""

    def __init__(self):
        self.items = []
        self.error = None

    def collect(self, query="technology", page_size=20):
        """从NewsAPI收集新闻"""
        try:
            import requests
        except ImportError:
            print("警告: requests未安装，跳过API收集")
            self.error = "requests未安装"
            return self.items

        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            print("警告: NEWS_API_KEY环境变量未设置")
            self.error = "API密钥未配置"
            return self.items

        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
            "apiKey": api_key
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()

            if data.get("status") == "ok":
                for article in data.get("articles", []):
                    self.items.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "link": article.get("url", ""),
                        "published": article.get("publishedAt", ""),
                        "source": article.get("source", {}).get("name", "NewsAPI")
                    })
            else:
                self.error = data.get("message", "未知错误")

        except Exception as e:
            self.error = str(e)

        return self.items


# 内容筛选器
class ContentFilter:
    """根据关键实体筛选新闻"""

    def __init__(self, items, config=None):
        self.items = items
        self.config = config or CONFIG

        # 从配置加载关键实体和评分权重
        if self.config and "filtering" in self.config:
            filtering = self.config["filtering"]
            self.key_entities = filtering.get("key_entities", {})
            self.scoring = filtering.get("scoring", {})
            self.max_output = filtering.get("max_output", 20)
            self.min_relevance = filtering.get("min_relevance", 0.3)
        else:
            # 默认配置
            self.key_entities = {
                "companies": [
                    "Apple", "Microsoft", "Google", "Amazon", "Meta", "Tesla", "NVIDIA",
                    "OpenAI", "Anthropic", "字节跳动", "阿里巴巴", "腾讯", "华为"
                ],
                "people": [
                    "Elon Musk", "Satya Nadella", "Tim Cook", "Sundar Pichai",
                    "Sam Altman"
                ],
                "technologies": [
                    "AI", "人工智能", "LLM", "大模型", "ChatGPT", "Claude"
                ]
            }
            self.scoring = {"title_entity": 0.4, "content_entity": 0.2}
            self.max_output = 20
            self.min_relevance = 0.3

    def filter(self, max_output=None, min_relevance=None):
        """筛选新闻并计算相关性分数"""
        max_output = max_output or self.max_output
        min_relevance = min_relevance or self.min_relevance
        filtered = []

        title_score = self.scoring.get("title_entity", 0.4)
        content_score = self.scoring.get("content_entity", 0.2)

        for item in self.items:
            title = item.get("title", "")
            content = item.get("description", "")
            text = f"{title} {content}"

            # 计算相关性分数
            score = 0.0
            entities_found = []

            # 标题提及 +title_score
            for entity in self.key_entities.get("companies", []):
                if entity in title:
                    score += title_score
                    entities_found.append(entity)
                    break

            # 正文提及
            body_matches = 0
            for category in self.key_entities.values():
                for entity in category:
                    if entity in content:
                        body_matches += 1
                        if entity not in entities_found:
                            entities_found.append(entity)

            score += min(body_matches * content_score, 0.4)

            if score >= min_relevance:
                item["relevance_score"] = round(score, 2)
                item["entities"] = entities_found
                filtered.append(item)

        # 按相关性排序
        filtered.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)

        return filtered[:max_output]


# 翻译器
class Translator:
    """翻译新闻标题和摘要到中文"""

    def __init__(self):
        self.translator = None
        try:
            from deep_translator import GoogleTranslator
            self.translator = GoogleTranslator(source='auto', target='zh-CN')
            print("  ✓ 翻译服务初始化成功")
        except Exception as e:
            print(f"  ⚠ 翻译服务初始化失败: {e}")

    def translate(self, text):
        """翻译文本"""
        if not self.translator or not text:
            return text

        try:
            # 限制翻译长度，避免API限制
            if len(text) > 1000:
                text = text[:1000] + "..."

            result = self.translator.translate(text)
            return result if result else text
        except Exception as e:
            print(f"  ⚠ 翻译失败: {e}")
            return text

    def translate_news(self, items):
        """批量翻译新闻"""
        if not self.translator:
            print("  ⚠ 翻译服务不可用，使用原文")
            return items

        translated_items = []
        for i, item in enumerate(items):
            # 保存原文
            item['title_original'] = item.get('title', '')
            item['description_original'] = item.get('description', '')

            # 翻译标题
            print(f"  翻译 [{i+1}/{len(items)}]: {item['title'][:40]}...", end=' ', flush=True)
            item['title'] = self.translate(item.get('title', ''))

            # 翻译摘要
            item['description'] = self.translate(item.get('description', ''))

            print("✓")
            translated_items.append(item)

        return translated_items


# GitHub Trending 收集器
class GitHubTrendingCollector:
    """从 GitHub Trending 收集 AI 相关项目"""

    def collect(self):
        """获取 GitHub Trending"""
        try:
            import requests
            from bs4 import BeautifulSoup
        except ImportError:
            return []

        items = []
        try:
            url = "https://github.com/trending/python?since=daily"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=30)
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('article', class_='Box-row')[:5]
            for article in articles:
                try:
                    link = article.find('h2', class_='h3').find('a')
                    title = link.get_text(strip=True).replace('\n', '').replace(' ', '')
                    desc_elem = article.find('p', class_='col-9')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""

                    # 只保留 AI 相关项目
                    if any(kw in title.lower() or desc_elem and kw in desc_elem.get_text(strip=True).lower()
                           for kw in ['ai', 'ml', 'machine', 'learning', 'llm', 'gpt', 'neural', 'model']):
                        items.append({
                            "title": f"[GitHub] {title}",
                            "description": description,
                            "link": f"https://github.com{link['href']}",
                            "published": datetime.now().isoformat(),
                            "source": "GitHub Trending"
                        })
                except Exception:
                    continue
        except Exception as e:
            print(f"  ⚠ GitHub Trending 获取失败: {e}")

        return items


# HuggingFace 收集器
class HuggingFaceCollector:
    """从 HuggingFace 获取热门模型"""

    def collect(self):
        """获取 HuggingFace Trending"""
        try:
            import requests
        except ImportError:
            return []

        items = []
        try:
            url = "https://huggingface.co/api/models?sort=likes&direction=-1&limit=10"
            response = requests.get(url, timeout=30)
            data = response.json()

            for model in data:
                try:
                    model_id = model.get('id', '')
                    description = model.get('description', 'AI Model')
                    if description:
                        description = description[:200]

                    items.append({
                        "title": f"[HuggingFace] {model_id}",
                        "description": description,
                        "link": f"https://huggingface.co/{model_id}",
                        "published": datetime.now().isoformat(),
                        "source": "HuggingFace"
                    })
                except Exception:
                    continue
        except Exception as e:
            print(f"  ⚠ HuggingFace 获取失败: {e}")

        return items


def main():
    parser = argparse.ArgumentParser(description="获取科技新闻")
    parser.add_argument("--date", help="指定日期 (YYYY-MM-DD)")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--max-items", type=int, default=20, help="最大输出数量")
    args = parser.parse_args()

    print("=" * 50)
    print("科技新闻收集器")
    print("=" * 50)

    # 收集RSS新闻
    print("\n[Stage 1] 从RSS源收集新闻...")
    rss_collector = RSSCollector()
    rss_items = rss_collector.collect()
    print(f"  ✓ 从RSS获取 {len(rss_items)} 条新闻")

    # 收集API新闻
    print("\n[Stage 2] 从API收集新闻...")
    api_collector = APICollector()
    api_items = api_collector.collect()
    print(f"  ✓ 从API获取 {len(api_items)} 条新闻")

    # 合并所有新闻
    all_items = rss_items + api_items
    print(f"\n总计获取 {len(all_items)} 条原始新闻")

    # 收集 GitHub Trending
    print("\n[Stage 2b] 从 GitHub Trending 收集...")
    github_collector = GitHubTrendingCollector()
    github_items = github_collector.collect()
    print(f"  ✓ 从 GitHub 获取 {len(github_items)} 条项目")
    all_items.extend(github_items)

    # 收集 HuggingFace
    print("\n[Stage 2c] 从 HuggingFace 收集...")
    hf_collector = HuggingFaceCollector()
    hf_items = hf_collector.collect()
    print(f"  ✓ 从 HuggingFace 获取 {len(hf_items)} 条模型")
    all_items.extend(hf_items)

    print(f"\n总计获取 {len(all_items)} 条原始新闻")

    # 内容筛选
    print(f"\n[Stage 3] 内容筛选 (max={args.max_items})...")
    filter_engine = ContentFilter(all_items)
    filtered = filter_engine.filter(max_output=args.max_items)
    print(f"  ✓ 筛选后 {len(filtered)} 条新闻")

    # 翻译
    print("\n[Stage 4] 翻译新闻标题和摘要...")
    translator = Translator()
    filtered = translator.translate_news(filtered)
    print(f"  ✓ 翻译完成")

    # 输出结果
    result = {
        "date": args.date or datetime.now().strftime("%Y-%m-%d"),
        "total_raw": len(all_items),
        "total_filtered": len(filtered),
        "items": filtered
    }

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 结果已保存: {args.output}")
    else:
        print("\n" + "=" * 50)
        print("筛选结果预览:")
        print("=" * 50)
        for i, item in enumerate(filtered[:5], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   来源: {item['source']} | 相关度: {item['relevance_score']}")
            print(f"   链接: {item['link']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
