import requests


class ApplySpider:
    def __init__(self):
        self.url = 'https://match.yuanrenxue.cn/match/3'
        self.loginInfo_url = 'https://match.yuanrenxue.cn/api/loginInfo'
        self.api_url = 'https://match.yuanrenxue.cn/api/match/3'
        self.jssm_url = 'https://match.yuanrenxue.cn/jssm'
        self.headers = {
            'content-length': '0',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile':	'?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'accept': '*/*',
            'origin': 'https://match.yuanrenxue.cn',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': self.url,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'X-Requested-With': 'XMLHttpRequest'
        }
        self.cookies = {
            "sessionid": "0yonn8wa4w6zhlqrrigenikxg594pxk8",
            "Hm_lvt_c99546cf032aaa5a679230de9a95c7db": "1684145810,1684192605,1684192866,1684317806",
            "qpfccr": "true",
            "no-alert3": "true",
            "tk": "7117510294618647776",
            "Hm_lvt_9bcbda9cbf86757998a2339a0437208e": "1684145827,1684192630,1684192871,1684317862",
            "Hm_lpvt_9bcbda9cbf86757998a2339a0437208e": "1684411583",
            "Hm_lpvt_c99546cf032aaa5a679230de9a95c7db": "1684411586"
        }
        self.session = requests.session()
        self.session.headers = self.headers
        # self.session.headers.update(self.headers)
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)
        self.chart_set = 'utf-8'

    def run(self):
        d = {}
        for page in range(1, 6):
            if page > 4:
                self.headers['User-Agent'] = 'yuanrenxue.project'
                self.session.headers.update(self.headers)
            jssm_resp = self.session.post(self.jssm_url)
            api_resp = self.session.get(self.api_url)
            datas = api_resp.json()['data']
            for data in datas:
                d[data['value']] = d.get(data['value'], 0) + 1
        print(max(d.items(), key=lambda x: x[1]))


if __name__ == '__main__':
    apply = ApplySpider()
    apply.run()
