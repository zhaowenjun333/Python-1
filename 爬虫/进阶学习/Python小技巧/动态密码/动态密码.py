import pyotp
import time

# 预共享密钥
totp = pyotp.TOTP('XFXXGRMELERZXQ7AQNF3UNF2OX56NOQ3')

# 获得基于当前时间戳生成动态密码
val = totp.now()
print(val)

# 此时验证是通过的，所以verify的结果是True
print(totp.verify(val))

time.sleep(30)

# 30秒后动态密码将会过期，所以verify的结果是False
print(totp.verify(val))
