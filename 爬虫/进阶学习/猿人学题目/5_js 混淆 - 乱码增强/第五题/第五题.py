import requests
import execjs


class ZhiBoSpider:
    def __init__(self):
        self.api_url = 'https://match.yuanrenxue.cn/api/match/5'
        self.headers = {
            'content-length': '0',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Referer': 'https://match.yuanrenxue.cn/match/5',
            'Origin': 'https://match.yuanrenxue.cn',
            'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }
        self.sessionid = '0yonn8wa4w6zhlqrrigenikxg594pxk8'
        self.cookies = {
            "sessionid": self.sessionid,
            'Hm_lvt_9bcbda9cbf86757998a2339a0437208e': '1684145827, 1684192630, 1684192871, 1684317862',
            'Hm_lvt_c99546cf032aaa5a679230de9a95c7db': '1684145810,1684192605,1684192866,1684317806',
            'Hm_lpvt_9bcbda9cbf86757998a2339a0437208e': '1684403473',
            'Hm_lpvt_c99546cf032aaa5a679230de9a95c7db': '1684403478',
            'no-alert3': 'true',
            'tk': '6329903228031357428'
        }
        self.session = requests.session()
        self.session.headers = self.headers
        for k, v in self.cookies.items():
            self.session.cookies.set(k, v)
        self.chart_set = 'utf-8'

        self.js_filename = './JS/m5.js'
        self.js_f = open(self.js_filename, 'r', encoding=self.chart_set)
        self.js_compile = execjs.compile(self.js_f.read())
        self.js_f.close()

    def get_content(self, url, params=None):

        if params:
            resp = self.session.get(url, params=params)
        else:
            resp = self.session.get(url)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set

        return resp

    def quick_sort(self, arr):
        # 递归结束条件：如果序列长度小于等于1，则直接返回序列本身
        if len(arr) <= 1:
            return arr
        # 被选择的基准值，这里选取索引位的一个元素
        pivot = arr[0]
        # 初始化左、右子序列
        left = []
        right = []
        # 遍历序列中的元素，将小于基准值的放入左子序列，大于等于枢轴元素的放入右子序列
        for i in range(1, len(arr)):
            if arr[i] < pivot:
                left.append(arr[i])
            else:
                right.append(arr[i])
            # 递归排序左右子序列，将排好序的左子序列、基准值、排好序的右子序列合并成一个有序序列
        return self.quick_sort(left) + [pivot] + self.quick_sort(right)

    def run(self):
        lst = []
        for page in range(1, 6):
            values = self.js_compile.call('get_params')
            params = {
                'page': page,
                'm': values['url_m'],
                'f': values['url_f']
            }
            # m = values[1]
            # self.session.cookies.set('m', m)

            RM4hZBv0dDon443M = values['RM4hZBv0dDon443M']
            self.session.cookies.set('RM4hZBv0dDon443M', RM4hZBv0dDon443M)

            if page > 4:
                self.headers['User-Agent'] = 'yuanrenxue.project'
                self.session.headers.update(self.headers)
            resp = self.session.get(self.api_url, params=params)
            content = resp.json()
            for i in content['data']:
                lst.append(i['value'])
        print(sum(self.quick_sort(lst)[-5:]))


if __name__ == '__main__':
    zhibo = ZhiBoSpider()
    zhibo.run()
