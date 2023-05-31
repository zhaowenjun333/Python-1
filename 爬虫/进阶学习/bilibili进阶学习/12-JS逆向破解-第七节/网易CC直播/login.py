import random
import time

import requests
import httpx
import urllib.request
import urllib.parse
import execjs
import re
import json
import cv2
import ddddocr


class Move:
    def __init__(self):
        self.user = '17302254866@163.com'
        self.password = 'Lry1730225@'

        self.start_url = 'https://cc.163.com/category/'
        self.ini_url1 = 'https://dl.reg.163.com/dl/dlzc/yd/ini'
        self.ini_url2 = 'https://dl.reg.163.com/dl/zj/mail/ini'
        self.d_url = 'https://webzjac.reg.163.com/v3/d'
        self.b_url = 'https://webzjac.reg.163.com/v3/b'
        self.vftcp_url = 'https://dl.reg.163.com/dl/zj/mail/vftcp'
        self.gt_url = 'https://dl.reg.163.com/dl/zj/mail/gt'
        self.l_url = 'https://dl.reg.163.com/dl/zj/mail/l'

        self.get_img_url = 'https://webzjcaptcha.reg.163.com/api/v2/get'
        self.check_url = 'https://webzjcaptcha.reg.163.com/api/v2/check'
        self.login_win_url = 'https://livestatic.cc.163.com/_next/static/chunks/login-win-f597e357b47f5ba2.js'

        self.session = requests.session()
        self.client = httpx.Client(http2=True)
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        self.session.headers.update(self.headers)
        self.chart_set = 'utf-8'

        self.cb_js_filename = './JS/cb.js'
        self.cb_js_f = open(self.cb_js_filename, 'r', encoding=self.chart_set)
        self.cb_js_compile = execjs.compile(self.cb_js_f.read())
        self.cb_js_f.close()

        self.move_js_filename = './JS/move.js'
        self.move_js_f = open(self.move_js_filename, 'r', encoding=self.chart_set)
        self.move_js_compile = execjs.compile(self.move_js_f.read())
        self.move_js_f.close()

        self.acToken_js_filename = './JS/acToken.js'
        self.acToken_js_f = open(self.acToken_js_filename, 'r', encoding=self.chart_set)
        self.acToken_js_compile = execjs.compile(self.acToken_js_f.read())
        self.acToken_js_f.close()

        self.encParams_js_filename = './JS/encParams.js'
        self.encParams_js_f = open(self.encParams_js_filename, 'r', encoding=self.chart_set)
        self.encParams_js_compile = execjs.compile(self.encParams_js_f.read())
        self.encParams_js_f.close()

        self.getId_js_filename = './JS/getId.js'
        self.getId_js_f = open(self.getId_js_filename, 'r', encoding=self.chart_set)
        self.getId_js_compile = execjs.compile(self.getId_js_f.read())
        self.getId_js_f.close()

        self.getPassword_js_filename = './JS/password.js'
        self.getPassword_js_f = open(self.getPassword_js_filename, 'r', encoding=self.chart_set)
        self.getPassword_js_compile = execjs.compile(self.getPassword_js_f.read())
        self.getPassword_js_f.close()

        self.__snaker__id_js_filename = './JS/__snaker__id.js'
        self.__snaker__id_js_f = open(self.__snaker__id_js_filename, 'r', encoding=self.chart_set)
        self.__snaker__id_js_compile = execjs.compile(self.__snaker__id_js_f.read())
        self.__snaker__id_js_f.close()

        self.get_d_js_filename = './JS/get_d.js'
        self.get_d_js_f = open(self.get_d_js_filename, 'r', encoding=self.chart_set)
        self.get_d_js_compile = execjs.compile(self.get_d_js_f.read())
        self.get_d_js_f.close()

        self.bg_filename = './image/bg.jpg'
        self.front_filename = './image/front.jpg'
        self.promark, self.productkey = self.static_datas()

        self.utid = self.getId_js_compile.call('utid')
        self.rtid = self.getId_js_compile.call('rtid')
        self.zoneId = 'CN31'
        self.fp_lst = [
            r'5xGvMY0LI2pIAt6PTEdeKlA3nb+eOMKzl6C7Hjyc1\HYkI8XUvcLjINJ\hWiuWlH1h/VejZqt4vKWMkSnxEWoALV2iBs6cRlC\PzCKAblXCujwsCgVpCBVS3j0W1NjPWlwecomTTneB8CO687SiqovVtLKunohwctou2h+1f\cOv7HUP:',
            r'1A+OIvVgTGoUVvCZWRj0zrUgPcCyKyGyV2SLpIafLYEphkN+y+ocXXUa2jYUTgiiOHiXWD2+Iby\jxz2KxkXqU5ss6zJz/zQA3gqkhmSC7S\LjaqSGEpQwT8\5bw0J7jnGjnH5xokCEBlUe/BS/Lsu6dKVzP7RU7HUKboGtzlseNxBNT:',
            r'+7V//vHkdahnrrzAZrxKwpBSunBonbuxhzPIk4XOJiPbBkDj4nM+g6kcu2E0lpdUTnYaijrbfJ196CndldYfkpfOTGPaz5m5+2Ilmye4ShiqmUT4pt7G2LGWO95Kd\674KchAdHK4brUC20g9dA7yS4e91fZJY4MxNEUSBdW63uEjcik:',
            r'7YLt4XM30mVa+nJaWlGXWqER4/VURCaoLzZaQ1W7uYw4x/S1hNwD6mPoaZEhJ5oyYOer89rT78+cuOj3qnHwoOtl1vJJWKKOh/7mb3wmAcJsjhuQQDMhMMPq7PyV9jZRRNMI0KR6NYa5B1naWKft//GXG+wa7KYvo2MuSPYSwYoqu1Cy:',
            r'B/xpXbOnlP//itihfWXlLhQW\yA048taL4OiuYYjCqDw\c2OtLq6rsOxVP9Xr8rrstdYI7AvqD29PPxUz0aIdUsVAQZkKS5d6lJ812cRvIzT8CH\CZ/oHJ2iBmG1SgwkaLr9ahGVKoDVc5TkXYL/j3NQU7HmUkGZxQAYV69oBXgSYSaW:',
            r'PrLoUsuNz51pEkIwJYzr\RdxxsTVjoYccV+G\geTJNk+xBVBZJ\Mi6Q4I4sKoUEbWT/gkN\kL99TVnvT9ZM8JqQpeaU7ospWIBRBmTN9g77rO/86e7MQKOywL9WpytHq8SeICIZUGOXzquDWL9HATjEnjn4yXNQQL5spLGhquOekRQJr:',
            r'KpZSwPJky8\ugsUN8tUJlts6rPArAo8me162eN599755pmDs/UZdniAyktL9o9Urxt8JEsL4jhVmBOqz9x59+c7B\08BJ49wvLUYn66OhNGyNbx6TsTWeJqPfYlAHUxP\YHTlB1JUKTjwdhVAc7O3Cy1EAT/K/KMqhxB4tw9q1lBLdja:',
            r'K65Bf4Ixq1ZzIvgH89xNwsmPXYwQydY/U3iqJM58ICje7ij\y/PyrnL5xQiAW8dYyqhPbb619Pj3slN/dxdEcnI8tmDMxtg1\5ZJz9jugpaQ/qgxf+eiUICGd\p63V+jWrrWsf7at1rwEUsVRND+CZte3eTS9w/f452yEHhCuK15jrHD:'
            r'sJwOUZIiqUU6eKpK77\DGtnJ8PP/L4nA9SR6ewHI32a3jcs03icBxbsiGxRaxccsRsIVi0ErYBbe8jXZfV+lPhv1Gdz0WkAbqnXkQHis+xkakoY4+2oorENCxgPuegziASpaaUPSDg\AJB7OJ9ovLOyyrC5K5T\5rMoJAltxNnhIOWyC:'
        ]
        self.fp = rf"{random.choice(self.fp_lst) + str(time.time()*1000).split('.')[0]}"
        self.NTES_WEB_FP_lst = [
            '8048f2cb1b2f73230dcb7d12671d1b16',
            '16ce384d8478f26482e28557203afe1c',
            '3c53467e6df4e8d143202cd100a7fa22'
        ]
        self.NTES_WEB_FP = random.choice(self.NTES_WEB_FP_lst)

    def get_cookies(self):
        return self.session.cookies.get_dict()

    def static_datas(self):
        static_resp = self.get_response(self.login_win_url)
        content = static_resp.text
        promark = re.search(r'promark:"(.*?)",', content, re.S).group(1)
        productkey = re.search(r'productKey:"(.*?)",', content, re.S).group(1)   # 744e2a6324ec5370616241baf4507538
        return promark, productkey

    def get_response(self, url, params=None, data=None):
        if not data:
            if not params:
                resp = self.session.get(url)
            else:
                resp = self.session.get(url, params=params)
        else:
            if not params:
                resp = self.session.post(url, data=data)
            else:
                resp = self.session.post(url, params=params, data=data)

        if resp.apparent_encoding:
            resp.encoding = resp.apparent_encoding
        else:
            resp.encoding = self.chart_set
        return resp

    def start_request(self):
        print('--'*20)
        print('请求首页')
        start_resp = self.get_response(self.start_url)
        # print(start_resp.status_code)
        print(self.get_cookies())
        start_resp.close()
        print('--' * 20)

    def ini_request(self):
        print('--' * 20)
        print('开始第一次请求ini')
        self.session.cookies.set('utid', self.utid)
        self.session.cookies.set('NTES_WEB_FP', self.NTES_WEB_FP)
        self.headers['Content-Type'] = 'application/json'
        self.headers['Referer'] = 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html?cd=https%3A%2F%2Fcc.res.netease.com%2F_next%2F_static%2Fstatic%2Fstyles%2F&cf=urs_component-v2.css%3Fversion%3D202208080951&MGID=1679926767132.66&wdaId=&pkid=PFClpTB&product=cc'
        self.session.headers.update(self.headers)
        data1 = {
            "pd": "cc",
            "pkid": self.promark,
            "pkht": "cc.163.com",
            "channel": 14,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.rtid
        }
        data1 = self.encParams_js_compile.call('encParams', data1)
        data1 = json.dumps({"encParams": f"{data1}"})
        ini_resp1 = self.get_response(self.ini_url1, params=None, data=data1)
        content = ini_resp1.json()
        print(f'第一次ini请求结果：{content}')
        # print(self.get_cookies())
        ini_resp1.close()

        print('开始第二次请求ini')
        data2 = {
            "pd": "cc",
            "pkid": self.promark,
            "pkht": "cc.163.com",
            "channel": 0,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.rtid
        }
        data2 = self.encParams_js_compile.call('encParams', data2)
        data2 = json.dumps({"encParams": f"{data2}"})
        ini_resp2 = self.get_response(self.ini_url2, params=None, data=data2)
        content = ini_resp2.json()
        print(f'第二次ini请求结果：{content}')
        # print(self.get_cookies())
        ini_resp2.close()
        print('--' * 20)

    def get_img(self):
        cb = self.cb_js_compile.call('cb')
        params = {
            'referer': 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html',
            'zoneId': self.zoneId,
            'id': self.productkey,
            'fp': self.fp,
            'https': 'true',
            'type': '2',
            'version': '2.15.2',
            'dpr': '1',
            'dev': '1',
            'cb': cb,
            'ipv6': 'false',
            'runEnv': '10',
            'group': '',
            'scene': '',
            'width': '320',
            'audio': 'false',
            'token': '15821d17c43b4c328b478bce201a3e3a',
            'callback': '__JSONP_ezeyv04_2',
        }
        resp = self.get_response(self.get_img_url, params=params)
        html = resp.text
        resp.close()
        content = json.loads(re.search(r'__JSONP_ezeyv04_2\((.*)\);', html, re.S).group(1))
        token = content['data']['token']
        bg = content['data']['bg'][0]
        front = content['data']['front'][0]
        return bg, front, token, cb

    # 方法一
    def get_distance(self, bg_url, front_url):
        bg_resp = self.get_response(bg_url)
        bg_content = bg_resp.content
        bg_resp.close()

        front_resp = self.get_response(front_url)
        front_content = front_resp.content
        front_resp.close()

        det = ddddocr.DdddOcr(det=False, ocr=False)
        res = det.slide_match(front_content, bg_content)
        distance = res['target'][0]
        return distance

    def save_img(self, img_url, img_path):
        urllib.request.urlretrieve(img_url, img_path)

    # 方法二
    def identify_gap(self, bg_image, tp_image, out="./image/new_image.png"):
        """
        通过cv2计算缺口位置
        :param bg_image: 有缺口的背景图片文件
        :param tp_image: 缺口小图文件图片文件
        :param out: 绘制缺口边框之后的图片
        :return: 返回缺口位置
        """
        # 读取背景图片和缺口图片
        bg_img = cv2.imread(bg_image)  # 背景图片
        tp_img = cv2.imread(tp_image)  # 缺口图片

        # 识别图片边缘
        # 因为验证码图片里面的目标缺口通常是有比较明显的边缘 所以可以借助边缘检测算法结合调整阈值来识别缺口
        # 目前应用比较广泛的边缘检测算法是Canny John F.Canny在1986年所开发的一个多级边缘检测算法 效果挺好的
        bg_edge = cv2.Canny(bg_img, 100, 200)
        tp_edge = cv2.Canny(tp_img, 100, 200)

        # 转换图片格式
        # 得到了图片边缘的灰度图，进一步将其图片格式转为RGB格式
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

        # 缺口匹配
        # 一幅图像中找与另一幅图像最匹配(相似)部分 算法：cv2.TM_CCOEFF_NORMED
        # 在背景图片中搜索对应的缺口
        res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
        # res为每个位置的匹配结果，代表了匹配的概率，选出其中「概率最高」的点，即为缺口匹配的位置
        # 从中获取min_val，max_val，min_loc，max_loc分别为匹配的最小值、匹配的最大值、最小值的位置、最大值的位置
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

        # 绘制方框
        th, tw = tp_pic.shape[:2]
        tl = max_loc  # 左上角点的坐标
        br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
        cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
        cv2.imwrite(out, bg_img)  # 保存在本地

        # 返回缺口的X坐标
        return tl[0]

    def get_move_data(self, token, distance):
        move_data = self.move_js_compile.call('move_data', distance, token)
        return move_data

    def check_move(self, move_data, token, cb):
        referer = 'https://dl.reg.163.com/'
        self.headers['Referer'] = referer
        ac_token = self.acToken_js_compile.call('acToken')
        params = {
            'referer': 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html',
            'zoneId': self.zoneId,
            'id': self.productkey,
            'token': f'{token}',
            'acToken': ac_token,
            'data': f'{move_data}',
            'width': '320',
            'type': '2',
            'version': '2.15.2',
            'cb': cb,
            'extraData': self.user,
            'runEnv': '10',
            'callback': '__JSONP_9nitdw2_9',
        }
        resp = self.get_response(self.check_url, params)
        html = resp.text
        resp.close()
        return html

    def get_d(self):
        print('请求d')
        __snaker__id = self.__snaker__id_js_compile.call('__snaker__id')
        self.session.cookies.set('gdxidpyhxdE', self.fp)
        self.session.cookies.set('_9755xjdesxxd_', '32')
        self.session.cookies.set('__snaker__id', __snaker__id)
        cookies_dict = self.get_cookies()
        cookies = f'__snaker__id={__snaker__id}; utid={cookies_dict["utid"]}; NTES_WEB_FP={cookies_dict["NTES_WEB_FP"]}; l_yd_s_ccPFClpTB={cookies_dict["l_yd_s_ccPFClpTB"]}; l_s_ccPFClpTB={cookies_dict["l_s_ccPFClpTB"]}; gdxidpyhxdE={self.fp}; _9755xjdesxxd_=32'
        # print(cookies)
        self.get_d_js_compile.eval(rf'get_d("{cookies}")')
        d_txt = open('get_d.txt', 'r', encoding=self.chart_set)
        d = d_txt.read()
        d_txt.close()
        wmjsonp = self.get_d_js_compile.call('wmjsonp')
        data = {
            'd': d,
            'v': 'e2891084',
            'cb': wmjsonp
        }
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Referer'] = 'https://dl.reg.163.com/'
        self.session.headers.update(self.headers)
        d_resp = self.get_response(self.d_url, params=None, data=data)
        content = d_resp.text
        print(content)
        result = re.search(rf'{wmjsonp}\(\[\d*?,\d*?,"(?P<TID>.*?)",".*?",.*?,"(?P<NI>.*?)"\]\)', content, re.S)
        self.session.cookies.set('YD00000710348764%3AWM_TID', result.group('TID'))
        self.session.cookies.set('YD00000710348764%3AWM_NI', result.group('NI'))

        print('\n')
        d_resp.close()

    def get_b(self):
        __snaker__id = self.__snaker__id_js_compile.call('__snaker__id')
        print(f'__snaker__id: {__snaker__id}')
        self.session.cookies.set('__snaker__id', __snaker__id)
        self.session.cookies.set('YD00000710348764%3AWM_NIKE', '9ca17ae2e6ffcda170e2e6ee8bc76f88928aaab55286bc8eb6c84f839b8a87c141ab9381cce64982a6bb96d82af0fea7c3b92ab8b3beb4cd4aa9939ed9ce63b59fbf89e26bb5b6af92e63bb4bcfad2e5689a9cf882b533ae9ab8d2e44296a7ac8afb68fbeb8ed6c65fa1bb8c94e23c93b1a2d1fc218ae98b85e25ff6ba84b7d73ffc90a2adc863aeefababc47eb1f59f9acd54a6ecb891d87086ac9bb2b460e99cf8d2d367f2bca6adef52b789bbb3dc4da78a9db9d037e2a3')
        # self.session.post(self.b_url)

        # d: X2bpfrhACzxLi9zVmiUX/4axIWte2Pfooe2+cXx81qqhjMcH2N8A/8q24mNZ+GKiVh0k9lwfWJ0a4TUgdzZKavp66QSFkyu68yHloWn5qkRYM9T8ENMOIMM9W70lE/KcPIzh+zlmIFKhpZjCz4okoJL.EpwTvvOr9ild/kj/V4dNxizbQed8LGrppARwwYKiT./wb.G5SQ9PiOHtvu8UU77wapfuVouhblFI8PA9B2ao+KYidkphHYMNCY78rqHQspv.01EVLlhd+ibCmWMNQ/dkN9ktXakFqbVwV2X2Ety4j2vSfv88tClRW4FREzKXUhwVrSyqw4WovPoWzCYqFicOj8nMnw7kG6yaCXGKSOMsyUppqnxCkqpogDCpARtzdIFJKMfNHQDeks.yUE0ds9cv0+kFrUymcmv6TvMpSkTNxLpzPavAdiMpFs2gTks2nVX6En2u4udSvxNRo7PA0PHHe4hmNRXwXiecTXzNWtLwUAE+antqCzGO6Q+Yoy+g/EG/ttYgKRjqzZ8twnJaaQ74BzD90LggO1cZb8Q.hy8.Jo0UpQY5YuyFYj2avBpgnx8R2Qi6GYcDQos8kpjRV5Yg2c0hyxba07CzC8mnlSeQuMDuC18MMx2N+DGRrRSazEoOR4fblmjig70tHloydN7z0DgyAG7QAxiYKcCHnHR+xPpUAFdlsd6V8n1E8EXvedQImThApCPlKKSwiBhko99Hk7gNwfgtfo9mdtmuBq/h6i/uE48eHshnPSypUqdL2.xs.YMNlsZLxHFtVdnU5ZvuA796.xqD4QN+x8mpIvVdozvP5FegdtlffjdEjupgygnUCPNUORQAyb/UuHYlUv1y.G/M01D+8hq.LXrqloccjTluGZ/H+hNNSDC9r8mXjdB8C00uRotuxL5oX8NyYWnCE740ncZm2hJwVjxpYN20zqTUE2i+glz8gs2gU5/gJ.xMTdNr4xuPNyyyoTBt2QAFfz/rjTVt/CJVdtKzaTkcNRXX6bWZwKEHg5KEZbxfkM6165.u4tXaxf1tT0R+iNfMEklrPMoenN0zVXz5amDK0kILAxi+eS.N1AGL22nP7NYsChpoBf6NiFKtX8hcb0.FfDgd/uzhFdDHdNFGbQQUvgeqSpFBLCONQRGGJV7Pymr4W9uhCV.yh6OJzwD6VxsNKj7iLP2e.NN+V2qp0omcxhDujCy7VqUHbMJpv7JYnrkCXdht1Zw9Rmywz6hpYc4NBSvVNcwt1Eo.BgqAyH8QQW+U66R.wfOxRkCprNKN2axvCR6Z6jZHJoet9rtfU2wm6JB66Cj72.vinrKiKiy9PT5qP6gMdt.HvwTEj+Wa.xhJ6gXT4SjW84BwXEbOU2uk.qi.suBRHEDiwUyuANdayTTUeZ4MhfTZwl1Eyk5YjvsvytNMC+GYQQlzXEcSoVFfn1JsMr7K28nTVAa2QNXFxi5UZBdAGHOgJFtgjMx.ngoI7jcQ0CKYNfywmgNoUdCN8qdgvrdtPSEoVjKzGHIGq4fDK2VesdHXgD1bjvjfjCIG6xuW2sdQxcTt9UvoNox/PLgIY8futSTi/Jr27CgdAyDocwLodYfp4r2O2lhP81fAEWWkV4VNNh62HdmS70Pk.dLKRZgtNWvCdhrJhx8gzVbuM7ffkWwuTQxf9b4yjFkvEFTOleEixAFrHAlNyZNNEm19AvSm+NNvVMS28cVd4pcqjCl5wmWHiSQgi5MZwn2ICY+NEB.9j/.wz6NcQwSFIL92P0DUIox.dh55SQZw2iQkU9HlMAmNbsR.Pe7+HEhEpY1ZCc.jJrVtHM672eFZPEz1OjHy2iCuCtxNaqmGB0Gu5CqdGcuNbtXQQ4NfF2NIKcZfu/scHrUwzUlmBugifO1.NhUQAoo.dhrlhBzGNR5izzaBGoig.R1EkJng2EN4C00Z/s27AP0tHCpNIBkNPNS6M6OehuqHVjJ2pE6dAcrc
        # v: 602a5ad7
        # cb: __wmjsonp_241acae

        # bHrvyHCpSIZEFBABBRfFkDHDg9+QD5EM
        # hoTFhfC311qs7iNd7GcMHYOQMj625FoEzjMJFc33mGVcjO8KbCoy3UU4nhgnqzG8PkGBOS7SwV072ksOyZg+/bu9vhDaTsh78NCTya0yEmzyFSBfGbb6QD3zaxB/lvjKQXk=

    def get_vftcp(self, validate, fp, zone_id):
        self.headers['Host'] = 'dl.reg.163.com'
        self.headers['Origin'] = 'https://dl.reg.163.com'
        self.headers['Referer'] = 'https://dl.reg.163.com/webzj/v1.0.1/pub/index2_new.html?cd=https%3A%2F%2Fcc.res.netease.com%2F_next%2F_static%2Fstatic%2Fstyles%2F&cf=urs_component-v2.css%3Fversion%3D202208080951&MGID=1680245921754.9956&wdaId=&pkid=PFClpTB&product=cc'
        self.headers['Content-Type'] = 'application/json'
        self.session.headers.update(self.headers)

        cap = self.cb_js_compile.call('cap', validate, fp, zone_id)
        data = {
            "un": self.user,
            "capkey": self.productkey,
            "pd": "cc",
            "pkid": self.promark,
            "cap": cap,
            "channel": 0,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.rtid
        }
        data = self.encParams_js_compile.call('encParams', data)
        data = json.dumps({"encParams": f"{data}"})
        vftcp_resp = self.get_response(self.vftcp_url, params=None, data=data)
        content = vftcp_resp.json()
        print(f'vftcp请求结果：{content}')
        print(self.get_cookies())
        print(vftcp_resp.status_code)
        print('\n')
        vftcp_resp.close()

        # vftcp_resp = self.client.post(self.vftcp_url, headers=self.headers, cookies=self.get_cookies(), data={"encParams": f"{data}"})
        # content = vftcp_resp.json()
        # print(f'vftcp请求结果：{content}')

    def get_gt(self):
        data = {
            "un": self.user,
            "pkid": self.promark,
            "pd": "cc",
            "channel": 0,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.rtid
        }
        data = self.encParams_js_compile.call('encParams', data)
        data = json.dumps({"encParams": f"{data}"})
        gt_resp = self.get_response(self.gt_url, params=None, data=data)
        content = gt_resp.json()
        print(f'gt请求结果：{content}')
        print(self.get_cookies())
        gt_resp.close()
        return content['tk']

    def get_l(self, tk):
        pw = self.getPassword_js_compile.call('password', self.password)
        data = {
            "un": self.user,
            "pw": pw,
            "pd": "cc",
            "l": 0,
            "d": 30,
            "t": 1680242442398,
            "pkid": self.promark,
            "domains": "",
            "tk": tk,
            "pwdKeyUp": 1,
            "channel": 0,
            "topURL": "https://cc.163.com/category/",
            "rtid": self.rtid
        }
        data = self.encParams_js_compile.call('encParams', data)
        data = json.dumps({"encParams": f"{data}"})
        l_resp = self.get_response(self.l_url, params=None, data=data)
        content = l_resp.json()
        print(f'l请求结果：{content}')
        print(self.get_cookies())
        print('\n')
        l_resp.close()

    def run(self):
        self.start_request()
        self.ini_request()
        # 方法一
        # while True:
        #     bg, front, token, cb = self.get_img()
        #     distance1 = self.get_distance(bg, front) + 1
        #     print(distance1)
        #
        #     move_data1 = self.get_move_data(token, distance1)
        #     # print(move_data1)
        #     result1 = self.check_move(move_data1, token, cb)
        #     print(result1)
        #     if 'true' in result1:
        #         result = json.loads(re.search(r'__JSONP_9nitdw2_9\((.*?)\);', result1, re.S).group(1))
        #         print(distance1)
        #         print(result)
        #         print(self.get_cookies())
        #         break
        # 方法二
        while True:
            bg, front, token, cb = self.get_img()
            # 下载图片
            self.save_img(bg, self.bg_filename)
            self.save_img(front, self.front_filename)
            distance2 = self.identify_gap(self.bg_filename, self.front_filename) + 4
            # print(distance2)
            move_data2 = self.get_move_data(token, distance2)
            # print(move_data2)
            result2 = self.check_move(move_data2, token, cb)
            print(result2)
            if 'true' in result2:
                print(distance2)
                result = json.loads(re.search(r'__JSONP_9nitdw2_9\((.*?)\);', result2, re.S).group(1))
                print(result)
                # print(self.get_cookies())
                break
        validate = result['data']['validate']
        self.get_d()
        # self.get_b()
        self.get_vftcp(validate, self.fp, self.zoneId)
        # tk = self.get_gt()
        # self.get_l(tk)


if __name__ == '__main__':
    move = Move()
    move.run()

