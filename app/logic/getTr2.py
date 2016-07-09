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

def getTr2(input,targetct):
    result=list()
    result_detail=list()
    output={}
    output_detail={}
    j=0
    total=0
    t=Counter(targetct)
    # print input
    # print t
    for key in input.iterkeys():
            c=Counter(input[key])
            for i in c:
                output[j]={}
                output[j]['source']=key
                output[j]['target']=i
                output[j]['weight']=float(c[i])/len(input[key])
                output[j]['count']=c[i]
                output[j]['count_source']=len(input[key])
                try:
                    for tc in t:
                        if tc==i:
                            output[j]['count_target']=t[tc]
                        else:
                            pass
                except:
                    pass
                result.append(output[j])
                j=j+1
                total=total+float(c[i])
            # print key,input[key]

    
    return result
    