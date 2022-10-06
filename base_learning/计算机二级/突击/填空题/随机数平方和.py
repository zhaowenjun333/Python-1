import random
random.seed(0)
s=0
for i in range(5):
    n = random.randint(1,97)
    s = s + n**2
print(s)