---
name: news-collector
description: 新闻收集核心技能，支持从配置读取多源聚合、内容筛选和翻译
version: 1.1.0
---

# News Collector Skill

## 能力范围

1. **配置驱动**: 从 `config/news-sources.json` 读取 RSS 源、筛选参数和评分权重
2. **多源收集**: RSS、NewsAPI、GitHub Trending、HuggingFace
3. **内容筛选**: 基于关键实体的相关性评分
4. **自动翻译**: 英文 → 中文（使用 deep_translator）
5. **多格式输出**: HTML、Markdown、RSS（通过 generate-all.py）

## 执行方式

### GitHub Actions（推荐）
- 每天 UTC 01:00 自动执行
- 输出部署到 GitHub Pages

### 本地运行
```bash
# 收集新闻（自动读取 config/news-sources.json）
python scripts/fetch-news.py --output cache/daily-news.json

# 生成多格式输出
python scripts/generate-all.py --input cache/daily-news.json --output-dir docs --summary
```

## 配置

编辑 `config/news-sources.json` 自定义：
- RSS 源列表（名称、URL、优先级、max_items）
- API 参数（NewsAPI 查询条件、pageSize）
- 筛选实体（公司、人物、技术关键词）
- 评分权重（title_entity、content_entity 等）
- 输出目录（cache_dir、docs_dir）

## 代码结构

```python
# fetch-news.py
load_config()                    # 加载配置
RSSCollector(config)            # 从配置读取源列表
APICollector(config)            # 从配置读取 API 参数
GitHubTrendingCollector()       # 爬取 GitHub Trending
HuggingFaceCollector()          # 调用 HuggingFace API
ContentFilter(items, config)    # 从配置读取筛选参数
Translator()                    # 翻译为中文
```

## 输出

| 文件 | 说明 |
|------|------|
| `docs/index.html` | GitHub Pages 网页版 |
| `docs/index.md` | Markdown 版本 |
| `docs/rss.xml` | RSS 订阅源 |
| `docs/summary.md` | AI 总结（可选） |
| `cache/daily-news.json` | 原始数据缓存 |

## 依赖

见 `requirements.txt`:
- feedparser>=6.0.11
- requests>=2.31.0
- beautifulsoup4>=4.12.0
- deep-translator>=1.11.4

## 更新日志

### v1.1.0
- 支持从 config/news-sources.json 读取配置
- 修复裸 except 语句
- 更新 base_url 为实际值

### v1.0.0
- 初始版本
- 支持 4 种数据源
- 支持翻译和多格式输出
