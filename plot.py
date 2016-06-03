import yoda
import math
import sys
import numpy as np
import json
import os
import matplotlib
matplotlib.use('pgf')

pgf_with_custom_preamble = {
    "pgf.texsystem": "pdflatex",
    "font.family": "serif", # use serif/main font for text elements
    "text.usetex": True,    # use inline math for ticks
    "font.serif": [],
    "font.size": 10,
    "axes.labelsize": 10,
    "legend.fontsize": 10,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
}
matplotlib.rcParams.update(pgf_with_custom_preamble)
#matplotlib.rcParams['axes.color_cycle'] = ['a6cee3', '1f78b4', 'b2df8a', '33a02c']

# not color blind safe
#matplotlib.rcParams['axes.color_cycle'] = ['e41a1c', '377eb8', '4daf4a', '984ea3', 'ff7f00']

# option 3
#matplotlib.rcParams['axes.color_cycle'] = ['e66101', 'fdb863', 'b2abd2', '5e3c99']

# option 4
#matplotlib.rcParams['axes.color_cycle'] = ['000000', '1b9e77', 'd95f02', '7570b3']

# option 5
#matplotlib.rcParams['axes.color_cycle'] = ['000000', 'e66101', 'b2abd2', '5e3c99']

# option 6
#matplotlib.rcParams['axes.color_cycle'] = ['332288', '88CCEE', '999933', 'AA4499']

# option 7
#matplotlib.rcParams['axes.color_cycle'] = ['000000', 'E94837', '9bd940', 'bc50d8']

# option 8
#matplotlib.rcParams['axes.color_cycle'] = ['332288', '88CCEE', '117733', 'DDCC77']

# option 9
matplotlib.rcParams['axes.color_cycle'] = ['66aa55', 'ee3333', '11aa99', '3366aa', '992288', '66aa55', 'cccc55']

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def figsize(width_in_pt):
    inches_per_pt = 1.0/72.27
    golden_mean = (math.sqrt(5.0) - 1.0)/2.0
    figwidth = inches_per_pt * width_in_pt
    figheight = figwidth * golden_mean
    return [figwidth, figheight]


class Histogram:
    def __init__(self, filename, name):
        self.hist = None
        self.read_hist_from_yoda(filename, name)
        self.name = "test"

    def read_hist_from_yoda(self, filename, name):
        yodafile = yoda.read(filename)
        try:
            self.hist = yodafile[name]
        except:
            print "error: \"%s\" is not in \"%s\"" % (name, filename)
            exit(1)

    def value(self, x):
        return self.hist.binAt(x).height

    def values(self, x):
        y = []
        for t in x:
            y.append( self.value(t))
        return y

    def error(self, x):
        return self.hist.binAt(x).heightErr

    def errors(self, x):
        yerr = []
        for t in x:
            yerr.append( self.error(t) )
        return yerr

    def rebin(self, n):
        self.hist.rebin(n)
#        b = list(range(58, 70,4)) + list(range(70,80,2)) + list(range(80,85,1)) + list(np.arange(85,95,0.5)) + list(np.arange(95,100,1)) + list(np.arange(100,110,2)) + list(np.arange(110,122,4)) + list(np.arange(122,146,8))
        self.hist.rebin(b)

    def setname(self, name):
        self.name = name



def plot_hists(hists,config, which):
    if len(which) > 2 or len(which) < 1:
        print >> sys.stderr, "error: don't know what to plot"
        exit(1)

    if len(which) == 2:
        inormal = 0
        iratio = 1
    else:
        if which[0] == "normal":
            inormal = 0
        elif which[0] == "ratio":
            iratio = 0
    f, ax = plt.subplots(len(which),sharex=True)
    f.set_size_inches( figsize(690) )
    if len(which) == 1:
        ax = [ax]
    f.subplots_adjust(hspace=0)
    t1 = np.arange(config["xmin"], config["xmax"], 0.01)
    lines = []
    linesratio = []
    yref = hists[0].values(t1)
    yreferr = hists[0].errors(t1)
    minorLocator = AutoMinorLocator()
    ls = ['-', '-', '-', '-', '-', '-' , '-' ]
    n = 0
    for hist in hists:
        y = hist.values(t1)
        if "normal" in which:
            line, = ax[inormal].plot(t1, y, label=hist.name, linestyle=ls[n])
            lines.append(line)
        if "ratio" in which:
            ratio = [y[i]/yref[i] for i in xrange(0,len(y))]
            line, = ax[iratio].plot(t1, ratio, label=hist.name, linestyle=ls[n])
            linesratio.append(line)
            if config["errors"]:
                yerr = hist.errors(t1)
                yerrup = []
                yerrdown = []
                for i in xrange(0,len(y)):
                    err2 = (1.0/yref[i]*yreferr[i])**2 + (y[i]/yref[i]**2*yerr[i])**2
                    err = math.sqrt(err2)
                    yerrup.append( ratio[i]+err )
                    yerrdown.append( ratio[i]-err )
                col = line.get_color()
                ax[iratio].fill_between(t1, yerrup, yerrdown, alpha=config["errorsalpha"], color=col)
        n += 1
    if "normal" in which:
        ax[inormal].legend( handles=lines )
        ax[inormal].set_yscale(config["yscale"])
        axis = ax[inormal].axis()
        newaxis = list(axis)
        newaxis[0] = config["xmin"]
        newaxis[1] = config["xmax"]
        ax[inormal].axis(newaxis)
        ax[inormal].grid(False)
        ax[inormal].xaxis.set_minor_locator(minorLocator)
        ax[inormal].set_xlabel(config["xlabel"])
        if "ratio" in which:
            ax[inormal].set_xlabel('')
        ax[inormal].set_ylabel(config["ylabel"])
        ax[inormal].set_title(config["title"],loc=config["titleloc"])
    if "ratio" in which:
        axis = ax[iratio].axis()
        newaxis = list(axis)
        newaxis[0] = config["xmin"]
        newaxis[1] = config["xmax"]
        ax[iratio].axis(newaxis)
        ax[iratio].xaxis.grid(False)
        ax[iratio].xaxis.set_minor_locator(minorLocator)
        ax[iratio].yaxis.set_minor_locator(AutoMinorLocator())
        ax[iratio].set_xlabel(config["xlabel"])
        ax[iratio].set_ylabel(config["rlabel"])
        if not "normal" in which:
            ax[iratio].legend( handles=linesratio )
            ax[iratio].set_title(config["title"],loc=config["titleloc"])
        else:
            ax[iratio].yaxis.get_major_ticks()[-1].label1.set_visible(False)
            ax[inormal].yaxis.get_major_ticks()[0].label1.set_visible(False)
            ax[iratio].xaxis.set_ticks_position('bottom')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print >> sys.stderr, "error: no input file"
        print >> sys.stderr, "  usage: %s FILE" % sys.argv[0]
        exit(1)

    filename = sys.argv[1]

    if not os.path.exists(filename):
        print >> sys.stderr, "error: could not open file: %s" % filename
        exit(1)


    infile = json.load(open(filename, 'r'))
    histograms = infile["histograms"]
    config = infile["config"]
    which = infile["which"]

    hists = []
    for hist in histograms:
        h = Histogram( hist["filename"], hist["plot"] )
        h.setname(hist["label"])
        h.rebin(int(config["rebin"]))
        hists.append(h)

    plot_hists(hists, config, which)

    for f in infile["outfiles"]:
        plt.savefig(f)

