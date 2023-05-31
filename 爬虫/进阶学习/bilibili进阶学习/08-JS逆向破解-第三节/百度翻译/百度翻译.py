import requests
import execjs


class BaiduFanYi:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Host': 'fanyi.baidu.com',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/',
        'Cookie': 'BAIDUID=64794B380927607AC89828B65449253B:FG=1; PSTM=1665423445; BIDUPSID=6335B1BE0326E994E45619ABFD09179B; BDUSS=ENWLTNsdC11bHdBWXh5WElzNkZRT28wQWtBSW94N2xFUHFwUHY4WmR-Q24yMnhqSVFBQUFBJCQAAAAAAAAAAAEAAAAh9fr3wLa99cHjbHJ5MQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKdORWOnTkVjO; BDUSS_BFESS=ENWLTNsdC11bHdBWXh5WElzNkZRT28wQWtBSW94N2xFUHFwUHY4WmR-Q24yMnhqSVFBQUFBJCQAAAAAAAAAAAEAAAAh9fr3wLa99cHjbHJ5MQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKdORWOnTkVjO; APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; newlogin=1; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BA_HECTOR=a58k2la4aga10g2lah050pjc1hmvsgv1f; ZFY=RuI2P4L4JPjXbCX:AjQW9zw3na2ro:A64C8DTMPtMSk68:C; BAIDUID_BFESS=64794B380927607AC89828B65449253B:FG=1; H_PS_PSSID=36551_37552_37689_37493_37722_36806_37538_37652_37500_37675_37742_26350; delPer=0; PSINO=2; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1666435454,1666895115,1668352410,1668358644; ab_sr=1.0.1_YTY5YzU1M2ZjZDdjNTMyNjY0ZjM4MWIzY2MxOWVmZjM5ZDA3MmU3YTkzNzBjYzVhZTVmYzAyMjNmYjA5ODU2ODQ5NzBlYTEwODNkY2NhOGNmMWI1NmQ5OWFhNzZiNTBmYWZlMjFmMTBhNTQ1YzZkMTFjN2ZmZmNiZGE4YmZhMzk4ZTUwZTc2M2VjNjIyZjRjZDBkZTI2ODc1ZTE4NWZiOTJiNTY1MTM5ZTkxYjE5NzE3YmY4ZTQ2MmIzMTY1Zjgy; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1668364497'
    }

    def __init__(self, word):
        self.word = word

    def get_sign(self):
        with open('./JS文件/baidufanyi.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        # 编译js代码
        compile_result = execjs.compile(js_code)
        sign = compile_result.call('sign', self.word)
        return sign

    def run(self):
        url = 'https://fanyi.baidu.com/v2transapi?from=en&to=zh'
        sign = self.get_sign()
        print(sign)
        # print('en' if self.word[0] in list('abcdefghijklmnopqrstuvwxyz') else 'zh')
        data = {
            'from': 'en' if self.word[0] in list('abcdefghijklmnopqrstuvwxyz') else 'zh',
            'to': 'zh' or 'en',
            'query': f'{self.word}',
            'simple_means_flag': '3',
            'sign': f'{sign}',
            # 'sign': f'871501.634748',
            'token': 'ea6645061f61decd6564ddc8f2ef79ee',
            'domain': 'common',
        }
        resp = requests.post(url, headers=self.headers, data=data)
        print(resp.json())


if __name__ == '__main__':
    w = input('请输入要翻译的单词：')
    baidu = BaiduFanYi(w)
    baidu.run()
