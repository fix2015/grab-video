# download-video

> Download videos from YouTube, Instagram, TikTok, Facebook, Twitter, and 1000+ sites — one command.

[![npm version](https://img.shields.io/npm/v/download-video.svg)](https://www.npmjs.com/package/download-video)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Powered by yt-dlp. Free and unlimited. No API key needed.

## Quick Start

```bash
npx download-video "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

## Prerequisites

- **Node.js** >= 14
- **Python 3** with pip (yt-dlp auto-installs on first run)

## Usage

### Download video

```bash
# YouTube
npx download-video "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Instagram
npx download-video "https://www.instagram.com/reel/ABC123/"

# TikTok
npx download-video "https://www.tiktok.com/@user/video/123456"

# Facebook
npx download-video "https://www.facebook.com/watch?v=123456"

# Twitter / X
npx download-video "https://x.com/user/status/123456"

# Telegram
npx download-video "https://t.me/channel/123"

# Reddit
npx download-video "https://reddit.com/r/sub/comments/abc123/title/"
```

### Choose quality

```bash
npx download-video "URL" --quality 720
npx download-video "URL" --quality 1080
npx download-video "URL" --quality 360    # Save bandwidth
npx download-video "URL" --quality best   # Default
```

### Audio only (MP3)

```bash
npx download-video "URL" --audio-only
```

### Save to folder

```bash
npx download-video "URL" --output ./downloads/
```

### Download playlist

```bash
npx download-video "https://youtube.com/playlist?list=PLxxx" --playlist
```

### Download with subtitles

```bash
npx download-video "URL" --subs
npx download-video "URL" --subs --subs-lang es    # Spanish
```

### List formats

```bash
npx download-video "URL" --formats
```

### Show metadata

```bash
npx download-video "URL" --metadata
```

### Download thumbnail

```bash
npx download-video "URL" --thumbnail
```

### Rate limiting

```bash
npx download-video "URL" --limit-rate 1M     # 1 MB/s max
npx download-video "URL" --limit-rate 500K    # 500 KB/s max
```

### Private / age-restricted videos

```bash
npx download-video "URL" --cookies ./cookies.txt
```

### Update yt-dlp

```bash
npx download-video update
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-q, --quality <res>` | Max quality: 360, 480, 720, 1080, 1440, 2160, best | `best` |
| `-o, --output <path>` | Output directory | `.` |
| `-a, --audio-only` | Download audio as MP3 | — |
| `-f, --formats` | List available formats | — |
| `-s, --subs` | Download subtitles | — |
| `--subs-lang <lang>` | Subtitle language | `en` |
| `--playlist` | Download entire playlist | — |
| `--thumbnail` | Download thumbnail image | — |
| `--metadata` | Show video info without downloading | — |
| `--limit-rate <rate>` | Limit download speed (1M, 500K) | — |
| `--proxy <url>` | Use proxy | — |
| `--cookies <file>` | Cookies file for private videos | — |

## Supported Sites

YouTube, Instagram, TikTok, Facebook, Twitter/X, Telegram, Reddit, Vimeo, Twitch, Dailymotion, SoundCloud, Bandcamp, Bilibili, LinkedIn, Pinterest, VK, and 1000+ more.

Full list: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

```bash
npx download-video sites
```

## How It Works

Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp), the most maintained fork of youtube-dl. Supports 1000+ sites, active development, regular updates.

## License

MIT
