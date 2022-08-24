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
def load_data(fullpath, cols=None):
    if(cols==None):
        print("loading", fullpath, "cols: all")
        return np.loadtxt(fullpath) # load all columns
    else:
        print("loading", fullpath, "cols:", cols)
        return np.loadtxt(fullpath, usecols=tuple([i-1 for i in cols]))

# interp 1d data
def interp1d_data(data, cols=[1,2], kind='linear'):
    x = [d[cols[0]-1] for d in data]
    y = [d[cols[1]-1] for d in data]
    return interp1d(x, y, kind)

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
    def __init__(self, dirs, files, cols=None):
        self.dataset = []
        self.interp1dset = []
        self.diffset = []
        dict_list = []
        for i in range(len(dirs)): # go over all dirs
            d = dirs[i]
            for f in os.listdir(d): # go over all files in d
                if re.search(files, f):
                    self.dataset.append(load_data(os.path.join(d, f), cols))
                    dict_list.append([i, os.path.basename(d)])
        self.dict = dict(dict_list)

    # choose two cols in self.dataset to do 1d interp
    def interp1d(self, cols=[1,2], kind='linear'):
        self.inter1dset = []
        for d in self.dataset:
            self.interp1dset.append(interp1d_data(d, cols, kind))

    def diff(self, f_exact, lims=[-0.5,0.5], num=100):
        self.diffset = []
        for f in self.interp1dset:
            self.diffset.append(diff_data(f, f_exact, lims, num))

    # get functions
    def getDir_name(self, i):
        return self.dict[i]

    def getDataset(self):
        return self.dataset

    def getInterp(self):
        return self.interp1dset

    def getDiffset(self):
        return self.diffset

    # plot functions
    def plotData(self, cols=[1,2], marker='-', labels=False, lims=False,
                 savefig=False, exact=False):
        for i in range(len(self.dataset)):
            d = self.dataset[i]
            plt.plot([x[cols[0]-1] for x in d],
                     [x[cols[1]-1] for x in d],
                    marker, label=self.dict[i])
        if(exact):
            plt.plot([x[1] for x in exact],
                     [x[2] for x in exact], marker, lable='exact')
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./data.pdf', bbox_inches='tight')

    def plotDiff(self, marker='-', labels=False, lims=False,
                 savefig=False):
        for i in range(len(self.diffset)):
            d = self.diffset[i]
            plt.plot([x[0] for x in d],
                     [x[1] for x in d],
                    marker, label=self.dict[i])
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./diff.pdf', bbox_inches='tight')

    def plotConv(self, marker='-', labels=False, lims=False,
                 savefig=False, conv_order=1):
        for i in range(len(self.diffset)):
            d = self.diffset[i]
            plt.plot([x[0] for x in d],
                     [x[1]*(i+1)**(conv_order) for x in d],
                     marker, label=self.dict[i])
        set_plot(plt, labels, lims)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig('./conv.pdf', bbox_inches='tight')


# end of plot_tools.py
