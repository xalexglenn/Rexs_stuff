import turtle
t = turtle.Pen()
x=200
t.speed(0)
for i in range(40):
    t.forward(x)
    t.right(90)
    x-=5
