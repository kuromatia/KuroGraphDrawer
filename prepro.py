#! /usr/bin/env python
# coding: utf-8

import pandas as pd
from matplotlib import pyplot as plt

class prepro:
    def __init__(self):
        pass

    def main(self, file_name):
        data = pd.read_csv(file_name, header=20)

        data2 = data[["Temperature (K)" ,"Long Moment (emu)"]]
        print(data2[data2["Temperature (K)"]>30])

        # plt.plot(data2.iloc[:,0], data2.iloc[:,1])
        # plt.show()

if __name__ == '__main__':
    file_name = "/Users/kuro/exData/KuroGraphDrawer/Gd124kx/squid/20190605Gd124kx002sh30sq2.rso.dat"
    prepro().main(file_name)
