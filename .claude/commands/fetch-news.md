# /fetch-news

手动触发新闻收集，支持本地运行和指定参数。

## Usage

```text
/fetch-news [--date YYYY-MM-DD] [--sources rss,api,github,hf] [--output PATH]
```

## Stage 1: 环境检查

**Goal**: 确保运行环境就绪

**Steps**:
1. 检查 Python 虚拟环境是否激活
2. 验证 `.env` 文件存在（可选）
3. 检查依赖是否安装

**Verify**:
- [ ] Python 3.9+ 可用
- [ ] 依赖包已安装
- [ ] cache/ 目录可写

## Stage 2: 新闻收集

**Goal**: 从指定源收集新闻

**Steps**:
1. 运行 `scripts/fetch-news.py`
2. 传递 `--date` 和 `--sources` 参数
3. 输出到 cache/daily-news.json

**Verify**:
- [ ] 输出文件生成
- [ ] 包含新闻条目
- [ ] JSON 格式有效

## Stage 3: 生成预览

**Goal**: 生成可读的 Markdown 预览

**Steps**:
1. 运行 `scripts/generate-all.py --summary`
2. 生成 docs/index.md 预览

**Verify**:
- [ ] Markdown 文件生成
- [ ] 中文显示正常

## Output

- `cache/daily-news.json` - 原始数据
- `docs/index.md` - 预览文件
