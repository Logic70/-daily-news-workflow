# /configure

配置 API Key 和基本设置，支持交互式配置。

## Usage

```text
/configure [--api-key KEY] [--anthropic-key KEY]
```

## Stage 1: 配置检查

**Goal**: 检查当前配置状态

**Steps**:
1. 检查 `.env` 文件是否存在
2. 检查 GitHub Secrets 配置（如可用 gh cli）

## Stage 2: 交互式配置

**Goal**: 引导用户完成配置

**Steps**:
1. **本地开发配置**:
   - 复制 `.env.example` → `.env`
   - 提示输入 NEWS_API_KEY
   - 可选：输入 ANTHROPIC_API_KEY 用于 AI 摘要

2. **GitHub Secrets 配置**（可选）:
   - 提示是否配置 Actions Secrets
   - 使用 `gh secret set` 命令设置

## Stage 3: 验证配置

**Goal**: 测试配置是否有效

**Steps**:
1. 加载 `.env` 文件
2. 测试 NEWS_API_KEY 是否有效（可选）
3. 显示配置摘要（隐藏完整 key）

**Output**:

```markdown
## 配置完成 ✅

### 本地配置 (.env)
- NEWS_API_KEY: 已配置 (ab33...)
- ANTHROPIC_API_KEY: 未配置

### GitHub Secrets
- NEWS_API_KEY: 已配置

### 下一步
运行 `/fetch-news` 测试新闻收集功能
```

## Security Notes

- `.env` 文件已添加到 `.gitignore`，不会提交
- GitHub Secrets 加密存储，仅 Actions 可访问
- 切勿在对话中分享完整 API Key
