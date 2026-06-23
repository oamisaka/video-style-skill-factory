# Video Style Skill Factory

从视频或视频主提炼文案风格，并生成可迁移的 Codex 写作 Skill。

Video Style Skill Factory 是一个 Codex 母 Skill。它可以从参考视频、视频合集、频道或视频主中提取字幕或音频转写内容，总结出可迁移的文案风格卡，然后生成一个独立的、研究优先的文案写作 Skill。

生成出来的风格 Skill 不依赖原视频链接、字幕、音频或完整 transcript，只保留风格卡、研究流程、写作流程、输出格式和安全边界。也就是说，一个风格可以对应一个独立 Skill，方便迁移、复用和继续改造。

## 这个项目能做什么

- 根据单个视频、合集、频道或视频主，提炼可复用的文案风格。
- 优先抓取字幕；没有字幕时，下载音频并准备转写请求。
- 生成一个独立的风格专属 Codex Skill。
- 让生成后的 Skill 支持“只给主题或问题，就先研究再写文案”。
- 附带一个生成结果示例和一篇展示文案。

## 这个项目不做什么

- 不保存完整字幕库。
- 不保存原始音频或视频。
- 不鼓励冒充任何创作者本人。
- 不暗示示例中出现的创作者、频道或品牌认可本项目。
- 不把原视频文案长段复制进生成的 Skill。

## 仓库结构

```text
video-style-skill-factory/
  create-video-style-skill/
    SKILL.md
    agents/openai.yaml
    scripts/
      fetch_video_text.py
      init_style_skill.py
    references/
      style-card-schema.md
  examples/
    yingshi-jufeng-copywriter/
      SKILL.md
      agents/openai.yaml
    outputs/
      benda-black-flag-600-yingshi-jufeng-script.md
  LICENSE
  README.md
```

## 工作流程

1. 用户提供视频 URL、合集 URL、频道 URL 或视频主 URL。
2. 母 Skill 使用 `yt_dlp` 抓取字幕或自动字幕。
3. 如果没有字幕，则下载音频并生成 `transcription_request.json`。
4. Codex 根据临时 transcript 提炼风格卡。
5. 用户确认风格卡、Skill 名称、适用范围和禁忌点。
6. 母 Skill 生成一个独立的风格专属写作 Skill。
7. 生成后的 Skill 可以根据主题、问题、产品、趋势、粗略方向或大纲，先研究互联网资料，再生成中文视频文案。

## 安装方式

把 `create-video-style-skill/` 复制到你的 Codex skills 目录。

常见路径：

```text
~/.codex/skills/create-video-style-skill
```

Windows 常见路径：

```text
C:\Users\<you>\.codex\skills\create-video-style-skill
```

然后在 Codex 中这样调用：

```text
Use $create-video-style-skill to learn a creator's video style from this URL and create a reusable copywriting skill.
```

## 依赖

- 支持 Skill 的 Codex 环境。
- Python 3.10 或更高版本。
- Python 包 `yt_dlp`，或当前 Python 环境中可用的 `yt-dlp` 能力。
- 当字幕不可用时，需要一个转写方案，例如 Whisper。

## 示例

`examples/yingshi-jufeng-copywriter/` 是一个生成出来的风格 Skill 示例，用来展示最终产物的结构。

`examples/outputs/benda-black-flag-600-yingshi-jufeng-script.md` 是这个示例 Skill 生成的一篇展示文案。

示例文案中的时间敏感信息，例如价格、发售状态、参数和技术规格，在正式发布前都应该重新核对最新来源。

## 安全与版权边界

- transcript 应该只作为临时分析材料。
- 不要把完整字幕或长段原文写入生成的 Skill。
- 提炼的是风格规律，不是复制原文。
- 生成的 Skill 不应声称自己是原创作者本人。
- 生成的文案不应暗示原创作者或品牌背书。
- 示例中的创作者名称只用于说明风格来源，不代表关联、授权或认可。

## English Summary

Video Style Skill Factory creates portable Codex copywriting skills from video or creator styles.

It extracts or prepares transcript material, summarizes transferable style patterns, and generates one independent research-first copywriting skill per style. The generated skills can write new Chinese video scripts from only a topic, question, product, trend, rough direction, or outline.

The repository includes the parent skill, a generated example skill, and an example output script. It does not include original subtitles, audio, videos, or full transcripts.

## License

MIT. See `LICENSE`.
