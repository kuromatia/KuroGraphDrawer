#! /usr/bin/env python
# coding: utf-8

import re
import sys
import pandas as pd
from matplotlib import pyplot as plt


class MtDrawer:
    def __init__(self):
        plt.rcParams['font.size'] = 18
        plt.rcParams['font.family']= 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'
        plt.rcParams['xtick.major.width'] = 1.5 # 目盛
        plt.rcParams['ytick.major.width'] = 1.5 # 目盛
        plt.rcParams['axes.linewidth'] = 2 # 枠
        # plt.rcParams['axes.grid']=True
        plt.rcParams['grid.linestyle']='--'
        plt.rcParams['grid.linewidth'] = 0.5

    def get_args(self):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs="*")
        parser.add_argument('-g', '--graph_type')
        parser.add_argument('-s', '--split')
        parser.add_argument('-o', '--output')
        args = parser.parse_args()
        self.split = args.split
        self.graph_type = args.graph_type
        self.file_list = args.input
        self.output_name = args.output


    def read_file(self, file_name):
        import codecs
        with codecs.open(file_name, "r", "utf-8", "ignore") as f:
            df = pd.read_csv(f)
        return df

    def read_ini(self, file_name="input.ini"):
        with open(file_name, "r") as f:
            self.file_list = f.read().split("\n")
        return(self.file_list)

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


    def preprocess_mt(self, data):
        x = data["Temperature (K)"]
        y = data["Long Moment (emu)"]

        # get index of approximately 20 K
        T20 = x[x>20]
        index_20K = T20.index[0]

        y /= -y[index_20K]
        return([x, y])

    def draw_mt_graph(self):
        self.set_mt()
        cnt = 0
        fig, ax = plt.subplots(figsize=(7,7))
        for file_name in self.file_list:
            data = pd.read_csv(file_name, header=20)
            xy = self.preprocess_mt(data)
            ax.plot(xy[0][::self.slice],
                     xy[1][::self.slice],
                     marker=self.marker[cnt],
                     ms=12,
                     color=self.color_list[cnt],
                     markeredgewidth=1.8,
                     markeredgecolor="black",
                     label=self.label[cnt],
                     )
            cnt += 1
        ax.tick_params(bottom=True,
                       left=True,
                       right=True,
                       top=True)
        ax.tick_params(length=5, pad=7)
        ax.set_xlim(20, 80)
        ax.set_ylim(-1, 0.2)
        ax.set_xticks(self.tick_range)
        ax.legend(frameon=False, loc='upper left')
        plt.tight_layout()
        plt.show()


    def main(self):
        self.get_args()
        if (re.search(".*\.ini", self.file_list[0])):
            try:
                self.read_ini(self.file_list[0])
            except:
                print("file not found.")
                return(0)

        self.file_list.remove("")
        print(self.file_list)

        self.draw_mt_graph()

if __name__ == '__main__':
    MtDrawer().main()
