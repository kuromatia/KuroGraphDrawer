import sys
import pandas as pd
from matplotlib import pyplot as plt

class GraphDrawer:
    def __init__(self):
        self.graph_type = ""
        self.file_list = []

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
        plt.tick_params(length=7, pad=7)

    def get_args(self):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs="*")
        parser.add_argument('-g', '--graph_type')
        args = parser.parse_args()

        self.graph_type = args.graph_type
        self.file_list = args.input


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
        plt.xlim(5, 35)
        plt.ylim(0, cnt+0.2)
        plt.show()

    def preprocess_mt(self, data):
        x = data["Temperature (K)"]
        y = data["Long Moment (emu)"]

        # get index of approximately 20 K
        T20 = x[x>20]
        index_20K = T20.index[0]

        y /= -y[index_20K]
        return([x, y])

    def draw_mt_graph(self):
        data = pd.read_csv(self.file_list[0], header=20)
        xy = self.preprocess_mt(data)
        cnt = 0
        color_list = ["black", "red", "blue"]
        for file_name in self.file_list:
            data = pd.read_csv(file_name, header=20)
            xy = self.preprocess_mt(data)
            plt.plot(xy[0][::3], xy[1][::3], marker="o", ms=10, color=color_list[cnt])
            cnt =+ 1
        plt.xlabel(r"$\it{T}$ / K")
        plt.ylabel(r"- $\it{M}$ / $\it{M}$ (20 K , ZFC)")
        plt.xlim(20, 100)
        plt.ylim(-1, )
        plt.tight_layout()
        plt.show()


    def preprocess_rt(self):
        pass


    def draw_rt_graph(self):
        pass


    def main(self):
        self.get_args()
        print(self.graph_type)
        if (self.graph_type == "mt"):
            self.draw_mt_graph()
        else:
            self.draw_xrd_graph()


if __name__ == "__main__":
    GraphDrawer().main()
