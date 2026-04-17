#!/usr/bin/env python3
"""
Download videos from YouTube, Instagram, TikTok, Facebook, Twitter, and 1000+ sites.
Powered by yt-dlp.
"""

import argparse
import json
import sys
from pathlib import Path

import yt_dlp


def get_format_selector(quality, audio_only=False):
    """Build yt-dlp format string based on quality preference."""
    if audio_only:
        return "bestaudio/best"

    if quality == "best":
        return "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

    # Limit to specific resolution
    return f"bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality}][ext=mp4]/best[height<={quality}]/best"


def list_formats(url, cookies=None):
    """List available formats for a URL."""
    opts = {
        "quiet": True,
        "no_warnings": True,
    }
    if cookies:
        opts["cookiefile"] = cookies

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

        if "entries" in info:
            info = info["entries"][0]

        print(f"\n  Title: {info.get('title', 'Unknown')}")
        print(f"  Duration: {info.get('duration_string', 'Unknown')}")
        print(f"  URL: {info.get('webpage_url', url)}\n")

        formats = info.get("formats", [])
        if not formats:
            print("  No formats found.")
            return

        print(f"  {'ID':<10} {'EXT':<6} {'RESOLUTION':<14} {'SIZE':<10} {'NOTE'}")
        print(f"  {'-'*60}")

        for f in formats:
            fid = f.get("format_id", "?")
            ext = f.get("ext", "?")
            res = f.get("resolution", "audio" if f.get("vcodec") == "none" else "?")
            size = f.get("filesize") or f.get("filesize_approx")
            size_str = f"{size / 1024 / 1024:.1f}MB" if size else "?"
            note = f.get("format_note", "")
            print(f"  {fid:<10} {ext:<6} {res:<14} {size_str:<10} {note}")

        print()


def show_metadata(url, cookies=None):
    """Show video metadata without downloading."""
    opts = {
        "quiet": True,
        "no_warnings": True,
    }
    if cookies:
        opts["cookiefile"] = cookies

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)

        if "entries" in info:
            # Playlist
            print(f"\n  Playlist: {info.get('title', 'Unknown')}")
            print(f"  Videos: {len(info['entries'])}")
            for i, entry in enumerate(info["entries"][:20]):
                if entry:
                    print(f"    [{i}] {entry.get('title', 'Unknown')} ({entry.get('duration_string', '?')})")
            if len(info["entries"]) > 20:
                print(f"    ... and {len(info['entries']) - 20} more")
        else:
            print(f"\n  Title:       {info.get('title', 'Unknown')}")
            print(f"  Channel:     {info.get('channel', info.get('uploader', 'Unknown'))}")
            print(f"  Duration:    {info.get('duration_string', 'Unknown')}")
            print(f"  Views:       {info.get('view_count', 'Unknown'):,}" if isinstance(info.get('view_count'), int) else f"  Views:       Unknown")
            print(f"  Upload date: {info.get('upload_date', 'Unknown')}")
            print(f"  URL:         {info.get('webpage_url', url)}")
            desc = info.get("description", "")
            if desc:
                print(f"  Description: {desc[:200]}{'...' if len(desc) > 200 else ''}")
        print()


def download(url, quality="best", output_dir=".", audio_only=False,
             subs=False, subs_lang="en", playlist=False, thumbnail=False,
             limit_rate=None, proxy=None, cookies=None):
    """Download video from URL."""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Output template
    outtmpl = str(output_path / "%(title)s.%(ext)s")

    format_str = get_format_selector(quality, audio_only)

    opts = {
        "format": format_str,
        "outtmpl": outtmpl,
        "noplaylist": not playlist,
        "merge_output_format": "mp4" if not audio_only else None,
        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [progress_hook],
    }

    if audio_only:
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    if subs:
        opts["writesubtitles"] = True
        opts["subtitleslangs"] = [subs_lang]
        opts["writeautomaticsub"] = True

    if thumbnail:
        opts["writethumbnail"] = True

    if limit_rate:
        opts["ratelimit"] = parse_rate(limit_rate)

    if proxy:
        opts["proxy"] = proxy

    if cookies:
        opts["cookiefile"] = cookies

    print(f"\n  Downloading...")
    print(f"  URL:     {url}")
    print(f"  Quality: {quality}")
    print(f"  Format:  {'audio (MP3)' if audio_only else 'video (MP4)'}")
    print(f"  Output:  {output_path}/\n")

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        print(f"\n  Done!\n")
    except yt_dlp.utils.DownloadError as e:
        print(f"\n  Download failed: {e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n  Error: {e}\n")
        sys.exit(1)


def progress_hook(d):
    """Show download progress."""
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "?%").strip()
        speed = d.get("_speed_str", "?").strip()
        eta = d.get("_eta_str", "?").strip()
        print(f"\r  {pct} at {speed} ETA {eta}    ", end="", flush=True)
    elif d["status"] == "finished":
        size = d.get("_total_bytes_str", d.get("total_bytes_str", "?"))
        print(f"\r  Downloaded {size}                    ")


def parse_rate(rate_str):
    """Parse rate limit string like '1M' or '500K' to bytes."""
    rate_str = rate_str.upper().strip()
    if rate_str.endswith("M"):
        return int(float(rate_str[:-1]) * 1024 * 1024)
    elif rate_str.endswith("K"):
        return int(float(rate_str[:-1]) * 1024)
    return int(rate_str)


def main():
    parser = argparse.ArgumentParser(description="Download videos from 1000+ sites")
    parser.add_argument("--url", type=str, required=True, help="Video URL")
    parser.add_argument("--quality", type=str, default="best", help="Video quality")
    parser.add_argument("--output", type=str, default=".", help="Output directory")
    parser.add_argument("--audio-only", action="store_true", help="Download audio only")
    parser.add_argument("--formats", action="store_true", help="List available formats")
    parser.add_argument("--metadata", action="store_true", help="Show metadata only")
    parser.add_argument("--subs", action="store_true", help="Download subtitles")
    parser.add_argument("--subs-lang", type=str, default="en", help="Subtitle language")
    parser.add_argument("--playlist", action="store_true", help="Download entire playlist")
    parser.add_argument("--thumbnail", action="store_true", help="Download thumbnail")
    parser.add_argument("--limit-rate", type=str, help="Limit download speed")
    parser.add_argument("--proxy", type=str, help="Proxy URL")
    parser.add_argument("--cookies", type=str, help="Cookies file path")
    args = parser.parse_args()

    if args.formats:
        list_formats(args.url, args.cookies)
        return

    if args.metadata:
        show_metadata(args.url, args.cookies)
        return

    download(
        url=args.url,
        quality=args.quality,
        output_dir=args.output,
        audio_only=args.audio_only,
        subs=args.subs,
        subs_lang=args.subs_lang,
        playlist=args.playlist,
        thumbnail=args.thumbnail,
        limit_rate=args.limit_rate,
        proxy=args.proxy,
        cookies=args.cookies,
    )


if __name__ == "__main__":
    main()
