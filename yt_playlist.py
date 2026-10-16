#!/usr/bin/env python3
"""
Download a YouTube video or a whole playlist as TV-friendly MP4 files
(H.264 video + AAC audio), ready to copy to a USB stick for an older TV.

Usage:
    python yt_playlist.py "<url>"                       # 720p, ./downloads/<playlist name>/
    python yt_playlist.py "<url>" -q 1080               # up to 1080p
    python yt_playlist.py "<url>" -q 480 -o E:\\Videos   # smaller files, straight to the USB drive
    python yt_playlist.py "<url>" --start 5 --end 10    # only videos 5..10 of the playlist

Requires: yt-dlp (pip install yt-dlp) and ffmpeg on PATH.
"""
import argparse
import glob
import os
import shutil
import sys

try:
    import yt_dlp
except ImportError:
    sys.exit("yt-dlp is missing. Install it with:  python -m pip install -U yt-dlp")


def find_ffmpeg():
    """Return the folder containing ffmpeg, or None. Also checks winget's install location,
    since a terminal opened before the install may not have it on PATH yet."""
    if shutil.which("ffmpeg"):
        return None  # already on PATH, yt-dlp will find it
    local = os.environ.get("LOCALAPPDATA", "")
    pattern = os.path.join(local, "Microsoft", "WinGet", "Packages", "Gyan.FFmpeg*", "**", "bin", "ffmpeg.exe")
    hits = glob.glob(pattern, recursive=True)
    if hits:
        return os.path.dirname(hits[0])
    sys.exit("ffmpeg not found. Install it with:  winget install Gyan.FFmpeg  (then reopen the terminal)")


def build_format(quality):
    # Prefer H.264 (avc1) + AAC (mp4a): the codec combo almost every TV supports.
    # Falls back to a pre-merged MP4. VP9/AV1 are deliberately excluded: many TVs can't play them.
    h = f"[height<={quality}]"
    return (
        f"bv*[vcodec^=avc1]{h}+ba[acodec^=mp4a]"
        f"/bv*[vcodec^=avc1]{h}+ba"
        f"/b[ext=mp4]{h}"
    )


def main():
    p = argparse.ArgumentParser(description="Download YouTube videos/playlists as TV-compatible MP4.")
    p.add_argument("url", help="Video or playlist URL")
    p.add_argument("-o", "--output", default="downloads", help="Output folder (default: ./downloads)")
    p.add_argument("-q", "--quality", type=int, default=720, choices=[360, 480, 720, 1080],
                   help="Max video height (default 720; old TVs are safest at 720 or lower)")
    p.add_argument("--start", type=int, help="First playlist item to download")
    p.add_argument("--end", type=int, help="Last playlist item to download")
    p.add_argument("--single", action="store_true",
                   help="If the URL has both a video and a playlist, download only that video")
    p.add_argument("--no-number", action="store_true", help="Don't prefix files with the playlist position")
    args = p.parse_args()

    # Numbered prefix keeps the playback order correct on TVs that sort by filename.
    is_playlist = "list=" in args.url and not args.single
    name = "%(playlist_index)03d - %(title).100B.%(ext)s" if is_playlist and not args.no_number         else "%(title).100B.%(ext)s"
    outtmpl = os.path.join(args.output, "%(playlist_title|)s", name)

    opts = {
        "format": build_format(args.quality),
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "noplaylist": args.single,
        "ignoreerrors": True,          # skip private/deleted videos instead of aborting
        "windowsfilenames": True,      # strip characters FAT32/exFAT USB sticks can't store
        "download_archive": os.path.join(args.output, ".downloaded.txt"),  # resume: skip finished videos
        "retries": 10,
        "fragment_retries": 10,
        "concurrent_fragment_downloads": 4,
        "ffmpeg_location": find_ffmpeg(),
    }
    if args.start:
        opts["playliststart"] = args.start
    if args.end:
        opts["playlistend"] = args.end

    os.makedirs(args.output, exist_ok=True)
    with yt_dlp.YoutubeDL(opts) as ydl:
        rc = ydl.download([args.url])
    print("\nDone. Files are in:", os.path.abspath(args.output))
    return rc


if __name__ == "__main__":
    sys.exit(main())
