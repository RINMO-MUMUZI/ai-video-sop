---
name: sop-md-publish
description: Maintain and publish the SOP site from Markdown sources. Use when updating `AI视频全流程生产SOP（通用版 V 1.0）.md`, syncing Markdown to HTML/index/tutorial pages, preparing the environment for new Cursor users, or committing and pushing SOP site changes online.
---

# SOP Markdown Sync And Publish

## Use This Skill When
- The user wants to edit the SOP in Markdown and sync it to HTML.
- The user asks to publish the SOP site online.
- A new Cursor user needs the local environment prepared for this workflow.
- The user mentions `sync_sop_markdown.py`, `publish_sop.sh`, `index.html`, `tutorials/`, GitHub Pages, or “同步并发布”.

## Project Files
- Main source: `AI视频全流程生产SOP（通用版 V 1.0）.md`
- Main template: `AI视频全流程生产SOP（通用版 V 1.0）.html`
- Deploy entry: `index.html`
- Tutorial sources: `tutorials/*.md`
- Tutorial pages: `tutorials/*.html`
- Sync script: `sync_sop_markdown.py`
- Publish script: `publish_sop.sh`

## Environment Prep
Run these checks before the first publish on a new machine:

1. Verify required tools:
   - `python3`
   - `git`
   - GitHub CLI: prefer `.tools/bin/gh`, otherwise `gh`
2. Verify the workspace is a git repo and has an `origin` remote.
3. Verify GitHub auth is ready:
   - `".tools/bin/gh" auth status` if local binary exists
   - otherwise `gh auth status`
4. If `publish_sop.sh` is not executable, run:

```bash
chmod +x publish_sop.sh
```

Default CLI preference in this repo:
- Use `.tools/bin/gh` when it exists.
- Fall back to `gh` when `.tools/bin/gh` does not exist.

## Standard Workflow

### 1. Edit Markdown First
Make content changes in:

```text
AI视频全流程生产SOP（通用版 V 1.0）.md
```

Only edit HTML directly when changing page structure, styling, or client-side behavior.

### 2. Sync Markdown To Generated Pages
After Markdown changes, run:

```bash
python3 sync_sop_markdown.py
```

This should update:
- `AI视频全流程生产SOP（通用版 V 1.0）.html`
- `index.html`
- `tutorials/*.html`

### 3. Verify Before Publish
Check only relevant SOP files:

```bash
git status --short
git diff -- "AI视频全流程生产SOP（通用版 V 1.0）.md" "AI视频全流程生产SOP（通用版 V 1.0）.html" "index.html"
```

Also include these when changed:
- `sync_sop_markdown.py`
- `publish_sop.sh`
- `tutorials/*.md`
- `tutorials/*.html`
- `.cursor/skills/sop-md-publish/*`

Never include unrelated files like OCR or experiment files unless the user explicitly asks.

### 4. Publish
Preferred one-command flow:

```bash
./publish_sop.sh "your commit message"
```

If the script needs troubleshooting or a custom staged set, do it manually:

```bash
git add -- <relevant files>
git commit -m "message"
git push origin HEAD
```

### 5. Confirm Online Status
After pushing, verify GitHub Pages:
- check recent Actions runs
- confirm the latest Pages deploy succeeded
- return the public site URL

Current public site:
- `https://rinmo-mumuzi.github.io/ai-video-sop/`

## Publishing Rules
- Commit only files related to the SOP workflow.
- Keep Markdown and generated HTML in sync before every publish.
- If the main template changes, make sure `index.html` and tutorial pages regenerate correctly.
- Do not revert unrelated user changes.
- Do not commit `ocr.swift`, `transcribe.swift`, large media, or scratch files unless explicitly requested.

## Troubleshooting

### HTML did not update
Run:

```bash
python3 sync_sop_markdown.py
```

Then verify the generated files actually changed with `git diff`.

### `index.html` is out of sync with the template
Re-run the sync script. In this repo, `sync_sop_markdown.py` should regenerate `index.html` from the main HTML template structure, not just replace Markdown content.

### GitHub CLI not found
Use `.tools/bin/gh` if available. Otherwise use `gh`.

### Push succeeded but site looks old
Check GitHub Pages workflow status. Wait for the latest run to finish before concluding the deploy failed.

### Feedback panel or tutorial page missing online
Confirm these files were included in the commit:
- `AI视频全流程生产SOP（通用版 V 1.0）.html`
- `index.html`
- `tutorials/*.html`
- any template or script file required to regenerate them

## Response Style
When using this skill:
- Prefer concise status updates.
- Tell the user whether you only synced locally or also published online.
- If publishing failed, say whether the failure happened during auth, commit, push, or Pages deploy.

## Additional Resource
- For example command sequences, see [examples.md](examples.md).
