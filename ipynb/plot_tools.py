# plot_tools.py
# (c) Liwei Ji 08/2022

import os
import re
import numpy as np

import matplotlib.pyplot as plt

##########
# Basics #
##########

# set limit for plt
def set_limit(plt, lims):
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
                fdata = load_data(os.path.join(d,f))
                datarow = []
                datarow.append(d)
                datarow.append(fdata)
                dataset.append(datarow)
    return dataset


########
# Plot #
########

def plot_rho(dataset, marker='-', lims=False, savefig=False):
    cols = [8, 11]
    for d in dataset:
        plt.plot([i[cols[0]-1] for i in d[1]],
                 [i[cols[1]-1] for i in d[1]],
                 marker, label=os.path.basename(d[0]))
    plt.xlabel(r'x')
    plt.ylabel(r'$\rho$')
    set_limit(plt, lims)
    plt.legend(loc="best")

    if(savefig):
        plt.savefig('./rho.pdf', bbox_inches='tight')

# end of plot_tools.py
