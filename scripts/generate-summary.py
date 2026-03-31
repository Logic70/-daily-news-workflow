#!/usr/bin/env python3
"""
AI 总结生成器 - 生成每日要点和分类
"""
import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def generate_summary_simple(news_data):
    """简单规则总结（无需 API）"""
    items = news_data.get("items", [])

    # 按实体分类
    categories = {
        "AI/大模型": [],
        "科技巨头": [],
        "硬件/设备": [],
        "开发者工具": [],
        "其他": []
    }

    for item in items:
        title = item.get("title", "").lower()
        entities = [e.lower() for e in item.get("entities", [])]

        if any(kw in title for kw in ['ai', 'gpt', 'llm', '模型', 'openai', 'claude', 'huggingface']):
            categories["AI/大模型"].append(item)
        elif any(kw in title for kw in ['apple', 'google', 'amazon', 'meta', 'microsoft', '字节', '阿里', '腾讯']):
            categories["科技巨头"].append(item)
        elif any(kw in title for kw in ['硬件', '设备', 'phone', 'laptop', 'chip']):
            categories["硬件/设备"].append(item)
        elif "github" in title or "开源" in title:
            categories["开发者工具"].append(item)
        else:
            categories["其他"].append(item)

    # 生成总结
    summary_lines = [f"## 今日科技要点 ({len(items)} 条)\n"]

    # 关键发现
    top_items = sorted(items, key=lambda x: x.get("relevance_score", 0), reverse=True)[:3]
    summary_lines.append("### 🔥 关键发现\n")
    for item in top_items:
        summary_lines.append(f"- **{item.get('title', '')}** ({item.get('source', '')})")
    summary_lines.append("")

    # 分类汇总
    summary_lines.append("### 📊 分类汇总\n")
    for cat, cat_items in categories.items():
        if cat_items:
            summary_lines.append(f"- **{cat}**: {len(cat_items)} 条")
    summary_lines.append("")

    # 每个分类的简要内容
    for cat, cat_items in categories.items():
        if cat_items:
            summary_lines.append(f"\n### {cat}\n")
            for item in cat_items[:5]:  # 每类最多5条
                title = item.get("title", "")
                summary_lines.append(f"- {title}")

    return "\n".join(summary_lines)


def generate_summary_with_llm(news_data, api_provider="anthropic"):
    """使用 LLM API 生成智能总结"""
    items = news_data.get("items", [])

    # 准备新闻文本
    news_text = "\n\n".join([
        f"{i+1}. {item.get('title', '')} (来源: {item.get('source', '')})\n{item.get('description', '')[:200]}"
        for i, item in enumerate(items)
    ])

    prompt = f"""请根据以下科技新闻，生成一份简洁的每日科技早报总结：

要求：
1. 用中文输出
2. 首先列出 3-5 条"今日关键发现"
3. 将新闻按主题分类（如：AI/大模型、科技巨头、开发者工具等）
4. 每个分类下简要列出相关新闻标题
5. 最后添加一句"今日观察"（对整个科技行业趋势的一句话点评）

新闻内容：
{news_text}
"""

    if api_provider == "anthropic":
        return _call_anthropic(prompt)
    elif api_provider == "openai":
        return _call_openai(prompt)
    else:
        return generate_summary_simple(news_data)


def _call_anthropic(prompt):
    """调用 Anthropic API"""
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Anthropic API 调用失败: {e}")
        return None


def _call_openai(prompt):
    """调用 OpenAI API"""
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API 调用失败: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="生成 AI 总结")
    parser.add_argument("--input", required=True, help="输入JSON")
    parser.add_argument("--output", required=True, help="输出Markdown")
    parser.add_argument("--llm", choices=["simple", "anthropic", "openai"], default="simple",
                        help="总结方式")
    args = parser.parse_args()

    print("=" * 50)
    print("AI 总结生成器")
    print("=" * 50)

    # 读取数据
    with open(args.input, "r", encoding="utf-8") as f:
        news_data = json.load(f)

    print(f"\n读取: {len(news_data.get('items', []))} 条新闻")
    print(f"模式: {args.llm}")

    # 生成总结
    if args.llm == "simple":
        summary = generate_summary_simple(news_data)
    else:
        summary = generate_summary_with_llm(news_data, args.llm)
        if summary is None:
            print("⚠ LLM 调用失败，使用简单总结")
            summary = generate_summary_simple(news_data)

    # 保存
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# 科技新闻早报\n\n")
        f.write(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write(summary)

    print(f"\n✓ 总结生成: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
