
# encoding:utf-8
import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=Rc6CIKDayLjW9fzY6upd4ear&client_secret=cytVQ2FOuzdnaHRqqbvGSG2Vak02nGvv'
response = requests.get(host)
if response:
    print(response.json())

