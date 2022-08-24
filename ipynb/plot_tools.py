# plot_tools.py
# (c) Liwei Ji 08/2022

import os
import re
import numpy as np

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


####################
# Basics Functions #
####################

# set limit for plt
def set_plot(plt, labels, lims):
    # set labels
    if(labels):
        if(type(labels)==list):
            plt.xlabel(labels[0])
            plt.ylabel(labels[1])
        else:
            plt.ylabel(labels)
    # set limits
    if(lims):
        if(type(lims[0])==list):
            # 2d list case
            plt.xlim(lims[0])
            plt.ylim(lims[1])
        else:
            # 1d list case
            plt.ylim(lims)

# load one file
def load_data(fullpath):
    print("loading", fullpath)
    fdata = np.loadtxt(fullpath)
    return fdata

# interp 1d data
def interp_data(data, cols=[1,2], kind='linear'):
    x = [d[cols[0]-1] for d in data]
    y = [d[cols[1]-1] for d in data]
    f = interp1d(x, y, kind)
    return f

# diff with exact solution
def diff_data(f_data, f_exact, lims=[-0.5, 0.5], num=100):
    diff = []
    x = np.linspace(lims[0], lims[1], num)
    for i in range(len(x)):
        diff.append([x[i], abs(f_data(x[i]) - f_exact(x[i]))])
    return diff

#################
# DataSet Class #
#################

class DataSet:
    def __init__(self, dirs, files):
        self.dataset = []
        self.interpf = []
        self.diffset = []
        dict_list = []
        for i in range(len(dirs)): # go over all dirs
            d = dirs[i]
            for f in os.listdir(d): # go over all files in d
                if re.search(files, f):
                    fdata = load_data(os.path.join(d, f))
                    self.dataset.append(fdata)
                    dict_list.append([i, os.path.basename(d)])
        self.dict = dict(dict_list)

    def interp(self, cols=[1,2], kind='linear'):
        for d in self.dataset:
            self.interpf.append(interp_data(d, cols, kind))

    def diff(self, f_exact, lims=[-0.5,0.5], num=100):
        for f in self.interpf:
            self.diffset.append(diff_data(f, f_exact, lims, num))

    # get functions
    def getDir_name(self, i):
        return self.dict[i]

    def getInterp(self):
        return self.interpf

    def getDiffset(self):
        return self.diffset

    # plot functions
    def plotData(self, cols=[1,2], marker='-', labels=False, lims=False,
                 savefig=False):
        for i in range(len(self.dataset)):
            d = self.dataset[i]
            plt.plot([x[cols[0]-1] for x in d],
                     [x[cols[1]-1] for x in d],
                    marker, label=self.dict[i])
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./data.pdf', bbox_inches='tight')

    def plotDiff(self, cols=[1,2], marker='-', labels=False, lims=False,
                 savefig=False):
        for i in range(len(self.diffset)):
            d = self.diffset[i]
            plt.plot([x[cols[0]-1] for x in d],
                     [x[cols[1]-1] for x in d],
                    marker, label=self.dict[i])
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./diff.pdf', bbox_inches='tight')

    def plotConv(self, cols=[1,2], marker='-', labels=False, lims=False,
                 savefig=False, conv_order=2):
        for i in range(len(self.diffset)):
            d = self.diffset[i]
            plt.plot([x[cols[0]-1] for x in d],
                     [x[cols[1]-1]*(i+1)**conv_order for x in d],
                     marker, label=self.dict[i])
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./conv.pdf', bbox_inches='tight')


# end of plot_tools.py
