import uuid
import time


def gen_uuid():
    uuid_sec = str(uuid.uuid4())
    time_sec = str(int(time.time() * 100 % 1e5))
    # rjust: 长度条件不满足，补0
    time_sec = time_sec.rjust(5, '0')

    return f'{uuid_sec}{time_sec}infoc'


_uuid = gen_uuid()

print(_uuid)
