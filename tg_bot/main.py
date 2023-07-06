# for video in yt.streams.filter(file_extension="mp4", progressive=False):
#     if video.resolution is not None:
#         video_resolution.add(video.resolution)




# import os
# import yt_dlp
#
# URLS = ['https://youtu.be/sEQf5lcnj_o']
#
#
# URL = 'https://www.youtube.com/watch?v=BaW_jenozKc'
# with yt_dlp.YoutubeDL() as ydl:
#     info = ydl.extract_info(URL, download=False)
#     res = ydl.list_formats(info)
#     print(res)


import pytube
import re

like_template = r'[0-9]{1,3},?[0-9]{0,3},?[0-9]{0,3} like'
yt = pytube.YouTube("https://www.youtube.com/watch?v=ywpOFjCmdRs")
str_likes = re.search(like_template, str(yt.initial_data)).group(0)
likes = int(str_likes.split(' ')[0].replace(',', ''))
print(likes)
print(yt.author)
print(yt.title)
print(yt.views)
print(yt)
print(yt.rating)