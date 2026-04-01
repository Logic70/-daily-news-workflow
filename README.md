# Daily Tech News Digest

> 每日科技新闻早报，自动收集、智能翻译、极简呈现。

[![GitHub Actions](https://github.com/Logic70/-daily-news-workflow/actions/workflows/daily-news.yml/badge.svg)](https://github.com/Logic70/-daily-news-workflow/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[📖 在线阅读](https://Logic70.github.io/-daily-news-workflow/) | [📡 RSS订阅](https://Logic70.github.io/-daily-news-workflow/rss.xml)

---

## 📋 简要介绍

**Daily Tech News Digest** 是一个自动化科技新闻收集工具，每日从多个权威来源获取最新科技资讯，自动翻译为中文，并以极简风格呈现。

### 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **多源聚合** | RSS + NewsAPI + GitHub Trending + HuggingFace |
| 🌐 **自动翻译** | 英文新闻自动翻译为中文 |
| 🎯 **智能筛选** | 基于关键实体（公司/人物/技术）的相关性评分 |
| 📱 **多格式输出** | HTML网页 + Markdown + RSS订阅 + AI总结 |
| ⚡ **自动部署** | GitHub Actions 每日自动运行，GitHub Pages 托管 |
| 🎨 **极简设计** | 专注内容，无干扰阅读体验 |

### 数据来源

- **TechCrunch** / **The Verge** - 国际科技媒体
- **36氪** / **极客公园** - 中文科技媒体
- **NewsAPI** - 全球新闻聚合
- **GitHub Trending** - AI/ML 热门开源项目
- **HuggingFace** - 最新AI模型

---

## 🚀 使用方法

### 方式一：在线阅读（推荐）

直接访问 GitHub Pages 地址：
- 📄 **网页版**: https://Logic70.github.io/-daily-news-workflow/
- 📡 **RSS订阅**: https://Logic70.github.io/-daily-news-workflow/rss.xml

### 方式二：GitHub Actions 自动执行

Fork 本仓库后自动配置：
1. 仓库 Settings → Pages → 选择 GitHub Actions 源
2. （可选）Settings → Secrets → 添加 `NEWS_API_KEY`
3. 每天 UTC 01:00 自动运行

### 方式三：本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 收集新闻（自动读取 config/news-sources.json）
python scripts/fetch-news.py --output cache/daily-news.json

# 生成多格式输出
python scripts/generate-all.py --input cache/daily-news.json --output-dir docs --summary
```

### 方式四：Claude Code 辅助（开发/调试）

在 Claude Code 中打开本仓库，通过**自然语言对话**协助调试和修改代码。
**注意**：`.claude/` 中的文件是设计文档，不会自动注册为 `/` 命令。

---

## ⚙️ 配置自定义

编辑 `config/news-sources.json` 自定义：
- **RSS 源列表**：添加/删除/修改 RSS 源
- **筛选实体**：公司、人物、技术关键词
- **评分权重**：调整相关性评分算法
- **输出设置**：缓存目录、输出目录

---

```bash
# 在终端中打开仓库
cd /path/to/daily-news-workflow
claude
```

在 Claude Code 中，你可以：

1. **直接运行脚本**（推荐）
   ```text
   User: 运行脚本收集今天的新闻
   Claude: 执行 python scripts/fetch-news.py...
   ```

2. **查看和编辑文件**
   ```text
   User: 查看 cache/daily-news.json 的内容
   Claude: 显示文件内容...
   ```

3. **调试问题**
   ```text
   User: 为什么 RSS 收集失败？
   Claude: 检查代码，发现...
   ```

**注意**：`.claude/commands/` 中的命令定义是**设计文档**，展示工作流的阶段结构，不会自动注册为 Claude Code 的 `/` 命令。

### 方式三：本地命令行运行

```bash
# 克隆仓库
git clone https://github.com/Logic70/-daily-news-workflow.git
cd -daily-news-workflow

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 获取新闻
python scripts/fetch-news.py --output cache/news.json

# 生成所有格式
python scripts/generate-all.py --input cache/news.json --output-dir docs --summary

# 查看结果
open docs/index.html  # 或双击文件
```

### 配置 API Key（可选）

```bash
# 复制示例配置
cp .env.example .env

# 编辑 .env 填入你的 API Key
# NEWS_API_KEY=your_key_here  # 从 newsapi.org 获取
```

> ⚠️ **安全提示**: `.env` 文件已被 `.gitignore` 排除，不会提交到 Git。

---

## 📁 项目结构

```
├── .claude/                    # Claude Code 工作流标记（可被 WorkflowProgram-CN 演进）
│   ├── commands/               # 命令设计文档（展示工作流阶段结构）
│   ├── skills/                 # 技能定义
│   └── settings.json           # 工作流元数据
│
├── .github/workflows/          # GitHub Actions 工作流（实际自动运行）
│   └── daily-news.yml          # 每日 UTC 01:00 自动运行
│
├── scripts/                    # 核心脚本（本地运行或 Claude 辅助调试）
│   ├── fetch-news.py           # 新闻收集（RSS/API/GitHub/HF）
│   ├── generate-all.py         # 多格式生成器
│   ├── generate-html.py        # HTML生成
│   ├── generate-rss.py         # RSS生成
│   └── generate-summary.py     # AI总结生成
│
├── docs/                       # 生成输出（GitHub Pages）
│   ├── index.html              # 网页版
│   ├── index.md                # Markdown版
│   ├── rss.xml                 # RSS订阅
│   └── summary.md              # AI总结
│
├── cache/                      # 数据缓存（.gitignore）
├── fonts/                      # 中文字体文件
├── config/                     # 配置文件
├── requirements.txt            # Python依赖
├── SECURITY.md                 # 安全指南
└── README.md                   # 本文件
```

### 关键文件说明

| 文件 | 作用 |
|------|------|
| `.claude/` | **工作流标记**：表示这是一个可被 WorkflowProgram-CN 审计和演进的标准工作流仓库 |
| `scripts/fetch-news.py` | 新闻收集主程序，支持4种数据源 |
| `scripts/generate-all.py` | 多格式输出，一次生成所有文件 |
| `.github/workflows/daily-news.yml` | GitHub Actions 定时任务（每日 UTC 01:00） |
| `config/news-sources.json` | 新闻源配置（可自定义） |

---

## 💡 设计哲学

### 1. 自动化优先

> "让机器做重复的事，让人做判断的事。"

- **全自动流程**: 从收集到部署，无需人工干预
- **定时触发**: 每天自动运行，像早报一样准时
- **失败重试**: 单个源失败不影响整体流程

### 2. 内容为王

> "极简不是少，而是没有多余。"

- **无干扰设计**: 纯白背景，无广告，无弹窗
- **信息密度**: 标题 + 摘要 + 来源，三步获取核心信息
- **中文优先**: 自动翻译，降低阅读门槛

### 3. 开放与隐私

> "你的数据属于你。"

- **本地优先**: 所有数据处理在本地完成
- **API可选**: 无需API Key也能运行基础功能
- **隐私保护**: 不追踪用户，不收集数据

### 4. 可扩展架构

> "为变化而设计。"

- **模块化收集器**: 新增数据源只需添加一个 Class
- **多格式输出**: HTML/Markdown/RSS 统一生成
- **Agent化设计**: 每个环节可独立优化替换

### 5. 可持续运营

> "低维护，长期跑。"

- **免费托管**: GitHub Pages + Actions，零成本
- **资源友好**: 低频率运行，低API消耗
- **容错设计**: 单点失败不影响整体服务

---

## 🛠️ 技术栈

- **Python 3.11+** - 核心语言
- **feedparser** - RSS解析
- **beautifulsoup4** - HTML解析
- **deep-translator** - 自动翻译
- **GitHub Actions** - CI/CD自动化
- **GitHub Pages** - 静态托管

---

## 📄 许可证

- **代码**: [MIT License](LICENSE)
- **内容**: 新闻版权归原媒体所有，翻译仅供学习交流

---

## 🙏 致谢

- [NewsAPI](https://newsapi.org) - 新闻数据
- [HuggingFace](https://huggingface.co) - AI模型趋势
- [GitHub](https://github.com) - 托管与Actions

---

> 📝 **注意**: 本项目仅供学习交流，新闻内容版权归原作者所有。
