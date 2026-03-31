#!/usr/bin/env python3
"""
项目验证脚本 - 检查所有组件是否正常工作
"""
import json
import os
import subprocess
import sys
from pathlib import Path

def check_python_deps():
    """检查 Python 依赖"""
    print("[1/6] 检查 Python 依赖...")
    required = ["feedparser", "requests", "bs4", "deep_translator"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace("bs4", "bs4" if pkg == "bs4" else pkg))
        except ImportError:
            missing.append(pkg)

    if missing:
        print(f"  ✗ 缺少依赖: {', '.join(missing)}")
        print(f"  运行: pip install -r requirements.txt")
        return False
    print("  ✓ 所有依赖已安装")
    return True

def check_fonts():
    """检查字体文件"""
    print("\n[2/6] 检查字体文件...")
    font_path = Path("fonts/NotoSansCJKsc-Regular.otf")
    if font_path.exists():
        print(f"  ✓ 中文字体已存在 ({font_path.stat().st_size / 1024 / 1024:.1f}MB)")
        return True
    print("  ⚠ 字体文件不存在，但 HTML 生成不需要")
    return True

def check_scripts():
    """检查脚本文件"""
    print("\n[3/6] 检查脚本文件...")
    scripts = [
        "scripts/fetch-news.py",
        "scripts/generate-all.py",
        "scripts/generate-html.py",
        "scripts/generate-rss.py",
        "scripts/generate-summary.py",
    ]
    missing = []
    for script in scripts:
        if not Path(script).exists():
            missing.append(script)

    if missing:
        print(f"  ✗ 缺少脚本: {', '.join(missing)}")
        return False
    print(f"  ✓ 所有脚本已存在")
    return True

def test_fetch():
    """测试新闻获取"""
    print("\n[4/6] 测试新闻获取...")
    try:
        result = subprocess.run(
            ["python", "scripts/fetch-news.py", "--output", "cache/test-verify.json"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"  ✗ 获取失败: {result.stderr[:200]}")
            return False

        # 检查输出
        with open("cache/test-verify.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        count = data.get("total_filtered", 0)
        if count > 0:
            print(f"  ✓ 成功获取 {count} 条新闻")
            return True
        else:
            print("  ✗ 未获取到新闻")
            return False
    except Exception as e:
        print(f"  ✗ 异常: {e}")
        return False

def test_generate():
    """测试生成功能"""
    print("\n[5/6] 测试多格式生成...")
    try:
        result = subprocess.run(
            ["python", "scripts/generate-all.py", "--input", "cache/test-verify.json",
             "--output-dir", "test-output", "--summary"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"  ✗ 生成失败: {result.stderr[:200]}")
            return False

        # 检查输出文件
        expected = ["test-output/index.html", "test-output/index.md", "test-output/rss.xml", "test-output/summary.md"]
        missing = [f for f in expected if not Path(f).exists()]

        if missing:
            print(f"  ✗ 缺少输出文件: {', '.join(missing)}")
            return False

        print(f"  ✓ 成功生成 {len(expected)} 个文件")
        return True
    except Exception as e:
        print(f"  ✗ 异常: {e}")
        return False

def test_content():
    """测试内容质量"""
    print("\n[6/6] 测试内容质量...")
    try:
        with open("cache/test-verify.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        items = data.get("items", [])
        if not items:
            print("  ✗ 没有新闻条目")
            return False

        # 检查翻译
        translated = sum(1 for item in items if "title_original" in item)
        print(f"  ✓ {translated}/{len(items)} 条已翻译")

        # 检查关键字段
        required_fields = ["title", "description", "link", "source", "relevance_score"]
        for item in items[:3]:
            for field in required_fields:
                if field not in item:
                    print(f"  ✗ 字段缺失: {field}")
                    return False

        print("  ✓ 内容结构正确")
        return True
    except Exception as e:
        print(f"  ✗ 异常: {e}")
        return False

def main():
    print("=" * 60)
    print("Daily News Workflow 验证工具")
    print("=" * 60)

    results = [
        check_python_deps(),
        check_fonts(),
        check_scripts(),
        test_fetch(),
        test_generate(),
        test_content(),
    ]

    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"验证结果: {passed}/{total} 通过")

    if all(results):
        print("✓ 项目工作正常！")
        print("\n你可以运行:")
        print("  python scripts/fetch-news.py --output cache/news.json")
        print("  python scripts/generate-all.py --input cache/news.json --output-dir docs --summary")
        return 0
    else:
        print("✗ 部分验证失败，请检查以上输出")
        return 1

if __name__ == "__main__":
    sys.exit(main())
