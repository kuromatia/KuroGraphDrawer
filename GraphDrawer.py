#! /usr/bin/env python
# coding: utf-8
import sys
import pandas as pd
from matplotlib import pyplot as plt

class GraphDrawer:
    def __init__(self, file_list):
        self.file_list = file_list[1:]

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
        plt.rcParams['grid.linewidth'] = 0.3

        plt.figure(figsize=(7, 7))

        plt.tick_params(bottom=True,
                        left=False,
                        right=False,
                        top=True)

        plt.tick_params(labelbottom=True,
                        labelleft=False,
                        labelright=False,
                        labeltop=False)

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
        color_list = ["black", "red", "blue"]
        cnt = 0
        for file_name in self.file_list:
            data = self.read_file(file_name)
            xy = self.preprocess_xrd(data)
            x = xy[0]
            y = xy[1]
            y = list(map(lambda i: i+cnt, y))
            plt.plot(x, y, color=color_list[cnt])
            cnt += 1

        plt.xlabel(r"2$\theta$ / deg. (Cu-$K_\alpha$)")
        plt.ylabel("intensity (normalized)")
        plt.xlim(5, 35)
        plt.ylim(0, cnt+0.2)
        plt.show()

    def draw_rt_graph(self):
        pass

    def main(self):
        self.draw_xrd_graph()

if __name__ == "__main__":
    GraphDrawer(sys.argv).main()
