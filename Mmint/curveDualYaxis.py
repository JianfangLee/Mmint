#!/usr/bin/env python

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
import os,sys
import argparse
from scipy import stats
#import seaborn as sns
import subprocess
'''
parser = argparse.ArgumentParser()
parser.add_argument('-bw','--bigwig',help="bigwig for the computeMatrix", nargs="*",metavar="FILE")
parser.add_argument('-bed','--bed',help="the regions to plot", metavar="FILE")
parser.add_argument('-after','--dnregions',help="downstream regions to plot",metavar="FILE")
parser.add_argument('-before','--upregions',help="upstream regions to plot",metavar="FILE")
parser.add_argument('-bs','--binsize',help="bins size to use", metavar="FILE")
parser.add_argument('-m','--scaleregion',help="scale the input bed regions to certain length(bp)",metavar="FILE")
parser.add_argument('-o','--outFile',help="output file name",nargs="*",metavar="FILE")
parser.add_argument('-L','--rowlabels',nargs="*",help="row labels for samples", metavar="FILE")
parser.add_argument('-n','--pdfName',help="name for pdf", metavar="FILE")
parser.add_argument('-xlab','--xaxislabel',help="Xaxis Label1",required=True)
parser.add_argument('-ylab1','--yaxislabel1',help="Yaxis Label1",required=True)
parser.add_argument('-ylab2','--yaxislabel2',help="Yaxis Label2",required=True)
'''
def run(parser):
    args = parser.parse_args()


    ##need to install computeMatrix and add it to your ~/.bashrc file
    ##pass the python variables to subprocess
    #subprocess.call("rm merge.ave.txt")
    ##iterate multiple input files
    out=[]
    for label in args.rowlabels:
        out.append(label+'.gz')
    for i in range(len(args.bigwig)):

        subprocess.call("computeMatrix scale-regions -S %s -R %s -a %s -b %s -bs %s -m %s -o %s" % (args.bigwig[i],args.bed,args.dnregions,args.upregions,args.binsize,args.scaleregion, out[i]),shell=True)


    for i in range(len(args.bigwig)):
        subprocess.call("gunzip -f %s" % out[i], shell=True)

    subprocess.call("rm merge.ave.txt", shell=True)
    #subprocess.call("rm test*", shell=True)

    #for i in range(len(args.bigwig)):
    #    subprocess.call("sh format.sh %s" % args.outFile[i],shell=True)
    subprocess.call("sh format.meth.sh %s" % out[0],shell=True)
    subprocess.call("sh format.sh %s" % out[1],shell=True)


    dt = pd.read_table("merge.ave.txt",header=None)

    array= dt.as_matrix(columns=dt.columns[0:])
    #print len(array)

    y=array
    x=np.arange((int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize))
    fig,ax1 = plt.subplots()
    fig.subplots_adjust(bottom=0.125,right=0.85)
    ax2 = ax1.twinx()

    ax1.grid(False)
    ax2.grid(False)
    ax1.plot(x,y[0],color="red",linewidth=4)
    #ax1.set_xlabel('Regions',fontsize=13)
    #ax1.set_ylabel('mCG/CG',color="red",fontsize=13)
    ax1.set_xlabel(args.xaxislabel,fontsize=13)
    ax1.set_ylabel(args.yaxislabel1,color="red",fontsize=13)
    
    ax1.set_ylim((0,1))

    ax2.plot(x,y[1],color="dodgerblue",linewidth=4)
    #ax2.set_ylabel('Signal',color="dodgerblue",fontsize=13)
    ax2.set_ylabel(args.yaxislabel2,color="dodgerblue",fontsize=13)
    ax2.set_ylim((1,(max(y[1])+1)))
    #ax2.set_yticklabels(fontsize=15)
    ax2.yaxis.set_tick_params(labelsize=13)

    ax1.set_xticks([0,int(args.upregions)/int(args.binsize),(int(args.upregions)+int(args.scaleregion))/int(args.binsize),(int(args.upregions)+int(args.scaleregion)+int(args.dnregions))/int(args.binsize)])
    ax1.set_xticklabels(['-'+str(int(args.upregions)/1000)+' kp','Start','END',str(int(args.dnregions)/1000)+' kb'],fontsize=13)
    #ax1.set_yticklabels(fontsize=15)
    ax1.yaxis.set_tick_params(labelsize=13)
    fig.savefig(str(args.pdfName) + '.pdf',figsize=(15,12))
    #fig.savefig("curveTest.pdf")
    #plt.show()

if __name__=="__main__":

    run(parser)
