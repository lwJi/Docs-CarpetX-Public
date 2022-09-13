# plot_tools.py
# (c) Liwei Ji 08/2022

import os, sys
sys.path += [ os.path.join(os.path.dirname(__file__),
                           '../../../Misc-Packages/python/') ]
import dataset as ds
import re
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import simpson


####################
# Basics Functions #
####################

# interp 1d data
def interp1d_data(data, cols=[1,2], kind='linear'):
    x = [d[cols[0]-1] for d in data]
    y = [d[cols[1]-1] for d in data]
    return interp1d(x, y, kind)

# diff with exact solution
def diff_data(data, f_ref, norm=1):
    diff = []
    #x = np.linspace(lims[0], lims[1], num)
    for i in range(2,len(data)-2):
        diff.append([data[i,0], pow(abs(data[i,1]-f_ref(data[i,0])), norm)])
    return diff

def plt_exact(data, cols=[1,2], kind='linear', num=200, lims=[-0.5,0.5]):
    x_new = np.linspace(lims[0], lims[1], num)
    if (type(kind) == list):
        for i in range(len(kind)):
            f_exact = interp1d_data(data, cols, kind[i])
            plt.plot(x_new, f_exact(x_new), '-')
    else:
        f_exact = interp1d_data(data, cols, kind)
        plt.plot(x_new, f_exact(x_new), '-')


#################
# DataSet Class #
#################

class DataSet(ds.DataSet):
    def __init__(self, dirs, files, cols=None):
        ds.DataSet.__init__(self, dirs, files, cols)
        self.interp1dset = []
        self.diffset = []
        self.integset = []
        self.convorderset = []

    # choose two cols in self.dataset to do 1d interp
    def interp1d(self, cols=[1,2], kind='linear'):
        self.interp1dset.clear()
        for d in self.dataset:
            self.interp1dset.append(interp1d_data(d, cols, kind))

    def diff(self, f_ref, norm=1):
        self.diffset.clear()
        for d in self.dataset:
            self.diffset.append(diff_data(d, f_ref, norm))

    def integ(self):
        self.integset.clear()
        for d in self.diffset:
            self.integset.append(simpson([x[1] for x in d], [x[0] for x in d]))

    def convorder(self):
        self.convorderset.clear()
        for i in range(len(self.integset)-1):
            low = self.integset[i]
            high = self.integset[i+1]
            self.convorderset.append(math.log(low/high, 2))

    # wrapper
    def calcAll(self, f_ref, norm=1):
        self.diff(f_ref, norm)
        self.integ()
        self.convorder()

    def getInterpSet(self):
        return self.interp1dset

    def getDiffSet(self):
        return self.diffset

    def getIntegSet(self):
        return self.integset

    def getConvorderSet(self):
        return self.convorderset

    # plot functions
    def pltData(self, cols=[1,2], marker='-', labels=False, lims=False,
                 fx=lambda x,i:x, fy=lambda x,i:x,
                 savefig=False, fig_name='data.pdf',
                 xlim=[-0.5,0.5], num=100, f_ref=None):
        ds.pltSet(self.dataset, self.dictset, cols, marker, labels, lims,
                  fx, fy)

        if(f_ref is not None):
            x_new = np.linspace(xlim[0], xlim[1], num)
            plt.plot(x_new, f_ref(x_new), marker, label='exact')

        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

    def pltDiff(self, marker='-', labels=False, lims=False,
                 fx=lambda x,i:x, fy=lambda x,i:x,
                 savefig=False, fig_name='diff.pdf'):
        ds.pltSet(self.diffset, self.dictset, [1,2], marker, labels, lims,
                  fx, fy)

        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

# end of plot_tools.py
