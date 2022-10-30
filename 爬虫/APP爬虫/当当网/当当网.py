import jsonpath
import requests
from urllib import parse
from pprint import pprint


url = 'http://mapi7.dangdang.com/index.php?page_version=new2&access-token=&time_code=3ab451b3e22d7b27f9ec290468801e73' \
      '&img_size=e&client_version=10.12.4&pageSize=10&union_id=537-100998&timestamp=1659676204&province_id=111' \
      '&permanent_id=20220804202833376538012545471914173&a=all-search&global_province_id=111&page_action=search&c' \
      '=search&sort_type=default_0&keyword=%E7%88%AC%E8%99%AB&udid=0ad94aefb59258df2b9efb3e5940f162&user_client' \
      '=android&page=1'

header = {
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/NRD90M)'
}

# print(parse.unquote('%E7%88%AC%E8%99%AB'))

resp = requests.get(url, headers=header)
# print(resp.json())
# 有格式的打印
# pprint(resp.json())

pro_lst = resp.json()['data']['product']

# for product in pro_lst:
#     # 图书名称
#     # product_name = product['productName']
#     # 建议使用 get获取
#     # product_name = product.get('productName')
#     # print(product_name)
#
#     item.txt = {
#             'productName': product.get('productName'),   # 图书名字
#             'author': product.get('author'),             # 作者
#             'publisher': product.get('publisher'),       # 出版社
#             'goodCommentRate': product.get('goodCommentRate'),  # 好评率
#             'price': product.get('price')                # 当前价格
#             }
#
#     print(item.txt)


book_name = jsonpath.jsonpath(resp.json(), '$..productName')
print(book_name)

