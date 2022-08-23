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
