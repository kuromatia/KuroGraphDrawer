#! /usr/bin/env python
# coding: utf-8

import re
from GraphDrawer import GraphDrawer
import pandas as pd
from matplotlib import pyplot as plt


class GraphAnalyzer(GraphDrawer):
    def __init__(self):
        pass

    def read_mt_data(self):
        print('\n')
        print("========result========")
        print('\n')
        for file_name in self.file_list:
            data = pd.read_csv(file_name, header=20)
            xy = self.preprocess_mt(data)
            data = pd.concat([xy[0], xy[1]], axis=1)
            data["diff"] = data["Long Moment (emu)"].diff()
            diff_max = data[data["diff"] == data["diff"].max()]
            Tc_diff = float(diff_max["Temperature (K)"])

            data_diamag = data[data["Long Moment (emu)"]<=-0.00001]
            Tc_diamag = data_diamag["Temperature (K)"].max()

            self.data = data
            print(file_name)
            print("Tc_diamag", Tc_diamag)
            print("Tc_diff", Tc_diff)
            print('\n')
        print("========end========")
            # self.analyzer()

    def analyzer(self):
        memo = [['x', "Tc_diamag", "Tc_diff"]]
        var_x = ["0", "0.02", "0.03", "0.05", "0.07", "0.10"]
        var_x = ["x"]*20
        from sklearn.gaussian_process import GaussianProcessRegressor
        import numpy as np
        print('\n')
        print("========result========")
        print('\n')
        cnt = 0
        for file_name in self.file_list:
            self.data = pd.read_csv(file_name, header=20)
            x = self.data["Temperature (K)"].values.reshape(-1, 1)
            y = self.data["Long Moment (emu)"].values.reshape(-1, 1)
            self.gp = GaussianProcessRegressor()
            self.gp.fit(x, y)
            print(self.gp.score(x, y))
            x2 = np.linspace(20, 100, 10000).reshape(-1, 1)
            pred_mean, pred_std = self.gp.predict(x2, return_std=True)
            kukan = pred_mean + pred_std
            data1 = pd.DataFrame(x2)
            data2 = pd.DataFrame(self.gp.predict(x2))
            data1 = data1.rename(columns ={0:"Temperature (K)"})
            data2 = data2.rename(columns ={0:"Long Moment (emu)"})

            data = pd.concat([data1, data2], axis=1)
            # print(data)
            # data = data.rename(columns ={0:"a", 0:"b"})
            # print(data)
            data["diff"] = data["Long Moment (emu)"].diff()
            diff_max = data[data["diff"] == data["diff"].max()]
            Tc_diff = float(diff_max["Temperature (K)"])

            data_diamag = data[data["Long Moment (emu)"]<=-0.00001]
            Tc_diamag = data_diamag["Temperature (K)"].max()
            print("Tc_diamag", Tc_diamag)
            print("Tc_diff", Tc_diff)
            print("\n")
            memo.append([var_x[cnt], Tc_diamag, Tc_diff])
            cnt += 1
        print("========end========")
        print(memo)

        # import csv
        # with open("a.csv", "w") as f:
        #     writer = csv.writer(f, lineterminator="\n")
        #     writer.writerows(memo)
            # plt.scatter(x, y, c="red")
            # plt.plot(x2, self.gp.predict(x2))
            # plt.fill_between(x2[:, 0], (pred_mean + pred_std)[:, 0], (pred_mean - pred_std)[:, 0], color="C0", alpha=.3,label= "1 sigma confidence")
            # plt.show()



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
        print(self.graph_type)

        self.read_mt_data()

    def main2(self):
        self.get_args()
        if (re.search(".*\.ini", self.file_list[0])):
            try:
                self.read_ini(self.file_list[0])
            except:
                print("file not found.")
                return(0)

        self.file_list.remove("")
        print(self.file_list)
        print(self.graph_type)
        self.read_mt_data()

        # self.analyzer()

if __name__ == "__main__":
    GraphAnalyzer().main2()
