# 安全配置指南

## API Key 安全最佳实践

### ❌ 绝对不要做的事

1. **不要将 API Key 提交到 Git**
   ```bash
   # 错误示例 ❌
   echo "API_KEY=abc123" > .env
   git add .env
   git commit -m "add api key"
   ```

2. **不要在代码中硬编码 API Key**
   ```python
   # 错误示例 ❌
   api_key = "sk-abc123..."  # 永远不要这样做！
   ```

3. **不要在日志中打印 API Key**
   ```python
   # 错误示例 ❌
   print(f"Using API key: {api_key}")  # 会泄露到日志
   ```

---

### ✅ 正确做法

#### 1. 本地开发：使用 `.env` 文件（已添加到 .gitignore）

```bash
# 复制示例文件
cp .env.example .env

# 编辑 .env，填入你的 API Key
nano .env
```

`.env` 内容示例：
```bash
NEWS_API_KEY=your_actual_key_here
```

**注意**：`.env` 已在 `.gitignore` 中，不会被提交。

#### 2. GitHub Actions：使用 Secrets

在仓库设置中添加：
1. Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `NEWS_API_KEY`
4. Value: 你的 API Key

GitHub Actions 会自动使用：
```yaml
env:
  NEWS_API_KEY: ${{ secrets.NEWS_API_KEY }}
```

#### 3. 代码中：使用环境变量

```python
import os

# 正确做法 ✅
api_key = os.getenv("NEWS_API_KEY")

if not api_key:
    print("警告: NEWS_API_KEY 未设置")
```

---

## 如果不小心泄露了 API Key

### 1. 立即撤销密钥

**NewsAPI**: https://newsapi.org/account → Regenerate API Key

**Anthropic**: https://console.anthropic.com/settings/keys → Delete & Create new

**OpenAI**: https://platform.openai.com/api-keys → Revoke & Create new

### 2. 从 Git 历史中删除

```bash
# 从 Git 历史中删除文件
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all

# 强制推送到远程（注意：这会重写历史！）
git push origin --force --all
```

### 3. 检查是否已被滥用

- 查看 API 使用量统计
- 检查是否有异常调用

---

## 项目中的安全设计

### 当前安全设计

| 组件 | 安全措施 |
|------|----------|
| `.env` | 已添加到 `.gitignore`，不会提交 |
| `.env.example` | 示例文件，不含真实密钥 |
| GitHub Actions | 使用 `secrets.NEWS_API_KEY` |
| Python 代码 | 使用 `os.getenv()` 读取 |

### 敏感文件清单

这些文件**不应该**被提交到 Git：

- [x] `.env` - 环境变量（已排除）
- [x] `cache/` - 缓存数据（已排除）
- [x] `output/` - 生成文件（已排除）
- [x] `test-output/` - 测试输出（已排除）
- [x] `logs/` - 日志文件（已排除）

---

## 验证安全配置

```bash
# 检查哪些文件会被 Git 跟踪
git status

# 检查 .env 是否在忽略列表中
git check-ignore -v .env

# 应该输出: .env is ignored
```

---

## 本地开发工作流

### 首次设置

```bash
# 1. 克隆仓库
git clone <your-repo>
cd daily-news-workflow

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 复制环境变量模板
cp .env.example .env

# 5. 编辑 .env 填入你的 API Key
# （使用编辑器，不要用 git add .env）
```

### 日常开发

```bash
# 加载环境变量
source venv/bin/activate
source .env  # 如果使用 export 语法

# 运行脚本
python scripts/fetch-news.py --output cache/news.json
```

---

## 总结

| 场景 | 安全做法 |
|------|----------|
| 本地开发 | `.env` 文件（在 .gitignore 中） |
| GitHub Actions | Secrets |
| 生产环境 | 环境变量 / Secrets Manager |
| 共享代码 | 只分享 `.env.example` |

**记住：API Key = 密码。永远不要暴露！**
