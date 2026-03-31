# Daily News Workflow - Test Scenarios

来源: 2026-03-31 /develop Stage 5 运行时验证

## 复杂度级别: M (5分钟超时)

## 测试场景

### 场景 1: Happy Path

**输入**: `/daily-news --date 2026-03-31`

**预期流程**:
1. Stage 1: 3个Collector并行执行，至少2个成功返回
2. Stage 2: Content Filter筛选出≤20条新闻
3. Stage 3: PDF Generator生成有效PDF文件
4. Stage 4: Quality Check全部PASS

**验证点**:
- [ ] PDF文件存在: `output/tech-news-digest-2026-03-31.pdf`
- [ ] 文件大小 > 0 且 < 10MB
- [ ] 文件可正常打开
- [ ] 包含日期页眉
- [ ] 包含≥5条新闻

### 场景 2: Edge Case - 单数据源

**输入**: `/daily-news --sources rss`

**预期**: 仅使用RSS源，仍能正常生成PDF

**验证点**:
- [ ] 仅RSS源被使用
- [ ] 新闻条目数可能较少但仍≥5
- [ ] PDF正常生成

### 场景 3: Error Case - 网络故障

**输入**: `/daily-news` (模拟断网环境)

**预期**: Stage 1失败，重试2次后报告错误

**验证点**:
- [ ] 错误信息清晰
- [ ] 不生成空/损坏的PDF
- [ ] 返回非零退出码

### 场景 4: Error Case - API配额耗尽

**输入**: `/daily-news` (模拟NewsAPI配额耗尽)

**预期**: API Collector失败，但RSS和Web继续，最终仍能生成PDF

**验证点**:
- [ ] API错误被记录但不阻塞流程
- [ ] 部分数据仍能生成PDF

### 场景 5: Quality Gate Failure

**输入**: `/daily-news --date 2020-01-01` (旧日期，可能没有新闻)

**预期**: Stage 4质量检查失败（条目数<5）

**验证点**:
- [ ] 明确报告质量检查失败
- [ ] 给出失败原因（条目不足）
- [ ] 不输出不合格PDF

## 验证检查清单

### 文件检查
- [ ] `.claude/settings.json` 格式正确
- [ ] `.claude/commands/daily-news.md` 存在
- [ ] `.claude/skills/daily-news/SKILL.md` 存在
- [ ] 6个Agent文件存在
- [ ] Python脚本语法正确

### 功能检查
- [ ] `/daily-news` 命令可识别
- [ ] `--date` 参数有效
- [ ] `--output-dir` 参数有效
- [ ] 依赖安装脚本可用

### 输出检查
- [ ] PDF格式正确
- [ ] 中文显示正常
- [ ] 链接可点击
- [ ] 页眉页脚正确

## 运行时验证步骤

1. 安装依赖: `pip install -r requirements.txt && playwright install chromium`
2. 运行Happy Path: `python scripts/fetch-news.py --output /tmp/test-news.json`
3. 生成PDF: `python scripts/generate-pdf.py --input /tmp/test-news.json --output /tmp/test.pdf`
4. 验证PDF: 检查文件大小、内容完整性
5. 运行完整工作流: `/daily-news --date 2026-03-31`

## 已知限制

- NewsAPI需要API密钥
- 某些RSS源可能有访问限制
- PDF生成依赖Playwright和Chromium
