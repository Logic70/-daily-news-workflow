# GitHub Pages 配置指南

## 🔧 为什么出现 404？

GitHub Pages 需要手动启用，以下是完整配置步骤。

---

## 步骤 1：推送最新代码

```bash
cd /mnt/d/Code/daily-news-workflow
git add .
git commit -m "fix: update GitHub Actions workflow for Pages deployment"
git push origin main
```

---

## 步骤 2：启用 GitHub Pages（关键）

### 方法 A：通过 GitHub 网页界面

1. **访问仓库设置**
   ```
   https://github.com/Logic70/-daily-news-workflow/settings/pages
   ```

2. **选择 Source**
   - Source: **GitHub Actions**
   
   ![设置示意图](https://docs.github.com/assets/images/help/pages/publishing-source-actions.png)

3. **保存**
   - 点击 Save

### 方法 B：使用 GitHub CLI

```bash
# 安装 gh（如果未安装）
# 然后运行：
gh api repos/Logic70/-daily-news-workflow/pages \
  --method POST \
  --input - <<< '{"source":{"branch":"main","path":"/"}}'
```

---

## 步骤 3：运行 Actions 工作流

### 手动触发

1. 访问 Actions 页面
   ```
   https://github.com/Logic70/-daily-news-workflow/actions
   ```

2. 点击 **Daily News Generator**

3. 点击 **Run workflow** → **Run workflow**

   ![Run workflow](https://docs.github.com/assets/images/help/actions/workflow-dispatch.png)

### 等待自动运行

- 每天 UTC 01:00（北京时间 09:00）自动运行
- 首次启用后，首次部署可能需要 5-10 分钟

---

## 步骤 4：验证部署

### 查看部署状态

1. 访问 Actions 页面
   ```
   https://github.com/Logic70/-daily-news-workflow/actions
   ```

2. 确认最新 workflow 状态为 ✅ **绿色**

### 访问 Pages 地址

部署成功后，访问：
```
https://Logic70.github.io/-daily-news-workflow/
```

---

## 🔍 常见问题

### Q1: Actions 运行失败

**检查**: 访问 `https://github.com/Logic70/-daily-news-workflow/actions`

**常见原因**:
- API Key 未设置 → 在 Secrets 中添加 `NEWS_API_KEY`
- 权限不足 → 检查 workflow 文件中的 `permissions`

### Q2: 部署成功但 404

**解决**: 等待 5-10 分钟，GitHub Pages 需要时间来传播

**检查**: 
```
https://github.com/Logic70/-daily-news-workflow/settings/pages
```
确认显示 "Your site is live at ..."

### Q3: 自定义域名（可选）

1. 在 `docs/` 目录添加 `CNAME` 文件
2. 写入你的域名：`news.yourdomain.com`
3. 在域名 DNS 添加 CNAME 记录指向 `Logic70.github.io`

---

## ✅ 配置检查清单

```
⬜ 代码已推送到 GitHub
⬜ 访问 Settings → Pages
⬜ Source 设置为 GitHub Actions
⬜ 运行 Actions workflow
⬜ 等待部署完成（5-10分钟）
⬜ 访问 https://Logic70.github.io/-daily-news-workflow/
```

---

## 📚 相关链接

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [配置自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

---

## 🆘 需要帮助？

如果配置遇到问题，请检查：

1. **Workflow 权限**
   - Settings → Actions → General → Workflow permissions
   - 选择 "Read and write permissions"

2. **Pages 权限**
   - Settings → Pages → 确保选择 GitHub Actions

3. **仓库公开性**
   - GitHub Pages 对免费用户需要 Public 仓库
   - Private 仓库需要 GitHub Pro
