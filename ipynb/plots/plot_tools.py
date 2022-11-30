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
def plt_exact(data, cols=[1,2], kind='linear', lims=[-0.5,0.5], num=200):
    x_new = np.linspace(lims[0], lims[1], num)
    if (type(kind) == list):
        for i in range(len(kind)):
            f_exact = interp1d_data(data, cols, kind[i])
            plt.plot(x_new, f_exact(x_new), label=kind[i])
    else:
        f_exact = interp1d_data(data, cols, kind)
        plt.plot(x_new, f_exact(x_new), label=kind)
    plt.legend(loc="best")


###############################
# Scaling Plot Data Set Class #
###############################
class ScalingSet:
    def __init__(self, data, fx=lambda x:x, fy=lambda y:y):
        self.dataset = [[], [], []]
        for d in data:
            self.dataset[0].append(fx(d[0]))
            self.dataset[1].append(fy(d[1]))

    def fitdata(self, fit_range=None):
        if(fit_range is None):
            fit_range = slice(0,len(self.dataset))
        fit = np.poly1d(np.polyfit(np.array(self.dataset[0][fit_range]),
                                   np.array(self.dataset[1][fit_range]), 1))
        print(fit)
        self.dataset[2] = fit(self.dataset[0])


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

    def diff(self, f_exact, difflims=None):
        self.diffset.clear()
        for d in self.dataset:
            self.diffset.append(diff_data(d, f_exact))
        if(difflims is not None):
            for d in self.diffset:
                for i in range(len(d)):
                    if(d[i][0]<difflims[0] or d[i][0]>difflims[1]):
                        d[i][1] = 0


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
    def pltData(self, cols=[1,2], fx=lambda x,i:x, fy=lambda x,i:x, markers='-',
                savefig=False, fig_name='data.pdf', num_ref=200, f_exact=None):
        ds.pltSet(self.dataset, self.dictset, cols, fx, fy, markers)
        if(f_exact is not None):
            data0 = self.dataset[0]
            x_new = np.linspace(data0[2,0], data0[len(data0)-3,0], num_ref)
            plt.plot(x_new, f_exact(x_new), label='exact')
        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

    def pltDiff(self, cols=[1,2], fx=lambda x,i:x, fy=lambda x,i:x, markers='-',
                savefig=False, fig_name='diff.pdf'):
        ds.pltSet(self.diffset, self.dictset, cols, fx, fy, markers)
        plt.legend(loc="best")
        if(savefig):
            plt.savefig(fig_name, bbox_inches='tight')

# end of plot_tools.py
