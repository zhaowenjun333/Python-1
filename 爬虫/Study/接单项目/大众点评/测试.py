from fractions import Fraction

# pig = 15  )
# chicken = 20
# cow = Fraction(1, 90)
N = int(input('请输入不超过1000的正整数：'))


def nums(n):
    pig = 15
    chicken = 20
    cow = Fraction(1, 90)
    if n > chicken:
        chicken_num = int(n/chicken)
        n = n - 20 * chicken_num
        if n > pig:
            pig_num = int(n / pig)
            n = n - 15 * pig_num
        else:
            pig_num = 0
    else:
        chicken_num = 0
        if n > pig:
            pig_num = int(n / pig)
            n = n - 15 * pig_num
        else:
            pig_num = 0
    cow_num = n / cow
    return chicken_num, pig_num, cow_num


ch_num, p_num, c_num = nums(N)
print(f'鸡的数量：{ch_num}')
print(f'猪的数量：{p_num}')
print(f'牛的数量：{c_num}')

