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
    return interp1d([d[cols[0]-1] for d in data],
                    [d[cols[1]-1] for d in data], kind)

# diff with exact solution
def diff_data(data, f_exact):
    diff = []
    for i in range(2,len(data)-2):
        diff.append([data[i,0], abs(data[i,1]-f_exact(data[i,0]))])
    return diff

# plot interplated data
def plt_exact(data, cols=[1,2], kind='linear', lims=[-0.5,0.5], num=200,
              marker='-'):
    x_new = np.linspace(lims[0], lims[1], num)
    if (type(kind) == list):
        for i in range(len(kind)):
            f_exact = interp1d_data(data, cols, kind[i])
            plt.plot(x_new, f_exact(x_new), marker, label=kind[i])
    else:
        f_exact = interp1d_data(data, cols, kind)
        plt.plot(x_new, f_exact(x_new), marker, label=kind)
    plt.legend(loc="best")


#################
# DataSet Class #
#################

class DataSet(ds.DataSet):
    def __init__(self, dirs, files, cols=None):
        ds.DataSet.__init__(self, dirs, files, cols)
        self.diffset = []
        self.normset = []
        self.convset = []

    def getDiffSet(self):
        return self.diffset
    def getNormSet(self):
        return self.normset
    def getConvSet(self):
        return self.convset

    def diff(self, f_exact):
        self.diffset.clear()
        for d in self.dataset:
            self.diffset.append(diff_data(d, f_exact))

    def norm(self, order=1):
        self.normset.clear()
        for d in self.diffset:
            self.normset.append(pow(simpson([pow(x[1],order) for x in d],
                                            [x[0] for x in d]), 1/order))

    def conv(self):
        self.convset.clear()
        for i in range(len(self.normset)-1):
            self.convset.append(math.log(self.normset[i]/self.normset[i+1], 2))

    # wrapper
    def calcAll(self, f_exact, order=1):
        self.diff(f_exact)
        self.norm(order)
        self.conv()

    # plot functions
    def pltData(self, cols=[1,2], marker='-', labels=False, lims=False,
                fx=lambda x,i:x, fy=lambda x,i:x,
                savefig=False, fig_name='data.pdf',
                num_ref=200, f_exact=None):
        ds.pltSet(self.dataset, self.dictset, cols, marker, labels, lims,
                  fx, fy)
        if(f_exact is not None):
            data0 = self.dataset[0]
            x_new = np.linspace(data0[2,0], data0[len(data0)-3,0], num_ref)
            plt.plot(x_new, f_exact(x_new), marker, label='exact')
        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

    def pltDiff(self, cols=[1,2], marker='-', labels=False, lims=False,
                fx=lambda x,i:x, fy=lambda x,i:x,
                savefig=False, fig_name='diff.pdf'):
        ds.pltSet(self.diffset, self.dictset, cols, marker, labels, lims,
                  fx, fy)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

# end of plot_tools.py
