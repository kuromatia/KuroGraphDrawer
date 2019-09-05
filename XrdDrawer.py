#! /usr/bin/env python
# coding: utf-8

import re
import sys
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


class XrdDrawer:
    def __init__(self):
        plt.rcParams['font.size'] = 18
        plt.rcParams['font.family']= 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['xtick.major.width'] = 1.5 # 目盛
        plt.rcParams['ytick.major.width'] = 1.5 # 目盛
        plt.rcParams['axes.linewidth'] = 2 # 枠
        plt.rcParams['axes.grid']=True
        plt.rcParams['grid.linestyle']='--'
        plt.rcParams['grid.linewidth'] = 0.5

    def get_args(self):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs="*")
        parser.add_argument('-r', '--reference_file')
        parser.add_argument('-s', '--split')
        parser.add_argument('-o', '--output')
        args = parser.parse_args()
        self.split = args.split
        self.file_list = args.input
        self.output_name = args.output
        self.ref = args.reference_file


    def read_file(self, file_name):
        import codecs
        with codecs.open(file_name, "r", "utf-8", "ignore") as f:
            df = pd.read_csv(f)
        return df

    def read_ini(self, file_name="input.ini"):
        with open(file_name, "r") as f:
            self.file_list = f.read().split("\n")
        return(self.file_list)

    def read_ini2(self, file_name="input.ini"):
        with open(file_name, "r") as f:
            self.ref = f.read().split("\n")
        return(self.ref)

    def set_mt(self):
        self.x_lower_limit = 20
        self.x_upper_limit = 80
        self.y_lower_limit = -1.0
        self.y_upper_limit = 0.2
        self.ticks_per = 10
        self.slice = 3
        self.tick_range = range(self.x_lower_limit, self.x_upper_limit+1, self.ticks_per)
        self.label = [r"$\it{x}$ = 0",
                      r"$\it{x}$ = 0.02",
                      r"$\it{x}$ = 0.03",
                      r"$\it{x}$ = 0.05",
                      r"$\it{x}$ = 0.07",
                      r"$\it{x}$ = 0.10"
                      ]
        self.marker = ["o", '^', "s", "v", "<", ">", "p", "D", "h"]
        self.marker = ["o", '^', "s", "p", "h", "8", "*", "<", ">", "D"]
        self.color_list = ["black", "red", "green", "blue", "purple", "Magenta"]

    def xrd_setting(self):
        self.x_lower_limit = 30
        self.x_upper_limit = 90
        self.y_lower_limit = 0
        self.y_upper_limit = 1.2
        self.ticks_per = 5
        self.tick_range = range(self.x_lower_limit, self.x_upper_limit+1, self.ticks_per)
        self.marker = ["o", '^', "s", "v", "<", ">", "p", "D", "h"]
        self.marker = ["o", '^', "s", "p", "h", "8", "*", "<", ">", "D"]
        self.color_list = ["black", "red", "green", "blue", "purple", "Magenta"]


    def preprocess_xrd(self, data):
        data = data.iloc[13:]
        x = data.iloc[:,0].astype(float)
        y = data.iloc[:,1].astype(float)
        y /= y.max()
        return([x, y])

    def preprocess_xrd2(self, data):
        pass

    def reference(self):
        self.pat_list = []
        for ref_file in self.ref:
            data = pd.read_csv(ref_file)
            self.pat = data
            self.pat_list.append(self.pat)

    def xrd_controller(self):
        self.correct = 0 #-(56.15 - 56.12)


    def fit_peaks(self, xy, x_range=[30.1, 30.6]):

        def gausian(x, a, b, c):
            return(a * np.exp(- (x - b)**2 / c**2))

        from scipy.optimize import curve_fit
        data = pd.concat([xy[0], xy[1]], axis=1)
        data.columns = ["2theta", "int."]
        use = data[(data["2theta"] > x_range[0]) & (data["2theta"] < x_range[1])]
        popt, pcov = curve_fit(gausian, data["2theta"], data["int."], p0=[0.42, 30.37, 0.2])
        print(popt)
        return data


    def draw_xrd_graph(self):
        self.xrd_setting()
        self.xrd_controller()
        fig, ax = plt.subplots(figsize=(7,7))
        for cnt, file_name in enumerate(self.file_list):
            data = self.read_file(file_name)
            xy = self.preprocess_xrd(data)
            x = xy[0]
            x += self.correct
            y = xy[1]
            y = list(map(lambda i: i+cnt, y))
            x = x.reset_index(drop=True)
            y = pd.Series(y)
            ax.plot(x, y, color=self.color_list[cnt])
            # self.fit_peaks([x, y])
        color_list = ["blue", "red"]

        for cnt, pat in enumerate(self.pat_list):
            intensity = pat["Int."] / pat["Int."].max()
            for i, t in zip(intensity, pat["2theta [deg.]"]):
                ax.plot([t, t], [0, i], c=color_list[cnt], alpha=0.6)
        # --------------------------------------------------------
        ax.tick_params(bottom=True,
                       left=False,
                       right=False,
                       top=True)

        ax.tick_params(labelbottom=True,
                       labelleft=False,
                       labelright=False,
                       labeltop=False)

        ax.set_xlabel(r"2$\theta$ / deg. (Cu-$K_\alpha$)")
        ax.set_ylabel("intensity (normalized)")
        ax.set_xlim(self.x_lower_limit, self.x_upper_limit)
        ax.set_ylim(self.y_lower_limit, self.y_upper_limit)
        ax.set_xticks(self.tick_range)
        # --------------------------------------------------------

    def main(self):
        self.get_args()
        if (re.search(".*\.ini", self.file_list[0])):
            try:
                self.read_ini(self.file_list[0])
            except:
                print("file not found.")
                return(0)

        # self.file_list.remove("")
        # print(self.file_list)
        # print(self.ref)
        # if (re.search(".*\.ini", self.ref)):
        #     try:
        #         self.read_ini2(self.ref)
        #     except:
        #         print("file not found.")
        #         return(0)
        # self.ref.remove("")
        # print(self.ref)
        # self.reference()
        # for i in self.pat["2theta [deg.]"]:

        self.draw_xrd_graph()
        plt.show()

if __name__ == '__main__':
    XrdDrawer().main()
