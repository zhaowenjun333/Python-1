import requests
from urllib import parse

if __name__ == '__main__':
    session = requests.Session()
    session.headers.update({
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
    })

    url = 'https://xiaoyuan.zhaopin.com/search/jn=2&kw=数据分析&pg=1'
    resp = session.get(url)
    print(session.cookies.get_dict())
    sajssdk_2015_cross_new_user = '1'
    at = 'b5a490941f174faeb363999bdb221fd0'
    rt = '9d0271bd60624264bc5c3aef67562695'
    sensorsdata2015jssdkcross = '%7B%22distinct_id%22%3A%221131967883%22%2C%22first_id%22%3A%22183d68b8fa2be1-00a727ae878cd148-26021f51-1327104-183d68b8fa3e90%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E4%BB%98%E8%B4%B9%E5%B9%BF%E5%91%8A%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Fother.php%22%2C%22%24latest_utm_source%22%3A%22baidupcpz%22%2C%22%24latest_utm_medium%22%3A%22cpt%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgzZDY4YjhmYTJiZTEtMDBhNzI3YWU4NzhjZDE0OC0yNjAyMWY1MS0xMzI3MTA0LTE4M2Q2OGI4ZmEzZTkwIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTEzMTk2Nzg4MyJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221131967883%22%7D%2C%22%24device_id%22%3A%22183d68b8fa2be1-00a727ae878cd148-26021f51-1327104-183d68b8fa3e90%22%7D'
    zp_passport_deepknow_sessionId = '62b09106s86e3745e1a9385753af1c7d46b1'
    ZL_REPORT_GLOBAL = '{%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%22f870bbcc-3aa9-4e10-8641-960095352147-cityPage%22}}'

    session.cookies.set('sajssdk_2015_cross_new_user', sajssdk_2015_cross_new_user)
    session.cookies.set('at', at)
    session.cookies.set('rt', rt)
    session.cookies.set('sensorsdata2015jssdkcross', sensorsdata2015jssdkcross)
    session.cookies.set('ZL_REPORT_GLOBAL', ZL_REPORT_GLOBAL)

    print(session.cookies.get_dict()['x-zp-client-id'])

    # page_url = f'https://xiaoyuan.zhaopin.com/api/sou?S_SOU_FULL_INDEX={parse.quote("数据分析")}&' \
    #            f'S_SOU_POSITION_SOURCE_TYPE=&pageIndex={1}&' \
    #            f'S_SOU_POSITION_TYPE=2&S_SOU_WORK_CITY={538}&' \
    #            f'S_SOU_JD_INDUSTRY_LEVEL=&S_SOU_COMPANY_TYPE=&' \
    #            f'S_SOU_REFRESH_DATE=&order=12&pageSize=30&_v=0.36212744&' \
    #            f'at=d065c80aa7c84d28a89f2a5a2bb70b37&rt=9a9999d4f70543928178d7c879968984&' \
    #            f'x-zp-page-request-id=5c537cd731424e02875891a1aa46d643-1665672564904-479503' \
    #            f'&x-zp-client-id=19c1f885-8e1e-459c-b827-8d17ffa99bb0'
    #
    # resp1 = session.get(page_url)


