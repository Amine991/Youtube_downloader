# Youtube_downloader

Download a YouTube video or a whole playlist as TV-friendly MP4 files (H.264 + AAC), ready to copy to a USB stick for an older TV.

## Requirements

- Python 3
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): `python -m pip install -U yt-dlp`
- [ffmpeg](https://ffmpeg.org/) on PATH: `winget install Gyan.FFmpeg`

## Usage

```
python yt_playlist.py "<video or playlist url>" -q 480 -o E:\Videos
```

| Option | Description |
|---|---|
| `-q {360,480,720,1080}` | Max video height (default 720) |
| `-o DIR` | Output folder (default `./downloads`) |
| `--start N` / `--end N` | Only download playlist items N..M |
| `--single` | Download only the video if the URL also has a playlist |
| `--no-number` | Don't prefix filenames with the playlist position |

Files are saved as `001 - Title.mp4` inside a folder named after the playlist. Re-running the same command resumes: finished videos are skipped.

On Windows you can also double-click `download.bat` and paste the URL.
