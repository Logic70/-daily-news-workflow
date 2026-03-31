---
name: daily-news
description: Generate daily tech news digest PDF from multiple sources
version: 1.0.0
---

# Daily News Generation Skill

生成每日科技新闻快报PDF，支持自动和手动触发。

## 触发方式

- 命令: `/daily-news [--date YYYY-MM-DD] [--output-dir PATH]`
- 自动: 每天09:00通过cron触发

## 职责

1. 接收用户命令和参数
2. 协调4个Stage的执行
3. 管理Agent之间的数据传递
4. 收集执行结果并生成报告
5. 处理错误和重试

## 执行流程

```
Stage 1: News Collection (Fan-out)
├── RSS Collector Agent
├── API Collector Agent
└── Web Collector Agent

Stage 2: Content Filtering (Sequential)
└── Content Filter Agent

Stage 3: PDF Generation (Sequential)
└── PDF Generator Agent

Stage 4: Quality Check (Parallel)
├── File Validator
└── Content Validator
```

## 参数

- `--date`: 指定日期 (默认: 今天)
- `--output-dir`: 输出目录 (默认: `./output`)
- `--sources`: 指定新闻源 (可选)

## 输出

- 主输出: `tech-news-digest-YYYY-MM-DD.pdf`
- 缓存: `cache/raw-news-YYYY-MM-DD.json`
- 日志: `logs/daily-news-YYYY-MM-DD.log`

## 错误处理

- 网络错误: 重试2次，使用指数退避
- 单个源失败: 记录警告，继续处理其他源
- 质量检查失败: 终止并报告详细错误

## 依赖

- Python 3.9+
- Playwright (PDF生成)
- feedparser (RSS解析)
- requests, beautifulsoup4 (网页抓取)
