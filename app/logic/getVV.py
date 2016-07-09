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
        # if result[i]['source'][0]=='A':
        #     s=result[i]['source'][0]+result[i]['source'][3]
        # else:
        #     s=result[i]['source'][0]
        # if result[i]['target'][0]=='A':
        #     t=result[i]['target'][0]+result[i]['target'][3]
        # else:
        #     t=result[i]['target'][0]
        # s=result[i]['source'][0]
        # t=result[i]['target'][0]
        
        # VV[i]=(s,t,'na')
        VVlist.append(VV[i])

    # onlyonce=list()
    # c=Counter(map(tuple,VVlist))
    # for i in c:
    #     if c[i]<=2:
    #         onlyonce.append(i)

    d_VVlist=[list(t) for t in set(map(tuple, VVlist))]

    VVdesc=dict()
    for t in range(0,len(d_VVlist)):
        # VVdesc['VV'+str(t+1)]=d_VVlist[t]

        # if d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI1_ACAR')>-1:
        #     VVdesc['AKI1_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI2_ACAR')>-1:
        #     VVdesc['AKI2_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI3_ACAR')>-1:
        #     VVdesc['AKI3_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI4_ACAR')>-1:
        #     VVdesc['AKI4_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI5_ACAR')>-1:
        #     VVdesc['AKI5_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI6_ACAR')>-1:
        #     VVdesc['AKI6_ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI_ACAR')>-1:
        #     VVdesc['AKI_ACAR'+str(t)]=d_VVlist[t]
        #
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI1_ACE')>-1:
        #     VVdesc['AKI1_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI2_ACE')>-1:
        #     VVdesc['AKI2_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI3_ACE')>-1:
        #     VVdesc['AKI3_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI4_ACE')>-1:
        #     VVdesc['AKI4_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI5_ACE')>-1:
        #     VVdesc['AKI5_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI6_ACE')>-1:
        #     VVdesc['AKI6_ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI_ACE')>-1:
        #     VVdesc['AKI_ACE'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI1_ARB')>-1:
        #     VVdesc['AKI1_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI2_ARB')>-1:
        #     VVdesc['AKI2_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI3_ARB')>-1:
        #     VVdesc['AKI3_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI4_ARB')>-1:
        #     VVdesc['AKI4_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI5_ARB')>-1:
        #     VVdesc['AKI5_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI6_ARB')>-1:
        #     VVdesc['AKI6_ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('AKI_ARB')>-1:
        #     VVdesc['AKI_ARB'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('1acar')>-1:
        #     VVdesc['1ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('2acar')>-1:
        #     VVdesc['2ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('3acar')>-1:
        #     VVdesc['3ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('4acar')>-1:
        #     VVdesc['4ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('5acar')>-1:
        #     VVdesc['5ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('6acar')>-1:
        #     VVdesc['6ACAR'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('acar')>-1:
        #     VVdesc['ACAR'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('1ace')>-1:
        #     VVdesc['1ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('2ace')>-1:
        #     VVdesc['2ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('3ace')>-1:
        #     VVdesc['3ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('4ace')>-1:
        #     VVdesc['4ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('5ace')>-1:
        #     VVdesc['5ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('6ace')>-1:
        #     VVdesc['6ACE'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('ace')>-1:
        #     VVdesc['ACE'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('1arb')>-1:
        #     VVdesc['1ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('2arb')>-1:
        #     VVdesc['2ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('3arb')>-1:
        #     VVdesc['3ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('4arb')>-1:
        #     VVdesc['4ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('5arb')>-1:
        #     VVdesc['5ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('6arb')>-1:
        #     VVdesc['6ARB'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('arb')>-1:
        #     VVdesc['ARB'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('1aki')>-1:
        #     VVdesc['AKI1'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('2aki')>-1:
        #     VVdesc['AKI2'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('3aki')>-1:
        #     VVdesc['AKI3'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('4aki')>-1:
        #     VVdesc['AKI4'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('5aki')>-1:
        #     VVdesc['AKI5'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('6aki')>-1:
        #     VVdesc['AKI6'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('aki')>-1:
        #     VVdesc['AKI'+str(t)]=d_VVlist[t]
        #
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_1_')>-1:
        #     VVdesc['1_'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_2_')>-1:
        #     VVdesc['2_'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_3_')>-1:
        #     VVdesc['3_'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_4_')>-1:
        #     VVdesc['4_'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_5_')>-1:
        #     VVdesc['5_'+str(t)]=d_VVlist[t]
        # elif d_VVlist[t]!='' and str(d_VVlist[t]).find('_6_')>-1:
        #     VVdesc['6_'+str(t)]=d_VVlist[t]

        if d_VVlist[t]!='':
            VVdesc['VV'+str(t)]=d_VVlist[t]
       
    
    with open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/VVdesc.json", 'w') as outfile:
        json.dump(VVdesc, outfile)  
    
    
    return VVdesc

