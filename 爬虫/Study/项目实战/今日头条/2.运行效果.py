import requests
import execjs


with open('_signature.js' ,'r', encoding='utf-8') as f:
    _signature_code = f.read()
    f.close()
_signature_js = execjs.compile(_signature_code)
url = 'https://www.toutiao.com/api/pc/list/feed?channel_id=3189398999&min_behot_time=0&refresh_count=1&category=pc_profile_channel&client_extra_params=%7B%22short_video_item%22:%22filter%22%7D&aid=24&app_name=toutiao_web'
_signature = _signature_js.call('get_sign', url)
url = f'{url}&_signature={_signature}'
headers = {
'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
resp = requests.get(url, headers=headers)

print(resp.json())

