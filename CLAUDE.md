# Daily Tech News Digest

每天自动收集科技新闻，生成多格式输出（HTML / Markdown / RSS），支持 GitHub Actions 自动化部署。

> **Code Agent 工作流**: 本仓库包含 `.claude/` 结构，可被 WorkflowProgram-CN 识别和演进。

## Claude Code 集成说明

在 Claude Code 中打开本仓库后，可以通过**自然语言对话**协助调试和修改代码：

```bash
# 在终端中打开仓库
cd /path/to/daily-news-workflow
claude
```

**使用示例**：
- "运行脚本收集今天的新闻"
- "查看 cache/daily-news.json 的内容"
- "为什么 RSS 收集失败？"

**注意**：`.claude/` 中的文件是设计文档，**不会**自动注册为 Claude Code 的 `/` 命令。

## 功能

- **配置驱动**: 从 `config/news-sources.json` 读取源配置和筛选参数
- **多源收集**: RSS、NewsAPI、GitHub Trending、HuggingFace
- **智能翻译**: 自动将英文新闻翻译为中文
- **内容筛选**: 基于关键实体计算相关性分数
- **多格式输出**:
  - HTML - 精美网页，适合浏览器阅读
  - Markdown - 纯文本，版本控制友好
  - RSS - 订阅器集成
  - AI 总结 - 自动分类和要点提取
- **自动部署**: GitHub Actions + GitHub Pages

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 收集新闻（配置驱动）
python scripts/fetch-news.py --output cache/news.json

# 生成所有格式
python scripts/generate-all.py --input cache/news.json --output-dir docs --summary

# 查看结果
open docs/index.html
```

### GitHub Actions 自动部署

1. Fork 本仓库
2. 在 Settings → Secrets 添加 `NEWS_API_KEY`（可选）
3. 在 Settings → Pages 选择 GitHub Actions 作为源
4. 每天自动运行，输出到 GitHub Pages

## 配置

编辑 `config/news-sources.json` 自定义：
- RSS 源列表（名称、URL、优先级、max_items）
- 筛选实体（公司、人物、技术关键词）
- 评分权重（title_entity、content_entity 等）
- 输出目录（cache_dir、docs_dir）

## 数据源

| 来源 | 类型 | 说明 |
|------|------|------|
| RSS | 新闻 | TechCrunch、The Verge、36氪等 |
| NewsAPI | API | 科技新闻聚合 |
| GitHub Trending | 开源 | AI/ML 相关热门项目 |
| HuggingFace | 模型 | 热门 AI 模型 |

## 项目结构

```
daily-news-workflow/
├── .claude/              # 工作流标记（可被 WorkflowProgram-CN 演进）
│   ├── README.md         # .claude/ 目录说明
│   ├── skills/           # 技能定义
│   └── settings.json     # 命令注册表
├── .github/workflows/    # GitHub Actions
├── scripts/
│   ├── fetch-news.py     # 新闻收集（配置驱动）
│   ├── generate-all.py   # 多格式生成
│   ├── generate-html.py  # HTML 生成
│   ├── generate-rss.py   # RSS 生成
│   └── generate-summary.py # AI 总结
├── config/
│   └── news-sources.json # 统一配置文件
├── docs/                 # 输出目录（GitHub Pages）
├── cache/                # 缓存
└── requirements.txt
```

## 环境变量

| 变量 | 说明 |
|------|------|
| `NEWS_API_KEY` | NewsAPI 密钥（可选） |
| `ANTHROPIC_API_KEY` | Claude API 密钥（用于高级 AI 总结，可选） |

## 订阅地址

部署后，RSS 订阅地址：
```
https://Logic70.github.io/-daily-news-workflow/rss.xml
```

## License

MIT
