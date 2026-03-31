# News Sources Configuration

来源: 2026-03-31 daily-news workflow设计

## RSS 源

### 英文源

| 名称 | URL | 优先级 | 说明 |
|------|-----|--------|------|
| TechCrunch | https://techcrunch.com/feed/ | high | 顶级科技新闻 |
| The Verge | https://www.theverge.com/rss/index.xml | high | 综合科技媒体 |
| Ars Technica | https://arstechnica.com/feed/ | medium | 深度技术报道 |
| Wired | https://www.wired.com/feed/rss | medium | 科技文化 |

### 中文源

| 名称 | URL | 优先级 | 说明 |
|------|-----|--------|------|
| 36氪 | https://36kr.com/feed | high | 创业和科技 |
| 极客公园 | https://www.geekpark.net/rss | high | 产品和科技 |
| 虎嗅 | https://www.huxiu.com/rss/0.xml | medium | 商业科技 |
| 机器之心 | https://www.jiqizhixin.com/rss | medium | AI垂直媒体 |

## API 源

### NewsAPI

- 端点: `https://newsapi.org/v2/everything`
- 参数:
  - `q`: "technology OR AI OR artificial intelligence"
  - `language`: "en,zh"
  - `sortBy`: "publishedAt"
  - `pageSize`: 20
- 配额: 100次/天 (免费版)

### GNews (备选)

- 端点: `https://gnews.io/api/v4/search`
- 参数:
  - `q`: "technology"
  - `lang`: "en,zh"
  - `max`: 20

## Web 源

用于直接抓取（当RSS不可用时）

| 名称 | URL | 选择器 | 说明 |
|------|-----|--------|------|
| TechCrunch | https://techcrunch.com | `article h2 a` | 主站首页 |
| The Verge | https://www.theverge.com | `.c-entry-box--compact h2 a` | 首页文章 |
| 36氪 | https://36kr.com | `.article-item-title a` | 首页列表 |

## 关键实体

### 公司

```yaml
tech_giants:
  - Apple
  - Microsoft
  - Google
  - Amazon
  - Meta
  - Tesla
  - NVIDIA

ai_companies:
  - OpenAI
  - Anthropic
  - DeepSeek
  - 字节跳动
  - 阿里巴巴
  - 腾讯
  - 百度

startups:
  - Stripe
  - Airbnb
  - Uber
  - 小米
  - 美团
  - 拼多多
```

### 人物

```yaml
tech_leaders:
  - Elon Musk
  - Satya Nadella
  - Tim Cook
  - Sundar Pichai
  - Mark Zuckerberg

ai_researchers:
  - Sam Altman
  - Demis Hassabis
  - 黄仁勋
  - 李飞飞
  - 吴恩达
```

### 技术关键词

```yaml
ai:
  - AI
  - 人工智能
  - LLM
  - 大模型
  - ChatGPT
  - Claude
  - GPT
  - 机器学习

tech:
  - 区块链
  - Web3
  - 元宇宙
  - AR
  - VR
  - 量子计算
  - 云计算
  - 边缘计算
```

## 更新规则

- ALWAYS 在添加新源前验证RSS/URL可用性
- NEVER 添加需要登录或付费才能访问的源
- ALWAYS 尊重robots.txt和网站服务条款
- ALWAYS 当源连续3天失败时标记为inactive
