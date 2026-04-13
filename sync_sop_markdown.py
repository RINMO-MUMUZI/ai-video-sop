#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_HTML = ROOT / "AI视频全流程生产SOP（通用版 V 1.0）.html"
DEFAULT_PUBLIC_HTML = ROOT / "index.html"
DEFAULT_MD = ROOT / "AI视频全流程生产SOP（通用版 V 1.0）.md"

SCRIPT_TAG_RE = re.compile(
    r'(<script id="md-source" type="text/plain">)(.*?)(</script>)',
    re.DOTALL,
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def extract_markdown_from_html(html_text: str) -> str:
    match = SCRIPT_TAG_RE.search(html_text)
    if not match:
        raise ValueError("未找到 md-source 脚本块。")

    markdown = match.group(2)
    if markdown.startswith("\n"):
        markdown = markdown[1:]
    return markdown.rstrip() + "\n"


def inject_markdown_into_html(html_text: str, markdown: str) -> str:
    match = SCRIPT_TAG_RE.search(html_text)
    if not match:
        raise ValueError("未找到 md-source 脚本块。")

    normalized = markdown.rstrip()
    replacement = f"{match.group(1)}{normalized}{match.group(3)}"
    return SCRIPT_TAG_RE.sub(replacement, html_text, count=1)


def export_html_to_md(html_path: Path, md_path: Path) -> bool:
    html_text = read_text(html_path)
    markdown = extract_markdown_from_html(html_text)
    previous = md_path.read_text(encoding="utf-8") if md_path.exists() else None
    if previous == markdown:
        return False
    write_text(md_path, markdown)
    return True


def sync_md_to_html(md_path: Path, html_path: Path, template_html_text: str | None = None) -> bool:
    markdown = read_text(md_path)
    html_exists = html_path.exists()
    if html_exists:
        html_text = read_text(html_path)
    elif template_html_text is not None:
        html_text = template_html_text
    else:
        raise FileNotFoundError(f"HTML 模板不存在：{html_path}")
    new_html = inject_markdown_into_html(html_text, markdown)
    if html_exists and new_html == html_text:
        return False
    write_text(html_path, new_html)
    return True


def sync_md_to_htmls(md_path: Path, html_paths: list[Path]) -> bool:
    primary_html = html_paths[0]
    primary_template = read_text(primary_html)
    changed_any = False

    for index, html_path in enumerate(html_paths):
        template = primary_template if index > 0 else None
        changed = sync_md_to_html(md_path, html_path, template_html_text=template)
        changed_any = changed_any or changed

    return changed_any


def watch(md_path: Path, html_paths: list[Path], interval: float) -> None:
    last_mtime = None
    print(f"Watching: {md_path}")
    for html_path in html_paths:
        print(f"Updating: {html_path}")

    while True:
        try:
            current_mtime = md_path.stat().st_mtime
            if last_mtime is None:
                last_mtime = current_mtime
                changed = sync_md_to_htmls(md_path, html_paths)
                if changed:
                    print("Initial sync complete.")
            elif current_mtime != last_mtime:
                last_mtime = current_mtime
                changed = sync_md_to_htmls(md_path, html_paths)
                print("HTML files updated." if changed else "No HTML changes needed.")
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\nWatch stopped.")
            return


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="在通用版 SOP 的 Markdown 和 HTML 之间同步内容。"
    )
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML, help="HTML 文件路径")
    parser.add_argument("--md", type=Path, default=DEFAULT_MD, help="Markdown 文件路径")
    parser.add_argument(
        "--export",
        action="store_true",
        help="从 HTML 中导出当前 md-source 到 Markdown 文件",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="监听 Markdown 文件变化并自动同步到 HTML",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="watch 模式轮询间隔，默认 1 秒",
    )
    parser.add_argument(
        "--public-html",
        type=Path,
        default=DEFAULT_PUBLIC_HTML,
        help="部署用首页 HTML 文件路径，默认 index.html",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    html_path = args.html.resolve()
    public_html_path = args.public_html.resolve()
    md_path = args.md.resolve()
    html_paths = [html_path]

    if public_html_path != html_path:
        html_paths.append(public_html_path)

    if args.export and args.watch:
        print("`--export` 和 `--watch` 不能同时使用。", file=sys.stderr)
        return 1

    if args.export:
        changed = export_html_to_md(html_path, md_path)
        print("Markdown exported." if changed else "Markdown already up to date.")
        return 0

    if args.watch:
        watch(md_path, html_paths, args.interval)
        return 0

    changed = sync_md_to_htmls(md_path, html_paths)
    print("HTML files updated." if changed else "HTML already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
