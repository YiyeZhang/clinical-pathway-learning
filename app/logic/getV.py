from numpy import *
import json

class Structure:
    def getNode(self,ET):
        data = ET
        diaglist = list()
        for pid in data:
            if len(data[pid]) != 0:
                for date in data[pid]['appt']:
                    if len(data[pid]['appt'][date]['diag']) != 0:
                        diaglist.append(data[pid]['appt'][date]['diag'])

        diaglist_distinct = [list(t) for t in set(map(tuple, diaglist))]

        proclist = list()
        for pid in data:
            if len(data[pid]) != 0:
                for date in data[pid]['appt']:
                    if len(data[pid]['appt'][date]['proc']) != 0:
                        proclist.append(data[pid]['appt'][date]['proc'])

        proclist_distinct = [list(t) for t in set(map(tuple, proclist))]

        druglist = list()
        for pid in data:
            if len(data[pid]) != 0:
                for date in data[pid]['appt']:
                    if len(data[pid]['appt'][date]['drugclass']) != 0:
                        if data[pid]['appt'][date]['drugclass'] != '"':
                            druglist.append(data[pid]['appt'][date]['drugclass'])

        druglist_distinct = [list(t) for t in set(map(tuple, druglist))]

        nodedesc = dict()

        for t in range(0, len(proclist_distinct)):
            if proclist_distinct[t] != '':
                nodedesc['P' + str(t)] = proclist_distinct[t]
        for x in range(0, len(druglist_distinct)):
            if druglist_distinct[x] != '':
                nodedesc['M' + str(x)] = druglist_distinct[x]
        for s in range(0, len(diaglist_distinct)):
            if diaglist_distinct[s] != '':
                nodedesc['D' + str(s)] = diaglist_distinct[s]

        with open("/Users/yiyezhang/github/clinical-pathway-learning/data/nodedesc.json",
                  'w') as outfile:
            json.dump(nodedesc, outfile)

        return nodedesc

    def getV(self,nodedesc,data):

        ETpair={}
        for pid in data:
            ETpair[pid]=dict()
            ETpair[pid]['diag']=list()
            ETpair[pid]['drugclass']=list()
            ETpair[pid]['proc']=list()

            if len(data[pid]) != 0:
                for date in data[pid]['appt']:
                    for key in nodedesc.iterkeys():
                        if len(data[pid]['appt'][date]['diag'])==0:
                            data[pid]['appt'][date]['diag']='NR'
                        if len(data[pid]['appt'][date]['drugclass'])==0:
                            data[pid]['appt'][date]['drugclass']='NR'
                        if len(data[pid]['appt'][date]['proc'])==0:
                            data[pid]['appt'][date]['proc']='NR'

                        if data[pid]['appt'][date]['diag']==nodedesc[key]:
                            data[pid]['appt'][date]['diag']=key
                            # for row in nd:
                            #     if key==row[0]:
                            #         data[pid]['appt'][date]['diag']=row[1]

                        if data[pid]['appt'][date]['proc']==nodedesc[key]:
                            data[pid]['appt'][date]['proc']=key


                        if data[pid]['appt'][date]['drugclass']==nodedesc[key]:
                            data[pid]['appt'][date]['drugclass']=key


                    if data[pid]['appt'][date]['diag']!='NR':
                        ETpair[pid]['diag'].append(data[pid]['appt'][date]['diag'])
                    if data[pid]['appt'][date]['drugclass']!='NR' and data[pid]['appt'][date]['drugclass']!='' and len(data[pid]['appt'][date]['drug'])>0:
                        ETpair[pid]['drugclass'].append(data[pid]['appt'][date]['drugclass'])
                    if data[pid]['appt'][date]['proc']!='NR':
                        ETpair[pid]['proc'].append(data[pid]['appt'][date]['proc'])

        visitlist=dict()
        w=0
        for pid in data:
            for date in data[pid]['appt']:
                visitlist[w]=list()
                visitlist[w].append(data[pid]['appt'][date]['type'])
                visitlist[w].append(data[pid]['appt'][date]['diag'])
                visitlist[w].append(data[pid]['appt'][date]['proc'])
                visitlist[w].append(data[pid]['appt'][date]['drugclass'])
                w=w+1

        d_visitlist=list()
        for w in range(0,len(visitlist)):
            d_visitlist.append(visitlist[w])
        
        onlyonce=list()

        try:
            d_visitlist=[list(t) for t in set(map(tuple, d_visitlist))]
        except TypeError as e:
            # print d_visitlist
            raise e

        Vdesc=dict()
        for t in range(0,len(d_visitlist)):
            if d_visitlist[t]!='' and tuple(d_visitlist[t]) not in onlyonce:
                Vdesc['V'+str(t)]=d_visitlist[t]


        with open("/Users/yiyezhang/github/clinical-pathway-learning/data/Vdesc.json", 'w') as outfile:
            json.dump(Vdesc, outfile)

        return Vdesc