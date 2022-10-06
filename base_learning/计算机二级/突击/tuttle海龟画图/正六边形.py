import turtle
turtle.setup(650,350,200,200)
""" for i in range(6):
    turtle.fd(200)
    turtle.right(60)
turtle.done() """

""" for i in range(6):
    turtle.fd(200)
    turtle.left(60)
turtle.done() """

""" for i in range(6):
    turtle.seth(i*60)
    turtle.fd(200)
turtle.done() """

for i in range(6):
    turtle.seth(i*-60)
    turtle.fd(200)
turtle.done() 