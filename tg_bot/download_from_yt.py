import os
import re
import pytube
import yt_dlp

DOWNLOAD_DIR = os.getcwd()


def get_videos_resolution(url_video: str):
    video_resolution = set()
    like_template = r'[0-9]{1,3},?[0-9]{0,3},?[0-9]{0,3} like'
    example_resolution = ["144p", "240p", "360p", "480p", "720p", "720p60", "1080p60", "1080p"]
    yt = pytube.YouTube(url_video)
    video_title = yt.title
    video_author = yt.author
    str_likes = re.search(like_template, str(yt.initial_data)).group(0)
    video_likes = int(str_likes.split(' ')[0].replace(',', ''))
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url_video, download=False)
        for i in info["formats"]:
            result = i.get("format_note")
            if result in example_resolution:
                video_resolution.add(result)
    list_sorted_resolution = sorted(list(video_resolution))
    return video_title, list_sorted_resolution, video_author, yt.views, video_likes


def download_user_file(url_file: str, file_resolution: str):
    yt = pytube.YouTube(url_file)
    file_title = yt.title
    if file_resolution == "audio":
        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            "outtmpl": f"{DOWNLOAD_DIR}/tg_bot/user_files/{file_title}.%(ext)s",
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                },
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_file])
        file_extension = "mp3"
    else:
        number_file_resolution = file_resolution.split("p")[0]
        ydl_opts = {
            "format": f"(bv*[ext=mp4]/bv*)[height={number_file_resolution}]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b",
            "outtmpl": f"{DOWNLOAD_DIR}/tg_bot/user_files/{file_title}.%(ext)s",
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url_file])
        file_extension = "mp4"
    return file_title, file_extension
