from cProfile import label
from ipaddress import collapse_addresses
import random
import matplotlib.pyplot as plt
import numpy as np

times = 5
color = 'red'
x, y = 550, 650
xt, yt = 60, 100
theta = 35 * 180 / np.pi
L = 250
Rmin = int(0.5 * L / np.sin(theta))
O = (100 + Rmin, 650 - Rmin)
link_d = 50

# 画车位
X = [0, 0, 200, 200, 400]
Y = [400, 0, 0, 400, 400]
plt.plot(X, Y, 'k-')

# 画b边界
X = [0, 1000]
Y = [1000, 1000]
plt.plot(X, Y, 'y-', linewidth=5.0)

# 画车
X = [500, 750, 750, 500, 500]
Y = [600, 600, 700, 700, 600]
plt.plot(X, Y, 'k-')

# 重心
plt.plot(x, y, 'k.', markersize=15)


def init():
    global x, y, color
    x, y = 550, 650
    color = plt.get_cmap('Paired')(random.randint(0, 11))


def step1():
    global x, y
    while True:
        x = x - 1
        y = y + random.random() * 0.5 - 0.25
        plt.plot(x, y, 'k.', markersize=1, color=color)
        if int(x) == (O[0]):
            break


def step2():
    global x, y
    while True:
        x = x - 1
        y = O[1] + np.sqrt(np.abs(Rmin ** 2 - (x - O[0]) ** 2))
        x = x + random.random() * 0.5 - 0.25
        y = y + random.random() * 0.5 - 0.25
        plt.plot(x, y, 'k.', markersize=1, color=color)
        if int(x) == 100:
            break


def step3():
    global x, y
    while True:
        y = y - 1
        x = x + random.random() * 0.5 - 0.25
        plt.plot(x, y, 'k.', markersize=1, color=color)
        if int(y) == 25:
            break
    return


for i in range(times):
    print("第" + str(i + 1) + "次倒车")
    init()
    step1()
    step2()
    step3()
plt.show()
