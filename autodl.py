import requests;
import subprocess;
import sys;
import ast;
import json;
from pathlib import Path

def delete_movie_files(directory):
    """Delete existing downloaded movie files from a directory."""
    target_dir = Path(directory)
    media_extensions = {".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".webm", ".wmv"}
    if (autodel):
        for file_path in target_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in media_extensions:
                file_path.unlink()
                print(f"Deleted existing movie file: {file_path}")


print("Hello, this is autodl.py!")


def delete_movie_files(directory):
    """Delete existing downloaded movie files from a directory."""
    target_dir = Path(directory)
    if not target_dir.exists():
        return

    media_extensions = {".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".mpeg", ".mpg", ".webm", ".wmv"}
    for file_path in target_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in media_extensions:
            file_path.unlink()
            print(f"Deleted existing movie file: {file_path}")


#Default Arguments for yt-dlp and output directory if args file is not found
args_ytdlp = None
args_ytdlp = ["-S res:480"]
outputdir = "output/"
holodex_args = "org=Hololive&order=desc&status=past&type=stream"
autodel = False
holodex_enabled = True

print("Fetching Holodex API Key...")
with open("etc/apikey", "r") as f:
    api_key = f.read().strip()
print("Fetching Arguments...")
with open("etc/args.json", "r") as f:
    args = json.load(f)
    args_ytdlp = args["ytdlp"]
    outputdir = args["outputdir"]
    holodex_args = args["holodex"]
    ytdlp_downloaders = args["ytdlp_downloaders"]
    autodel = args["autodel"]
    holodex_enabled = args["holodex_enabled"]


if holodex_enabled:
    print("Holodex enabled, fetching data...")
    try:
        json_data = requests.get(f"https://holodex.net/api/v2/videos?{holodex_args}", headers={"X-APIKEY": api_key}).json()
    except requests.RequestException as e:
        print(f"Error fetching data from Holodex: {e}")
        json_data = None

    if json_data is not None:
        delete_movie_files(outputdir)
        for video in json_data:
            print(f"Title: {video['title']}, ID: {video['id']},\n\tBy: {video['channel']['name']}")
            print("Downloading...")
            if sys.platform == "darwin":
                proc = subprocess.run(["./yt-dlp", *args_ytdlp, f"-P {outputdir}", f"https://www.youtube.com/watch?v={video['id']}"])
                if proc.returncode != 0:
                    print("Error occurred while downloading video.")
                else:
                    print(f"Download completed successfully. at {outputdir}")
            else:       
                proc = subprocess.run(["yt-dlp", *args_ytdlp, f"-P {outputdir}", f"https://www.youtube.com/watch?v={video['id']}"])
                if proc.returncode != 0:
                    print("Error occurred while downloading video.")
                else:
                    print(f"Download completed successfully. at {outputdir}")


if ytdlp_downloaders:
    print("\n\nRunning yt-dlp downloaders...")
    for downloader in ytdlp_downloaders:
        print(f"Running {downloader['url']}...")
        delete_movie_files(downloader['dir'])
        args_ytdlp_temp = args_ytdlp.copy()
        if downloader['playlist-items'] != "NOOP":
            args_ytdlp_temp.extend(["--playlist-items", downloader['playlist-items']])
        if downloader['match-filter'] != "NOOP":
            args_ytdlp_temp.extend(["--match-filters", downloader['match-filter']])

        if sys.platform == "darwin":
            dlp_list = ["./yt-dlp", *args_ytdlp_temp, f"-P {downloader['dir']}", f"{downloader['url']}"]
            print(f"Running command: {' '.join(dlp_list)}")
            proc = subprocess.run(dlp_list)
            if proc.returncode != 0:
                print("Error occurred while downloading video.")
            else:
                print(f"Download completed successfully. at {downloader['dir']}")
        else:
            proc = subprocess.run(["yt-dlp", *args_ytdlp_temp, f"-P {downloader['dir']}", f"{downloader['url']}"])
            if proc.returncode != 0:
                print("Error occurred while downloading video.")
            else:
                print(f"Download completed successfully. at {downloader['dir']}")