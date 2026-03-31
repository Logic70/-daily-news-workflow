---
name: news-collector
description: 新闻收集核心技能，支持多源聚合、内容筛选和翻译
version: 1.0.0
---

# News Collector Skill

## 能力范围

1. **多源收集**: RSS、API、GitHub Trending、HuggingFace
2. **内容筛选**: 基于实体的相关性评分
3. **自动翻译**: 英文 → 中文
4. **多格式输出**: HTML、Markdown、RSS

## 快速开始

```bash
# 收集今天的新闻
python scripts/fetch-news.py --output cache/daily-news.json

# 生成所有格式
python scripts/generate-all.py --input cache/daily-news.json --output-dir docs
```

## 数据源配置

见 `.claude/rules/news-sources.md`

## 输出文件

| 文件 | 说明 |
|------|------|
| `docs/index.html` | GitHub Pages 网页版 |
| `docs/rss.xml` | RSS 订阅源 |
| `docs/index.md` | Markdown 版本 |
