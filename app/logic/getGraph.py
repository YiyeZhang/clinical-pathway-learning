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

def getGraph(result,weight,count):
    sourcelist=list()
    for i in range(0,len(result)):
        sourcelist.append(result[i]['source'])
    sourcelist=list(set(sourcelist))
    finalresult=copy.copy(result)
    
    for i in range(0,len(result)):             
        # if result[i]['count']>=float(count):
        #     pass
        if (result[i]['count']>=float(count) and result[i]['weight']>=float(weight)):
            pass                     
        else:
            # print 'remove'
            finalresult.remove(result[i])
            
    # for i in range(len(finalresult)):
    #     print finalresult[i]['source'],finalresult[i]['target'],finalresult[i]['weight']
    # for i in range(len(finalresult)):
    #     print finalresult[i]
    
    return finalresult
