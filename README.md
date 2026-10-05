# API Downloader

A small Python utility that downloads videos from Holodex and configurable YouTube sources using yt-dlp.

## Features

- Fetches recent past Holodex streams using the Holodex API
- Downloads each video to the configured output directory
- Supports additional YouTube channel and playlist downloaders
- Applies yt-dlp formatting and filtering options
- Removes existing media files from each downloader destination before downloading

## Project structure

- `autodl.py` — main download script
- `yt-dlp` — bundled yt-dlp executable
- `etc/apikey` — Holodex API key
- `etc/args.json` — downloader and yt-dlp configuration
- `output/` — downloader output directory

## Requirements

- Python 3
- The `requests` package
- Access to the Holodex API

Install the Python dependency with:

```bash
python3 -m pip install requests
```

## Configuration

### Holodex API key

Create `etc/apikey` and put your Holodex API key in it:

```text
your-api-key
```

### Downloader options

Configure the script in `etc/args.json`:

```json
{
  "ytdlp": ["-S res:480"],
  "holodex": "org=Hololive&order=desc&status=past&type=stream",
  "outputdir": "/path/to/downloads/",
  "autodel": true,
  "ytdlp_downloaders": [
    {
      "url": "https://www.youtube.com/@channel/streams",
      "playlist-items": "1-10",
      "match-filter": "!is_live & live_status!=is_upcoming",
      "dir": "output/"
    }
  ]
}
```

Settings:

- `ytdlp`: Additional arguments passed to yt-dlp.
- `holodex`: Query string used for the Holodex API request.
- `outputdir`: Directory used by the main Holodex downloader.
- `autodel`: Enables pre-download cleanup of media files in downloader destinations.
- `ytdlp_downloaders`: Additional YouTube sources to download.
- `url`: YouTube channel, playlist, or another yt-dlp-supported URL.
- `playlist-items`: Optional playlist item selector, such as `1`, `1-10`, or `NOOP`.
- `match-filter`: Optional yt-dlp match filter, or `NOOP` to disable it.
- `dir`: Destination directory for the downloader.

> `--playlist-items` and `--match-filters` are passed as separate arguments to yt-dlp.

## Usage

From the project directory, run:

```bash
python3 autodl.py
```

The script uses the bundled `./yt-dlp` executable on macOS. On other platforms, it uses the `yt-dlp` command from `PATH`.

Before each configured downloader run, existing media files in its destination directory are deleted. The cleanup only removes supported video file extensions and leaves directories untouched.

## Notes

- The script does not currently validate the API key or configuration file.
- It will download only the configured Holodex streams and YouTube sources.
- Do not commit your API key or private configuration.
- Check the Holodex API documentation and your account permissions before using the API.
