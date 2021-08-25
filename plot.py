#!/usr/bin/env python3
from tkinter import *
import re
import argparse
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc
from itertools import cycle
import matplotlib.ticker as ticker
import numpy as np
from matplotlib.patches import Patch
from matplotlib.backends.backend_pgf import FigureCanvasPgf
matplotlib.backend_bases.register_backend('pdf', FigureCanvasPgf)
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('text', usetex=True)
pgf_with_latex = {
    "pgf.texsystem": "xelatex",         # use Xelatex which is TTF font aware
    "text.usetex": True,                # use LaTeX to write all text
    "font.family": "serif",             # use serif rather than sans-serif
    "font.serif": "Ubuntu",             # use 'Ubuntu' as the standard font
    "font.sans-serif": [],
    "font.monospace": "Ubuntu Mono",    # use Ubuntu mono if we have mono
    "axes.labelsize": 10,               # LaTeX default is 10pt font.
    "font.size": 10,
    "legend.fontsize": 8,               # Make the legend/label fonts a little smaller
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "pgf.rcfonts": False,               # Use pgf.preamble, ignore standard Matplotlib RC
    "pgf.preamble": [
        r'\usepackage{fontspec}',
        r'\usepackage{unicode-math}'
    ]
}

matplotlib.rcParams.update(pgf_with_latex)


linestyles = [
     (0, (1, 10)),
     (0, (1, 1)),
     (0, (1, 2)),

     (0, (5, 10)),
     (0, (5, 5)),
     (0, (5, 1)),

     (0, (3, 10, 1, 10)),
     (0, (3, 5, 1, 5)),
     (0, (3, 1, 1, 1)),

     (0, (3, 5, 1, 5, 1, 5)),
     (0, (3, 10, 1, 10, 1, 10)),
     (0, (3, 1, 1, 1, 1, 1))]

def bar_color(df,color1,color2):
    return np.where(np.array(df)>0,color1,color2).T

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iFile", help="the input file", nargs='+', required=True)
    parser.add_argument("--oFile", help="the output file", type=str, default="/tmp/plot.png")
    parser.add_argument("--plotDec", help="plot decompression measurements",  required=False, action='store_true')
    parser.add_argument("--plotDiff", help="plot difference",default=-1, type=int)
    parser.add_argument("--hLine", help="plot single measurements as horizontal line",  required=False, action='store_true')
    parser.add_argument("--labels", help="labels",default=["zstd", "pigz", "pixz", "xz", "pbzip2", "bzip2", "gzip"], nargs='+')
    parser.add_argument("--linewidths", help="line width",default=[3,3,3,3,3,3,3,3,3,3,3], nargs='+')
    parser.add_argument("--markerwidths", help="marker width",default=[5,5,5,5,5,5,5,5,5,5,5,5], nargs='+')
    parser.add_argument("--ms", help="plot y axis in ms",  required=False, action='store_true')
    parser.add_argument("--maxX", help="plot only until",  required=False, type=int)
    parser.add_argument("--title", help="the plot title", type=str, required=False)
    parser.add_argument("--xAxis", help="x axis [red, size, idx, time, direct, height, width, imgSize, var, mean]", type=str, default="size")
    parser.add_argument("--yAxis", help="y axis [red, size, idx, time, direct, height, width, imgSize, var, mean]", type=str, default="time")
    parser.add_argument("--idxLabel", help="if --*Axis was selected with idx than this defines the label for the respective axis", type=str, default="")
    parser.add_argument("--idxStartVal", help="the start value of index", type=int, default=0)

    args = parser.parse_args()
    regex_list = [re.compile(s) for s in args.labels]
    labels = [label.replace('*','').replace('^','').replace('_','').replace('$','').replace('pbzip2','pbzip2-') for label in args.labels]
    label_idx = { label : args.idxStartVal for label in labels}
    linewidths = args.linewidths

    unit = 's'
    if args.ms:
        unit = 'ms'


    colors = cycle([ "black", "aqua", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal","blue", "yellow"])
    styles = cycle(linestyles)


    data = []
    for i in range(len(labels)):
        data.append([[],[]])

    plt.rcParams["figure.figsize"] = (21,9)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    marker_size =args.markerwidths 
    marker = ["^","*",".","D","<","+", ">", "#", "~", ";", ","]

    rel_fac = [-1 for i in range(len(labels))]
    for file in args.iFile:
        lines = [l.rstrip('\n').split() for l in open(file)]
        for line in lines:
            if len(line) == 0:
                continue
            if line[1] == 'to':
                continue

            label = line[0]
            if args.plotDec and not 'DEC' in label:
                continue
            if not args.plotDec and 'DEC' in label:
                continue
            elif 'DEC' in label:
                label = label[4:]
            
            found=False 
            for i in range(0,len(labels)):   
                #if labels[i] in label:
                if regex_list[i].match(label):
                    if args.maxX and len(data[i][0]) >= args.maxX:
                        break
                    time=float(line[1])
                    red=float(line[2])
                    if len(line) == 7:
                        height = int(line[3])
                        width = int(line[4])
                        mean = float(line[5])
                        var = float(line[6])
                    print(label, " -> ", labels[i], "         ", time, " " , red)
                    if args.ms:
                        time *= 1000
                    
                    for (attr, stuff, set_label) in zip([args.xAxis, args.yAxis],[data[i][1],data[i][0]], [ax.set_xlabel,ax.set_ylabel]):
                        if attr == 'time':
                            stuff.append(time)
                            set_label("Execution Time (in %s)" % unit, fontsize=16)
                        elif attr == 'relTime':
                            if rel_fac[i] == -1:
                                rel_fac[i] = time
                            stuff.append(time/rel_fac[i]* 100.)
                            set_label("Relative Execution Time (in \%)", fontsize=16)
                        elif attr == 'red':
                            stuff.append(-red)
                            set_label("File Size Reduction (in \%)", fontsize=16)
                        elif attr == 'size':
                            # diff_(t=i) / diff_(t=1), larger diff is good
                            stuff.append(100+red)
                            set_label("Compressed File Size (in \%)", fontsize=16)
                        elif attr == 'relSize':
                            if rel_fac[i] == -1:
                                rel_fac[i] = (100.+red)
                            val=((100+red)/rel_fac[i]) * 100.
                            stuff.append(val)
                            set_label("Relative File Size(in \%)", fontsize=16)

                        elif attr == 'direct': 
                            stuff.append(int(re.search(args.labels[i], label).group(1)))
                            set_label(args.idxLabel, fontsize=16)

                        elif attr == 'imgSize':
                            stuff.append(height*width)
                            set_label("Image Size (in B)", fontsize=16)

                        elif attr == 'height':
                            stuff.append(height)
                            set_label("Image Height(in B)", fontsize=16)

                        elif attr == 'width':
                            stuff.append(width)
                            set_label("Image Width (in B)", fontsize=16)

                        elif attr == 'var':
                            stuff.append(var)
                            set_label("Image Variance", fontsize=16)

                        elif attr == 'mean':
                            stuff.append(mean)
                            set_label("Image Mean", fontsize=16)

                        else: 
                            stuff.append(label_idx[labels[i]])
                            label_idx[labels[i]] += 1
                            set_label(args.idxLabel, fontsize=16)
        #ax.set_xlabel("File Size Reduction (in \%)", fontsize=18)
        #ax.set_ylabel("Execution Time (in %s)" % unit, fontsize=15)

                    found=True 
                    break
    if args.plotDiff >= 0:
        for i in range(len(data)):
            if i == args.plotDiff:
                continue
            for j in range(min(len(data[i][0]),len(data[args.plotDiff][0]))):
                data[i][0][j] -= data[args.plotDiff][0][j]
    
    for i in range(len(data)):
        if args.plotDiff >= 0:
            if args.plotDiff == i:
                continue
            labels[i] += "-diff"

        print(labels[i], " " , len(data[i][0]), " " ,data[i])
        color = next(colors)
        linestyle = next(styles)

        if args.hLine and len(data[i][1] ) == 1:
            plt.axhline(y=data[i][0], color=color,linewidth=linewidths[i], linestyle='-')
            marker_size[i] = 0
        ax.plot(data[i][1], data[i][0], label=labels[i], color=color, linewidth=linewidths[i],  markersize=marker_size[i], marker=marker[i])
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    #ax.margins(0.1)
    fig.tight_layout()

    if not args.title:
        plt.title(args.iFile[0].split('/')[-1].replace("_","-").replace("^","-"))
    else:
        plt.title(args.title)
    plt.subplots_adjust(top=0.975)
    plt.grid(True)
    plt.savefig(args.oFile)
    plt.show()
    print(args.oFile)

if __name__ == "__main__":
    main()
