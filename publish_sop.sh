#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

MD_FILE="AI视频全流程生产SOP（通用版 V 1.0）.md"
HTML_FILE="AI视频全流程生产SOP（通用版 V 1.0）.html"
PUBLIC_HTML_FILE="index.html"
SYNC_SCRIPT="sync_sop_markdown.py"
TUTORIALS_DIR="tutorials"

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

shopt -s nullglob

FILES_TO_TRACK=(
  "$MD_FILE"
  "$HTML_FILE"
  "$PUBLIC_HTML_FILE"
  "$SYNC_SCRIPT"
  "${BASH_SOURCE[0]##*/}"
)

if [[ -d "$TUTORIALS_DIR" ]]; then
  for file in "$TUTORIALS_DIR"/*.md "$TUTORIALS_DIR"/*.html; do
    FILES_TO_TRACK+=("$file")
  done
fi

if [[ -z "$(git status --short -- "${FILES_TO_TRACK[@]}")" ]]; then
  echo "SOP 内容没有变化，无需发布。"
  exit 0
fi

git add -- "${FILES_TO_TRACK[@]}"

if git diff --cached --quiet -- "${FILES_TO_TRACK[@]}"; then
  echo "没有可提交的 SOP 变更。"
  exit 0
fi

git commit -m "$COMMIT_MESSAGE"
git push origin HEAD

echo "发布完成。"
echo "站点地址：https://rinmo-mumuzi.github.io/ai-video-sop/"
