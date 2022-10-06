""" import random
brandlist = ['华为','苹果','诺基亚','OPPO','小米']
random.seed(0)
name = random.choice(brandlist)
print(name) """

import random
brandlist = ['华为','苹果','诺基亚','OPPO','小米']
random.seed(0)
name = brandlist[random.randint(0,4)]
print(name)