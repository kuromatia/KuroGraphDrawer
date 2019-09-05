#! /usr/bin/env python
# coding: utf-8


from matplotlib import pyplot as plt
import numpy as np

class DrawTest:
    def __init__(self):
        pass

    def main(self):
        fig, ax = plt.subplots(figsize=(7,7))
        print(fig)
        print(ax)
        # def f(t):
        #     return np.exp(-t) * np.cos(2*np.pi*t)
        # x = np.arange(0, 10, 1)
        # y = f(x)
        # fig, ax = plt.subplots()
        #
        # ax.plot(x,f(x), marker="o")
        # plt.show()




if __name__ == '__main__':
    DrawTest().main()
