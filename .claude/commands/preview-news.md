# /preview-news

预览今天或指定日期的新闻，快速查看内容质量。

## Usage

```text
/preview-news [--date YYYY-MM-DD] [--limit N]
```

## Stage 1: 检查数据源

**Goal**: 确定数据来源

**Steps**:
1. 检查 cache/daily-news.json 是否存在
2. 如果不存在，询问是否先运行 /fetch-news

## Stage 2: 格式化输出

**Goal**: 以可读格式展示新闻列表

**Steps**:
1. 读取 JSON 数据
2. 按 relevance_score 排序
3. 格式化为 Markdown 表格

**Output Format**:

```markdown
| 排名 | 标题 | 来源 | 评分 |
|------|------|------|------|
| 1 | ... | TechCrunch | 0.95 |
```

## Stage 3: 摘要展示

**Goal**: 展示前 N 条新闻的详细摘要

**Steps**:
1. 显示新闻标题和摘要
2. 提供原文链接
3. 标注翻译状态

## Output

直接在对话中显示新闻预览，不生成文件。
