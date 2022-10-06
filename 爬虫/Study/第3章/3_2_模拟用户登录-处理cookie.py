# 登录 — 得到cookie
# 带着 cookie 去请求到书架url ——> 书架上的内容

# 必须得把上面的两个操作连起来
# 可以使用 session 进行请求 ——> session可以认为是一连串的请求，在这个过程中 cookie 不会丢失
import requests

# 会话
session = requests.session()
data = {
    "loginName": "17302254866",
    "password": "lry1730225",
}

# 1.登录
url = "https://passport.17k.com/ck/user/login"
resp1 = session.post(url, data=data)
# print(resp1.text)
# print(resp1.cookies)

# 2.拿到书架上的数据
# 刚才的session中是有cookie的
resp2 = session.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919")
# print(resp2.text)
# print(resp2.json())

resp1.close()
resp2.close()

# cookie第二种方案
# header = {
# 	"Cookie": "GUID=7b7ccd10-7555-4bbd-8301-076ba52dfc7e; Hm_lvt_9793f42b498361373512340937deb2a0=1649734925; sajssdk_2015_cross_new_user=1; c_channel=0; c_csc=web; accessToken=avatarUrl%3Dhttps%253A%252F%252Fcdn.static.17k.com%252Fuser%252Favatar%252F08%252F88%252F21%252F95642188.jpg-88x88%253Fv%253D1649735875000%26id%3D95642188%26nickname%3DLGean%26e%3D1665291211%26s%3Dcd05090ad897ca55; Hm_lpvt_9793f42b498361373512340937deb2a0=1649739212; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2295642188%22%2C%22%24device_id%22%3A%221801bdd3c96e-00641b519b876f-1f343371-1327104-1801bdd3c97fa2%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%2C%22first_id%22%3A%227b7ccd10-7555-4bbd-8301-076ba52dfc7e%22%7D",
# }
#
# resp = requests.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919", headers=header)
# print(resp.text)
# resp.close()
