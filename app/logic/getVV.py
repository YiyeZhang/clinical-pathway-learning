from time import gmtime, strftime
from datetime import datetime,timedelta
import sys,getopt,os,tempfile,itertools,numpy
import MySQLdb as mdb
import simplejson
import fnmatch
from numpy import *
import json
from collections import Counter
import collections
import copy
import datetime
import numpy as np

def getVV(result):
    
    VV=dict()
    VVlist=list()
    
    for i in range(len(result)):
        VV[i]=(result[i]['source'],result[i]['target'],result[i]['delta'])

        VVlist.append(VV[i])

    d_VVlist=[list(t) for t in set(map(tuple, VVlist))]

    VVdesc=dict()
    for t in range(0,len(d_VVlist)):

        if d_VVlist[t]!='':
            VVdesc['VV'+str(t)]=d_VVlist[t]
       
    
    with open("data/VVdesc.json", 'w') as outfile:
        json.dump(VVdesc, outfile)  
    
    
    return VVdesc

