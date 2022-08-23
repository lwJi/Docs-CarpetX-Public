# plot_tools.py
# (c) Liwei Ji 08/2022

import os
import re
import numpy as np

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


##########
# Basics #
##########

# set limit for plt
def set_plots(plt, labels, lims):
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


#############
# Load Data #
#############

# load one file
def load_data(fullpath):
    print("loading", fullpath)
    fdata = np.loadtxt(fullpath)
    return fdata

# load multiple files in all dirs
def load_dataset(dirs, files):
    dataset = []
    for d in dirs: # go over all dirs
        for f in os.listdir(d): # go over all files in d
            if re.search(files, f):
                fdata = load_data(os.path.join(d, f))
                datarow = []
                datarow.append(os.path.basename(d)) # lowest level of dir
                datarow.append(fdata)
                dataset.append(datarow)
    return dataset


#################
# Interpolation #
#################

# interp 1d data
def interp_data(data, cols=[1,2], kind='linear'):
    x = [d[cols[0]-1] for d in data]
    y = [d[cols[1]-1] for d in data]
    f = interp1d(x, y, kind)
    return f

# interp multiple 1d data
def interp_dataset(dataset, cols=[1,2], kind='linear'):
    funcset = []
    for d in dataset:
        funcrow = []
        funcrow.append(d[0])
        funcrow.append(interp_data(d[1], cols, kind))
        funcset.append(funcrow)
    return funcset


############################################
# Calculate Difference with Exact Solution #
############################################
def diff_data(f_data, f_exact, lims=[-0.5, 0.5], num=100):
    diff = []
    x = np.linspace(lims[0], lims[1], num)
    for i in range(len(x)):
        diffrow = []
        diffrow.append(x[i])
        diffrow.append(abs(f_data(x) - f_exact(x)))
        diff.append(diffrow)
    return diff

def diff_dataset(f_set, f_exact, lims=[-0.5, 0.5], num=100):
    diffset = []
    for f in f_set:
        diffrow = []
        diffrow.append(f[0])
        diffrow.append(diff_data(f[1], f_exact, lims, num))
        diffset.append(diffrow)
    return diffset


########
# Plot #
########

def plot(dataset, cols=[1,2], marker='-',
         labels=False, lims=False,
         savefig=False):
    for d in dataset:
        plt.plot([i[cols[0]-1] for i in d[1]],
                 [i[cols[1]-1] for i in d[1]],
                 marker, label=d[0])
    set_plots(plt, labels, lims)
    plt.legend(loc="best")

    if(savefig):
        plt.savefig('./rho.pdf', bbox_inches='tight')

# end of plot_tools.py
