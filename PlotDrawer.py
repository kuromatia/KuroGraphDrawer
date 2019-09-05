#! /usr/bin/env python
# coding: utf-8

import re
import sys
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.ticker import *
import numpy as np
from sklearn.linear_model import LinearRegression
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable, get_cmap
from sklearn.gaussian_process import GaussianProcessRegressor


class PlotDrawer:
    def __init__(self):
        self.graph_type = ""
        self.split = ""
        self.file_list = []
        self.marker = ["o", '^', "s", "v", "<", ">"]
        self.color_list = ["black", "red", "green", "blue", "purple", "Magenta"]
        self.output_name = ""
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
        # plt.figure(figsize=(7, 7))
        # plt.tick_params(length=5, pad=7)

    def get_args(self):
        from argparse import ArgumentParser
        parser = ArgumentParser()
        parser.add_argument('-i', '--input', nargs="*")
        parser.add_argument('-g', '--graph_type')
        parser.add_argument('-o', '--output')
        args = parser.parse_args()

        self.file_list = args.input
        self.output_name = args.output

    def plot_RE124_tc(self):
        """
        mt_.*\.ini => tc
        """
        self.get_args()
        data = pd.read_csv(self.file_list[0])
        data = data.dropna(how="any")
        print(data)

        fig, ax = plt.subplots(figsize=(7,3))


        x = data['ionic_radius'].values.reshape(-1, 1)
        y = data["tc"].values.reshape(-1, 1)
        # lr = LinearRegression()
        lr = GaussianProcessRegressor()
        lr.fit(x, y)
        # print(lr.coef_)
        # print(lr.intercept_)
        print(lr.score(x, y))

        lrx = np.linspace(0, 1.3, 1000).reshape(-1, 1)
        ax.plot(lrx, lr.predict(lrx), color="m", zorder=-1, alpha=0.3, lw=5)

        # ax.errorbar(data['ionic_radius'], data["a"], yerr=data["da"], fmt='o', color="red", markersize=10, capsize=5, markeredgecolor="black")
        # ax.errorbar(data['ionic_radius'], data["b"], yerr=data["db"], fmt='^', color="blue", markersize=10, capsize=5, markeredgecolor="black")
        # ax.errorbar(data['ionic_radius'], data["c"], yerr=data["dc"], fmt='s', color='m',ecolor="m",markersize=10, capsize=5, markeredgecolor="black")
        # ax.errorbar(data['ionic_radius'], data["o"], yerr=data["do"], fmt='o', color="m",markersize=10, capsize=5, markeredgecolor="black")
        ax.scatter(data['ionic_radius'], data["tc"], marker='o', color="m",s=100)

        ax.tick_params(labelbottom=False)
        # ax.set_xlim(1.0, 1.12)
        # ax.set_ylim(3.84, 3.90)
        # ax.set_yticks([3.84, 3.87, 3.90])
        # ax.set_xlabel(r"$RE^{3+}$ ionic radius / $\rm\AA$")
        # ax.set_ylabel(r"lattice parameter / $\rm\AA$")
        ax.set_ylim(60, 90)
        ax.set_ylabel(r"$\it{T}_{\mathsf{c}}$ / K")
        # ax.set_ylabel("orthorhombicity / -")

        # ax.set_ylabel(r"$\it{T}_{\mathsf{c}}$ / K")
        # ax.errorbar(data['ionic_radius'], data["c"], yerr=data["dc"], fmt='s', color='m',ecolor="m",markersize=10, capsize=5, markeredgecolor="black")
        ax.set_xlim(1.0, 1.12)
        # ax.set_ylim(27.2, 27.4)
        # ax.set_yticks(range(70, 96, 5))
        # ax.set_xticks([0, 0.05, 0.10])
        ax.tick_params(length=5, pad=8)
        ax.tick_params(right=True, top=True)

        fig.tight_layout()
        plt.savefig("tc_RE124.png", transparent=True, dpi=500)
        plt.show()

        # plt.show()
        # self.save_and_show()


    def plot_RECa124_tc(self):
        self.get_args()
        data = pd.read_csv(self.file_list[0])
        data = data.dropna(how="any")
        print(data)

        fig, ax = plt.subplots(figsize=(7,5))

        norm = Normalize(vmin=data['ionic_radius'].min(), vmax=1.08)
        cmap = get_cmap('seismic')
        mappable = ScalarMappable(cmap=cmap, norm=norm)
        mappable._A = []

        re = ['Y', "Dy", "Gd", "Eu", "Sm"]
        re_ir = [1.019, 1.027, 1.053 ,1.066, 1.079]
        re_ir = [0, 0.2, 0.6, 0.7, 0.9]

        for r,rir in zip(re, re_ir):
            print(rir)
            data2 = data[data['RE'] == r]
            print(data2)
            x = data2['Ca_x'].values.reshape(-1, 1)
            y = data2["Tc_onset"].values.reshape(-1, 1)
            # lr = LinearRegression()
            lr = GaussianProcessRegressor()
            lr.fit(x, y)
            # print(lr.coef_)
            # print(lr.intercept_)
            print(lr.score(x, y))
            lrx = np.linspace(0, 0.15, 1000).reshape(-1, 1)
            ax.plot(lrx, lr.predict(lrx), color=cmap(rir), zorder=-1, alpha=0.5, lw=5)
        # =======================================================

        ax.scatter(data['Ca_x'], data["Tc_onset"], marker='o', s=200, c=data['ionic_radius'], cmap=cmap)
        fig.colorbar(mappable).set_label(r"$RE^{3+}$ ionic radius / $\rm\AA$")
        ax.set_xlim(0, 0.1)
        ax.set_ylim(70, 95)
        ax.set_yticks(range(70, 96, 5))
        ax.set_xticks([0, 0.05, 0.10])
        ax.tick_params(length=5, pad=8)
        ax.tick_params(right=True, top=True)
        ax.set_xlabel(r"$\it{x}$")
        ax.set_ylabel(r"$\it{T}_{\mathsf{c}}$ / K")
        # plt.gca().spines['left'].set_visible(False)
        # plt.gca().spines['right'].set_visible(False)
        # plt.tick_range()
        fig.tight_layout()
        plt.show()
        # self.save_and_show()
        # =======================================================

    def plot_tc2(self):
        self.get_args()
        data = pd.read_csv(self.file_list[0])
        data = data.dropna(how="any")
        print(data)

        x = data['x'].values.reshape(-1, 1)
        y = data["Tc_rt0"].values.reshape(-1, 1)
        lr = LinearRegression()
        lr.fit(x, y)
        print(lr.coef_)
        print(lr.intercept_)
        print(lr.score(x, y))

        lrx = np.linspace(0, 0.12, 1000).reshape(-1, 1)

        # =======================================================
        fig, ax = plt.subplots(figsize=(7,5))
        ax.plot(lrx, lr.predict(lrx), color="m", zorder=-1, alpha=0.3, lw=5)
        ax.scatter(data['x'], data["Tc_rt0"], marker='s', s=200, color="m")

        ax.set_xlim(0, 0.12)
        ax.set_ylim(45, 75)
        ax.set_ylim(40, 80)

        ax.tick_params(length=5, pad=8)
        ax.tick_params(right=True, top=True)
        ax.set_xlabel(r"$\it{x}$")
        ax.set_ylabel(r"$\it{T}_{\mathsf{c}} ^{0}$ / K")
        # plt.gca().spines['left'].set_visible(False)
        # plt.gca().spines['right'].set_visible(False)
        # plt.tick_range()
        fig.tight_layout()
        plt.savefig("rt0_Gd124kx.png", transparent=True, dpi=600)
        plt.show()
        # self.save_and_show()
        # =======================================================


    def plot_lp(self):
        self.get_args()
        data = pd.read_csv(self.file_list[0])
        data = data.dropna(how="any")
        print(data)
        fig, ax = plt.subplots(figsize=(7,4))
        ax.errorbar(data['x'], data["a"], yerr=data["da"], color="red",fmt='o', markersize=10, capsize=5, markeredgecolor="black")
        ax.errorbar(data['x'], data["b"], yerr=data["db"], fmt='^',color="blue", markersize=10, capsize=5, markeredgecolor="black")
        # ax.errorbar(data['x'], data["c"], yerr=data["dc"], fmt='s', color="m",markersize=10, capsize=5, markeredgecolor="black")
        # ax.errorbar(data['x'], data["o"], yerr=data["do"], fmt='o',color="m", markersize=10, capsize=5, markeredgecolor="black")
        # ax.set_ylim(27.25, 27.28)
        # ax.set_ylim(2.2, 3.0)
        ax.set_ylim(3.84, 3.90)
        # ax.set_yticks([])
        ax.set_xlim(0, 0.12)
        ax.tick_params(length=5, pad=8)
        ax.set_xlabel(r"$\it{x}$")
        ax.set_ylabel(r"$\it{a}, \it{b}$ / $\rm \AA$")
        # ax.set_ylabel(r"orthorhombicity / $\rm \AA$")
        # ax.set_ylabel(r"$\it{c}$ / $\rm \AA$")

        plt.tight_layout()
        # plt.savefig("ab_Gd124kx.png", transparent=True, dpi=300)
        plt.show()
        # self.save_and_show()


    def save_and_show(self):
        # plt.savefig("Tc_Gd124kx.png", transparent=True, dpi=600)
        plt.show()

if __name__ == '__main__':
    # PlotDrawer().plot_RE124_tc()
    # PlotDrawer().plot_RECa124_tc()
    # PlotDrawer().plot_lp()
    PlotDrawer().plot_tc2()
