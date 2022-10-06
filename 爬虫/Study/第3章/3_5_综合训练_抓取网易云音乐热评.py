#  1. 找到未加密的参数
#  2. 想办法把参数进行加密（必须参考网易的逻辑）， params => encText, encSecKey => encSecKey
#  3. 请求到网易的，拿到评论信息
import requests
from Crypto.Cipher import AES
from base64 import b64encode
import json
import csv


url = 'https://music.163.com/weapi/comment/resource/comments/get?csrf_token='

# 请求方式POST
data = {
    "csrf_token": "",
    "cursor": "-1",
    "offset": "0",
    "orderType": "1",
    "pageNo": "1",
    "pageSize": "20",
    "rid": "R_SO_4_1913763108",
    "threadId": "R_SO_4_1913763108",
}

# 服务于d的
e = '010001'
f = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
g = '0CoJUm6Qyw8W8jud'
i = 'osRyWILWNmS6yTU6'   # 手动固定的. -> 人家函数中是随机的


# 由于i是固定的，那么encSecText就是固定的. c()函数的结果就是固定的
def get_encSecKey():
    return "c69ebe97d8370afa7db6ea569613b4a823660c76aba85d199ef6ea88502f7f6e8491f6d4345d38c6464801b036841b2958718d940dcfba34ed0bddc2f05e656ae35985489d46e5328c519561833c435383b83ab5040c8ba1a37ffecadcc78ef3de1b5a1b97304672c1fe0190874266ba2c2a62e670cbedae7e54aad31481b71d"


# 把参数进行加密
def get_params(data):   # 默认这里接收到的data是字符串
    first = enc_params(data, g)
    second = enc_params(first, i)
    return second  # 返回的就是params


# 转化成16的倍数，为下方的加密算法服务
def to_16(data):
    pad = 16 - len(data) % 16
    data += chr(pad) * pad
    return data


# 加密过程
def enc_params(data, key):
    iv = "0102030405060708"
    data = to_16(data)
    aes = AES.new(key=key.encode("utf-8"), IV=iv, mode=AES.MODE_CBC)  # 创建加密器
    bs = aes.encrypt(data.encode("utf-8"))    # 加密, 加密的内容长度必须是16的倍数
    return str(b64encode(bs), "utf-8")  # 转化为字符串返回

# 处理加密过程
'''
    # a = 16
    function a(a) {    #随机16位字符串
        var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
        for (d = 0; a > d; d += 1)         # 循环16次
            e = Math.random() * b.length,  # 随机数
            e = Math.floor(e),             # 向下取整
            c += b.charAt(e);              # 取字符串的xxxx位置
        return c
    }
    function b(a, b) {    # a是要加密的内容，
        var c = CryptoJS.enc.Utf8.parse(b)   # b是密钥
          , d = CryptoJS.enc.Utf8.parse("0102030405060708")
          , e = CryptoJS.enc.Utf8.parse(a)
          , f = CryptoJS.AES.encrypt(e, c, {  # c 加密的密钥
            iv: d,       # AES加密算法，iv是偏移量
            mode: CryptoJS.mode.CBC   # 加密模式：CBC
        });
        return f.toString()
    }
    function c(a, b, c) {    # c不产生随机数
        var d, e;
        return setMaxDigits(131),
        d = new RSAKeyPair(b,"",c),
        e = encryptedString(d, a)
    }
    
    # d:数据，
      e:'010001'，
      f:'00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
      g:'0CoJUm6Qyw8W8jud'
    function d(d, e, f, g) { 
        var h = {}  # 空对象
          , i = a(16); # i就是16位随机值，把i设置成定值
        return h.encText = b(d, g),     # g是密钥
        h.encText = b(h.encText, i),    # 返回的就是params    i也是密钥
        # e和f是定死的定值，i是随机值,定死i值，得到的key一定是固定的
        h.encSecKey = c(i, e, f),       # 返回的就是encSecKey
        h
    }
    # 两次加密
    数据+g => b => 第一次加密+i => b = params     
'''
# 发送请求
resp = requests.post(url, data={
    "params": get_params(json.dumps(data)),
    "encSecKey": get_encSecKey()
})

# print(resp.text)
# print(type(resp.text))
# print(resp.json())
# print(type(resp.json()))
resp1 = resp.json()
# print(resp1)
f = open("./网易热评/hotComments.csv", "w", encoding="utf-8")
csvwriter = csv.writer(f)

csvwriter.writerow(["commentId", "nickname", "userId", "hotComment"])
# print(resp1[data])
for comment in resp1['data']['hotComments']:
    commentId = comment['commentId']
    nickname = comment['user']['nickname']
    userId = comment['user']['userId']
    hotComment = comment['content'].replace('\n','')
    # print(f'{commentId} {nickname} {userId} {hotComment}')
    csvwriter.writerow([commentId, nickname, userId, hotComment])

print("over!")

resp.close()

