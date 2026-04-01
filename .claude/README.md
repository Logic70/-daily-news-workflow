# .claude/ 目录说明

## 用途

此目录表示这是一个**标准工作流仓库**，可被 [WorkflowProgram-CN](https://github.com/Logic70/WorkflowProgram-CN) 识别和演进。

## 重要说明

⚠️ **本目录中的文件不是可执行命令**：
- `settings.json` 不会自动注册命令到 Claude Code
- `skills/` 中的文档仅供 `/evolve-workflow` 审计使用
- 实际执行请查看 `scripts/` 目录

## 实际使用方法

### 1. GitHub Actions 自动执行（推荐）
每天 UTC 01:00 自动运行，输出到 GitHub Pages。

### 2. 本地手动执行
```bash
python scripts/fetch-news.py --output cache/daily-news.json
python scripts/generate-all.py --input cache/daily-news.json --output-dir docs
```

### 3. 使用 Claude Code 辅助
在 Claude Code 中打开本仓库，通过对话请求 Claude 协助运行脚本或调试问题。

## 演进方法

如需审计和改进本工作流：
```bash
# 在 WorkflowProgram-CN 仓库中执行
/evolve-workflow /path/to/daily-news-workflow
```
