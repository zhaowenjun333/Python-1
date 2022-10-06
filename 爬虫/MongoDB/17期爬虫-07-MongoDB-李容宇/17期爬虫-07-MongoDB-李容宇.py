# 9.（必做题）将数据集1的数据通过Python插入到MongoDB数据库中：
# 数据库名字为crawl_one;
# 集合名字为collection_one；
from pymongo import MongoClient
import time


class MongoDBConn:
    def __init__(self):
        self.conn = MongoClient()
        self.db = self.conn['crawl_one']['collection_one']

    # 读取数据
    def read_data(self):
        with open('./movie_world.csv', 'r', encoding='utf-8') as f:
            header = f.readline().strip('\n').strip('\ufeff').split(',')
            lst = []
            for i in f.readlines():
                item = {}
                line = i.strip('\n')
                d1 = line.split(',"')
                if len(d1) > 2:
                    d1[0] = d1[0] + ',"' + d1[1]
                    del d1[1]
                d1[1] = d1[1].replace(',', '，')
                # print(d1)
                line = ',"'.join(d1).split(',')
                if len(line) > 6:
                    line[1] = eval(line[1] + line[2])
                    del line[2]
                line[5] = line[5].replace('"', '').replace('，', ',')
                for j in range(6):
                    item[header[j]] = line[j]
                lst.append(item)
            f.close()
            return lst

    def add_content(self):
        content = self.read_data()
        self.db.insert_many(content)

    def get_all(self):
        for i in self.db.find():
            print(i)


if __name__ == '__main__':
    t1 = time.time()
    m = MongoDBConn()
    lis = m.read_data()
    print(lis)
    m.add_content()
    m.get_all()
    t2 = time.time()
    print(t2-t1)
