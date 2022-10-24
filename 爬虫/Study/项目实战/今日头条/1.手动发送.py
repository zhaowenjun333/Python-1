import requests

url = 'https://www.toutiao.com/api/pc/list/feed?offset=0&channel_id=94349549395&max_behot_time=0&category=pc_profile_channel&disable_raw_data=true&aid=24&app_name=toutiao_web&_signature=_02B4Z6wo00d01KSjiVAAAIDCRhb5x6pCD5ykh43AAEpthpFJghWHu3E3aJ7xuQRq24sHjhv5yzi3mu-NzOzQli3U5dTpxQ0I9F-kaTSVcfr4a9XC-8LcTJZrQopdhlN5JUfABSwCJ8jtkSfi12'

resp = requests.get(url)

print(resp.json())

# 期初发送请求
# req.get(
#   url="...",
#   params = {
#       a = 1,
#       b = 2,
#       c = 21,
#       age = 19
#   }
# )

# 拦截器
# interceptors.params = {
#   a = 1,
#   b = 2,
#   c = 21,
# }


# 使用req调用拦截器发送请求
# req.interceptors = interceptors
# 发送请求时自动执行拦截器里的参数
# req.get(
#   url = "...",
#   params = {
#       age = 19
#   }
# )

