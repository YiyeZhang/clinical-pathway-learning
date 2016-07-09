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

def processPair2(pair):
    l=list()
    input=dict()
    targetct=list()
        
    for k,v in pair.values():
        if (type(k)!=list and type(v)!=list):
            l.append(k)
            input[k]=list()
            targetct.append(v)
            
    distinctl=set(l)

    for k,v in pair.values():
        if (type(k)!=list and type(v)!=list):
            for i in distinctl:
                if k ==i:
                    input[k].append(v)
                    
    return input,targetct