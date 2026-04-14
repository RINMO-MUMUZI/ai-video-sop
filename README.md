# AI 视频 SOP 站点

这个仓库用于维护 `AI视频全流程生产SOP（通用版 V 1.0）` 的 Markdown 源文件、生成页面和线上发布流程。

线上地址：
- `https://rinmo-mumuzi.github.io/ai-video-sop/`

## 仓库结构

- `AI视频全流程生产SOP（通用版 V 1.0）.md`
  - 主文档源文件，日常内容修改优先改这里
- `AI视频全流程生产SOP（通用版 V 1.0）.html`
  - 主模板页面
- `index.html`
  - GitHub Pages 发布入口页
- `tutorials/`
  - 项目教程 Markdown 和对应生成页
- `sync_sop_markdown.py`
  - Markdown 同步脚本
- `publish_sop.sh`
  - 一键同步并发布脚本
- `.cursor/skills/sop-md-publish/`
  - 项目级 Cursor Skill，供团队成员直接复用

## 日常更新流程

### 1. 先改 Markdown

优先修改：

```text
AI视频全流程生产SOP（通用版 V 1.0）.md
```

如果是项目教程，则修改：

```text
tutorials/*.md
```

### 2. 同步到 HTML

运行：

```bash
python3 sync_sop_markdown.py
```

这会同步更新：
- `AI视频全流程生产SOP（通用版 V 1.0）.html`
- `index.html`
- `tutorials/*.html`

### 3. 发布到线上

推荐直接用：

```bash
./publish_sop.sh "update SOP content"
```

这个脚本会自动完成：
- Markdown 同步
- 暂存相关文件
- 提交 git
- 推送到 GitHub
- 触发 GitHub Pages 发布

## 首次环境准备

新机器或新同学第一次使用时，先检查：

- `python3`
- `git`
- GitHub CLI：优先使用 `.tools/bin/gh`，没有的话再用系统 `gh`

建议执行：

```bash
python3 --version
git status -sb
".tools/bin/gh" auth status
```

如果本地没有 `.tools/bin/gh`，改用：

```bash
gh auth status
```

如果发布脚本没有执行权限，运行：

```bash
chmod +x publish_sop.sh
```

## Cursor 用户怎么用

这个仓库内已经包含项目级 Skill：

```text
.cursor/skills/sop-md-publish/
```

其他 Cursor 用户拉下仓库后，可以直接在对话里这样说：

- “帮我同步 SOP 的 md 到 html”
- “帮我把这份 SOP 发布到线上”
- “帮我检查这个仓库的 SOP 发布环境”
- “帮我同步 tutorials 里的教程页并上线”

一般不需要手动打开 Skill 文件，Cursor 会根据请求自动命中。

如果想看 Skill 规则本身，可查看：

- `.cursor/skills/sop-md-publish/SKILL.md`
- `.cursor/skills/sop-md-publish/examples.md`

## 反馈功能

页面右下角已接入 `文档反馈` 入口。

当前使用的反馈表单为：
- `https://my.feishu.cn/share/base/form/shrcnuWLvLOvcblxKFFQavmgDE4`

如果后续需要替换表单地址，更新主模板中的反馈常量后，再重新同步：

```bash
python3 sync_sop_markdown.py
```

## 提交规范

提交时只包含 SOP 相关文件，不要顺手带上无关实验文件。

通常应提交这些内容：
- `AI视频全流程生产SOP（通用版 V 1.0）.md`
- `AI视频全流程生产SOP（通用版 V 1.0）.html`
- `index.html`
- `tutorials/*.md`
- `tutorials/*.html`
- `sync_sop_markdown.py`
- `publish_sop.sh`
- `.cursor/skills/`

不要提交无关文件，除非明确需要：
- `ocr.swift`
- `transcribe.swift`
- 大体积媒体或临时文件

## 常见问题

### 改了 Markdown，但页面没更新

先运行：

```bash
python3 sync_sop_markdown.py
```

然后用 `git diff` 检查 `html` 和 `index.html` 是否真的发生变化。

### 本地同步了，但线上没更新

同步只是本地更新。
要上线还需要：

```bash
git add
git commit
git push
```

或者直接运行：

```bash
./publish_sop.sh "your message"
```

### push 成功了，但线上还是旧内容

去看 GitHub Pages 对应的 Actions 是否执行完成。只有最新一轮 Pages workflow 成功，线上页面才会更新。
