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

def getTr(input,inputdelta):
        # print "input",input
        # print "inputdelta",inputdelta
        result=list()
        result_detail=list()
        output={}
        output_detail={}
        j=0
        total=0
        for key in input.iterkeys():            
            c=Counter(input[key])
            
            for i in c:
                for j in range(len(inputdelta[key][i])):
                    output[j]={}
                    output[j]['source']=key
                    output[j]['target']=i
                    output[j]['weight']=float(c[i])/len(input[key])
                    output[j]['count']=c[i]
                    output[j]['count_source']=len(input[key])
                    output[j]['count_target']=0
                    output[j]['delta']=inputdelta[key][i][j]
                    result.append(output[j])
                j=j+1
                total=total+float(c[i])
        # for f in range(len(result)):
        #     print result[f]['source'],result[f]['target'],result[f]['delta']
        return result