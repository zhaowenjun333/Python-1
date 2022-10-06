import math
import random
import time

# # e = this.splitDate()
# e = int(time.time() * 1000)
# print(e)
#
# # Math.ceil(e).toString(16).toUpperCase()
# t = hex(math.ceil(e))[2:].upper()

data = ''
for i in range(8):
    v1 = math.ceil(16 * random.uniform(0, 1))
    v2 = hex(v1)[2:].upper()
    data += v2
result = data.rjust(8, '0')

e = int(time.time() * 1000)
t = hex(e)[2:].upper()

b_lsid = f'{result}_{t}'
print(b_lsid)

