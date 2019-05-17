#! /usr/bin/env python
# coding: utf-8

import sys
import pandas as pd
from matplotlib import pyplot as plt

class GraphDrawer:
    def __init__(self):
        self.graph_type = ""
        self.split = ""
        self.file_list = []
        self.a = -1.0
        self.b = -1.0
        self.l = -1.0
        self.color_list = ["black", "red", "blue"]
        self.output_name = ""

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
        plt.figure(figsize=(7, 7))
        plt.tick_params(length=5, pad=7)

    def xrd_setting(self):
        self.lower_limit = 5
        self.upper_limit = 55
        self.ticks_per = 5
        self.tick_range = range(self.lower_limit, self.upper_limit+1, self.ticks_per)

    def mt_setting(self):
        self.lower_limit = 40
        self.upper_limit = 100
        self.ticks_per = 10
        self.slice = 3
        self.tick_range = range(self.lower_limit, self.upper_limit+1, self.ticks_per)


    def rt_setting(self):
        self.lower_limit = 0
        self.upper_limit = 300
        self.ticks_per = 10
        self.slice  = 4
        self.tick_range = range(self.lower_limit, self.upper_limit+1, self.ticks_per)


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


    def preprocess_xrd(self, data):
        data = data.iloc[13:]
        x = data.iloc[:,0].astype(float)
        y = data.iloc[:,1].astype(float)
        y /= y.max()
        return([x, y])


    def draw_xrd_graph(self):
        self.xrd_setting()
        cnt = 0
        for file_name in self.file_list:
            data = self.read_file(file_name)
            xy = self.preprocess_xrd(data)
            x = xy[0]
            y = xy[1]
            y = list(map(lambda i: i+cnt, y))
            plt.plot(x, y, color=self.color_list[cnt])
            cnt += 1

        plt.tick_params(bottom=True,
                        left=False,
                        right=False,
                        top=True)

        plt.tick_params(labelbottom=True,
                        labelleft=False,
                        labelright=False,
                        labeltop=False)

        plt.xlabel(r"2$\theta$ / deg. (Cu-$K_\alpha$)")
        plt.ylabel("intensity (normalized)")
        plt.xlim(self.lower_limit, self.upper_limit)
        plt.ylim(0, cnt+0.2)
        plt.xticks(self.tick_range)

    def preprocess_mt(self, data):
        x = data["Temperature (K)"]
        y = data["Long Moment (emu)"]

        # get index of approximately 20 K
        T20 = x[x>20]
        index_20K = T20.index[0]

        y /= -y[index_20K]
        return([x, y])


    def draw_mt_graph(self):
        self.mt_setting()
        cnt = 0
        for file_name in self.file_list:
            data = pd.read_csv(file_name, header=20)
            xy = self.preprocess_mt(data)
            plt.plot(xy[0][::self.slice], xy[1][::self.slice], marker="o", ms=10, color=self.color_list[cnt])
            cnt =+ 1
        plt.xlabel(r"$\it{T}$ / K")
        plt.ylabel(r"- $\it{M}$ / $\it{M}$ (20 K , ZFC)")
        plt.xlim(self.lower_limit, self.upper_limit)
        plt.ylim(-1, )
        plt.tight_layout()

    def preprocess_rt(self, data):
        x = data.iloc[:,1]
        y = data.iloc[:,2]
        y = y * 100 * self.l / (self.a * self.b)
        return([x, y])


    def draw_rt_graph(self):
        self.rt_setting()
        cnt = 0
        for file_name in self.file_list:
            with open(file_name, 'r') as f:
                value = f.read().split("\n")
            self.a = float(value[0])
            self.b = float(value[1])
            self.l = float(value[2])
            data = pd.read_csv(file_name, header=3)
            xy = self.preprocess_rt(data)
            plt.plot(xy[0][::self.slice], xy[1][::self.slice], marker="o", linewidth=3 ,color=self.color_list[cnt], ms=10, markeredgewidth=1, markeredgecolor="black", alpha=1.0, label="sample")
            cnt += 1
        plt.legend(loc=4, frameon=True, facecolor='white', edgecolor='black',fontsize=14)
        plt.xlabel(r"$\it{T}$ / K")
        plt.ylabel(r"$\it{\rho}$ / m$\Omega$cm")
        plt.xlim(self.lower_limit, self.upper_limit)
        plt.ylim(0, )
        plt.tight_layout()


    def split_data_rt(self):
        data = pd.read_csv(self.file_list[0], header=25)
        ch1 = data[["Temperature (K)", "Res. ch1 (ohm-cm)"]]
        ch2 = data[["Temperature (K)", "Res. ch2 (ohm-cm)"]]
        ch1 = ch1.dropna(how="any")
        ch2 = ch2.dropna(how="any")
        ch1.to_csv("ch1_" + self.file_list[0])
        ch2.to_csv("ch2_" + self.file_list[0])

    def save_and_show(self):
        if self.output_name:
            plt.savefig(self.output_name, transparent=True, dpi=300)
        plt.show()


    def main(self):
        self.get_args()
        if (self.split == "rt"):
            self.split_data_rt()
            print("splited in ch1 and ch2")
            return(0)

        print(self.graph_type)
        if (self.graph_type == "mt"):
            self.draw_mt_graph()
        elif (self.graph_type == "rt"):
            self.draw_rt_graph()
        elif (self.graph_type == "xrd"):
            self.draw_xrd_graph()

        self.save_and_show()

if __name__ == "__main__":
    GraphDrawer().main()
