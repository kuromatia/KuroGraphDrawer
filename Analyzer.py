#! /usr/bin/env python
# coding: utf-8


from GraphDrawer import GraphDrawer
import pandas as pd
from matplotlib import pyplot as plt


class Analyzer():
    def __init__(self):
        pass

    def get_args(self):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs="*")
        parser.add_argument('-g', '--graph_type')
        parser.add_argument('-s', '--split')
        parser.add_argument('-o', '--output')
        args = parser.parse_args()

        self.graph_type = args.graph_type
        self.file_list = args.input
        self.output_name = args.output

    def preprocess_mt(self, data):
        x = data["Temperature (K)"]
        y = data["Long Moment (emu)"]

        # get index of approximately 20 K
        T20 = x[x>20]
        index_20K = T20.index[0]

        y /= -y[index_20K]
        return([x, y])

    def read_mt_data(self):
        for file_name in self.file_list:
            data = pd.read_csv(file_name, header=20)
            xy = self.preprocess_mt(data)
            data = pd.concat([xy[0], xy[1]], axis=1)
            data["diff"] = data["Long Moment (emu)"].diff()
            diff_max = data[data["diff"] == data["diff"].max()]
            Tc_diff = float(diff_max["Temperature (K)"])

            data_diamag = data[data["Long Moment (emu)"]<=-0.00001]
            Tc_diamag = data_diamag["Temperature (K)"].max()

            print(Tc_diff)
            print(Tc_diamag)


    def main(self):
        self.get_args()
        self.read_mt_data()


if __name__ == "__main__":
    Analyzer().main()
