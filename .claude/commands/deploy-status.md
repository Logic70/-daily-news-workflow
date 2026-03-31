# /deploy-status

检查 GitHub Actions 工作流运行状态和 GitHub Pages 部署情况。

## Usage

```text
/deploy-status [--workflow daily-news] [--limit 5]
```

## Stage 1: 获取 Actions 状态

**Goal**: 查询最近的 workflow 运行

**Steps**:
1. 运行 `gh run list --workflow=daily-news.yml --limit=5`
2. 解析状态（success, failure, in_progress）

**Verify**:
- [ ] 能获取到 run 列表
- [ ] 状态信息完整

## Stage 2: 获取 Pages 部署状态

**Goal**: 检查 GitHub Pages 是否成功部署

**Steps**:
1. 运行 `gh api repos/{owner}/{repo}/pages`
2. 解析部署状态和 URL

## Stage 3: 汇总报告

**Goal**: 生成状态摘要

**Output Format**:

```markdown
## 部署状态

### GitHub Actions
| Run ID | 状态 | 时间 | 分支 |
|--------|------|------|------|
| ... | success | 2 hours ago | main |

### GitHub Pages
- 状态: built
- URL: https://Logic70.github.io/-daily-news-workflow/
- 上次部署: 2 hours ago

### 建议
- ✅ 一切正常
- ⚠️ 最新 run 失败，查看日志...
```
