# 一般的视频网站是怎么做的
# 用户上传 ——> 转码（把视频做处理， 2K， 1000， 标清）  ——> 切片处理（把单个文件进行拆分）  60
# 用户在进行拉动进度条的时候
# ==============================

# 需要一个文件记录：1. 视频播放顺序， 2. 视频存放路径
# M3U8   ===>  文本

# 想要抓取一个视频
# 1. 找到m3u8 (各种手段)
# 2. 通过m3u8下载到ts文件
# 3. 可以通过各种手段（不仅是编程手段）把ts文件合并为一个mp4文件


