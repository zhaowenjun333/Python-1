# 1.拿到contId
# 2.拿到videoStatus返回的json。 ——> srcURL
# 3.srcURL里面的内容进行修正
# 4.下载视频

import requests

url = 'https://www.pearvideo.com/video_1754918'
conId = url.split("_")[1]

header = {
    "X-Requested-With": "XMLHttpRequest",
    # 防盗链：Referer,溯源，当前本次请求的上一级是谁
    "Referer": url,
}

videoStatus = f'https://www.pearvideo.com/videoStatus.jsp?contId={conId}&mrd=0.8278446675700286'

resp = requests.get(videoStatus, headers=header)
dic = resp.json()
srcUrl = dic["videoInfo"]["videos"]["srcUrl"]
systemTime = dic["systemTime"]

# 真实视频链接：
# https://video.pearvideo.com/mp4/short/20220315/cont-1754918-15842868-hd.mp4
# https://video.pearvideo.com/mp4/short/20220315/1649749390307-15842868-hd.mp4

# 替换视频链接
srcUrl = srcUrl.replace(systemTime, f"cont-{conId}")
# print(srcUrl)
download = requests.get(srcUrl)

# 下载视频
with open("./MP4/a.mp4", "wb") as f:
    f.write(download.content)

resp.close()
download.close()
