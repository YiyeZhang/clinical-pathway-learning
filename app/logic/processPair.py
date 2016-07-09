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

def processPair(pair):
        l=list()
        input=dict()
        inputdelta=dict()
        
        for k,v,f in pair.values():
            if (type(k)!=list and type(v)!=list):
                # print k,v
                l.append(k)
                input[k]=list()
                inputdelta[k]=dict()
                
        distinctl=set(l)

        for k,v,f in pair.values():
            inputdelta[k][v]=list()

        for k,v,f in pair.values():
            if (type(k)!=list and type(v)!=list):
                for i in distinctl:
                    if k ==i:
                        input[k].append(v)
                        inputdelta[k][v].append(f)
        # print inputdelta    
        return input,inputdelta