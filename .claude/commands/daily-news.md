# Daily Tech News Digest

每天自动收集科技新闻，生成格式化的PDF新闻快报。支持手动触发指定日期。

## Usage

```text
/daily-news [--date YYYY-MM-DD] [--output-dir PATH] [--sources SOURCE_LIST]
```

示例:

```text
/daily-news
/daily-news --date 2026-03-20
/daily-news --output-dir ~/Documents/News
/daily-news --sources rss,api
```

## Stage 1: 新闻收集 (Fan-out)

**Goal**: 从多个源并行收集科技新闻数据

并行启动3个收集代理：
1. **RSS Collector**: 从RSS源获取新闻（TechCrunch, 36氪等）
2. **API Collector**: 从新闻API获取数据（NewsAPI等）
3. **Web Collector**: 从科技网站抓取头条

**Verify**:
- [ ] 至少2个源成功返回数据
- [ ] 原始新闻总数≥15条
- [ ] 数据格式为有效JSON

**On failure**: 重试2次，仍失败则记录到lessons.md并继续（使用部分数据）

## Stage 2: 内容筛选 (Sequential)

**Goal**: 根据关键实体筛选重要新闻

启动 **Content Filter Agent**：
1. 合并所有来源的新闻
2. 基于URL去重
3. 提取关键实体（公司、个人、技术）
4. 计算相关性分数
5. 筛选前20条相关新闻

关键实体包括：Apple, Google, OpenAI, 字节跳动, AI, 大模型等。

**Verify**:
- [ ] 输出≤20条新闻
- [ ] 所有条目包含title/content/url
- [ ] 按relevance_score降序排列

**On failure**: 重试1次，失败则使用原始数据继续

## Stage 3: PDF生成 (Sequential)

**Goal**: 生成格式精美的PDF文档

启动 **PDF Generator Agent**：
1. 读取HTML模板
2. 填充新闻数据
3. 使用Playwright渲染PDF
4. 添加页眉页脚和页码

**Verify**:
- [ ] PDF文件存在且>0字节
- [ ] 文件大小<10MB
- [ ] 包含日期页眉和标题

**On failure**: 重试2次，失败则终止并报告错误

## Stage 4: 质量检查 (Parallel)

**Goal**: 验证PDF符合质量标准

并行启动2个验证代理：
1. **File Validator**: 检查文件完整性、大小、格式
2. **Content Validator**: 检查内容完整性、格式规范

**Verify**:
- [ ] 所有CRITICAL检查PASS
- [ ] 新闻条目数≥预期的80%
- [ ] 无乱码，链接可点击

**On failure**: 报告详细错误，终止工作流

## Output

生成文件：
- `tech-news-digest-YYYY-MM-DD.pdf` - 新闻快报PDF
- `cache/raw-news-YYYY-MM-DD.json` - 原始数据缓存（可选）

## Auto Trigger

通过cron每天09:00自动执行：

```json
{
  "cron": "0 9 * * *",
  "command": "/daily-news"
}
```

## Configuration

新闻源配置在 `.claude/rules/news-sources.md`

## Dependencies

- Python 3.9+
- Playwright (PDF生成)
- feedparser, requests, beautifulsoup4
