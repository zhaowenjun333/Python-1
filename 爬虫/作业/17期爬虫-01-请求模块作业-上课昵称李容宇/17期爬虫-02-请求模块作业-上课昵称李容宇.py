import requests
key = input("请输入你要搜索的内容：")
start = int(input("查询的起始页："))
end = int(input("查询的终止页："))
# url = f'https://www.sogou.com/web?query={key}&page={start}&ie=utf8'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",

}
for i in range(start, end+1):
    url = f'https://www.sogou.com/web?query={key}&page={i}&ie=utf8'
    resp = requests.get(url, headers=headers)
    resp.encoding = "utf-8"
    # print(resp.text)
    with open(f'./data/{key}{i}页.html', 'w', encoding='utf-8') as f:
        # 方法一
        f.write(resp.text)
        # 方法二
        # f.write(resp.content.decode('utf-8'))
    f.close()
    resp.close()
    break
    print(f"{key}{i}页.html is over!")
