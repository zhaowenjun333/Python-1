import turtle
#设置铅笔粗细
turtle.pensize(2)
d = -45
for i in range(4):
    turtle.seth(d)
    d  += 90
    turtle.fd(200)