import  turtle
n = 4
for i in range(n):
    turtle.goto(80*i,0)
    turtle.pendown()
    for j in range(4):
        turtle.fd(40)
        turtle.right(90)
    turtle.penup()
turtle.hideturtle()
turtle.done()