# Examples

## Sync only

```bash
python3 sync_sop_markdown.py
```

Use this when the user only asks to update local HTML from Markdown.

## Publish with one command

```bash
./publish_sop.sh "update SOP content"
```

Use this when the user wants local sync plus commit plus push.

## Manual publish

```bash
git add -- "AI视频全流程生产SOP（通用版 V 1.0）.md" "AI视频全流程生产SOP（通用版 V 1.0）.html" "index.html"
git commit -m "update SOP content"
git push origin HEAD
```

Use this when the publish script needs debugging or only part of the SOP workflow should be committed.

## First-time environment check

```bash
python3 --version
git status -sb
".tools/bin/gh" auth status
```

If `.tools/bin/gh` does not exist:

```bash
gh auth status
```
