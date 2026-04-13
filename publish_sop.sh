#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MD_FILE="AI视频全流程生产SOP（通用版 V 1.0）.md"
HTML_FILE="AI视频全流程生产SOP（通用版 V 1.0）.html"
PUBLIC_HTML_FILE="index.html"
SYNC_SCRIPT="sync_sop_markdown.py"

COMMIT_MESSAGE="${1:-update SOP site}"

cd "$ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "未找到 python3，请先安装后再运行。"
  exit 1
fi

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "当前目录不是 Git 仓库，无法发布。"
  exit 1
fi

python3 "$SYNC_SCRIPT" --md "$MD_FILE" --html "$HTML_FILE" --public-html "$PUBLIC_HTML_FILE"

if [[ -z "$(git status --short -- "$MD_FILE" "$HTML_FILE" "$PUBLIC_HTML_FILE")" ]]; then
  echo "SOP 内容没有变化，无需发布。"
  exit 0
fi

git add -- "$MD_FILE" "$HTML_FILE" "$PUBLIC_HTML_FILE"

if git diff --cached --quiet -- "$MD_FILE" "$HTML_FILE" "$PUBLIC_HTML_FILE"; then
  echo "没有可提交的 SOP 变更。"
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"
git push origin HEAD

echo "发布完成。"
echo "站点地址：https://rinmo-mumuzi.github.io/ai-video-sop/"
