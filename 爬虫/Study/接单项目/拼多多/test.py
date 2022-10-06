import requests


url = 'https://cmtw.pinduoduo.com/api/ajax'

print(requests.post(url).cookies.get_dict())

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'cookie': 'api_uid=CkoXwWM2j1HCqwBoWsuXAg==; _nano_fp=XpEjn0dxX09al0TbnT_FKEnPfISpfiiOdVg9VOkh; webp=1; dilx=kG12w5lMteFO~ha3txPVw; jrpl=RsdMDZOjYEMv4yvEoxDfUiWD9VXyG0oX; njrpl=RsdMDZOjYEMv4yvEoxDfUiWD9VXyG0oX; PDDAccessToken=M5NKENMJFEITZ4BSSHDKWOPO7IWCUNUX7GVLKIJCMAAWQ3JRA4OQ1122d90; pdd_user_id=4544664441389; pdd_user_uin=ZIQELYOS4MGDVI5W4T5K6K5TNY_GEXDA; rec_list_personal=rec_list_personal_lsncvy; pdd_vds=gaFLkOktZLcGviYiqQYbqEMirnFtkIYQWECIvbWaZbZmHtqtFyzIqECIvLCI'
}

# resp = requests.get(url, headers=header)
# print(resp.json())
