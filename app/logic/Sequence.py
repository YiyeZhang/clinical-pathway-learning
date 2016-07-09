import json
from LookUp import LookUp
import getVV
import processPair2
import getTr2
import getTr
import processPair
import getGraph

JSON_FILE_OUT = "data/data_out2.json"
JSON_FILE = "data/data.json"

class Sequence:    
    def getNodes(self,data):
        l=LookUp()
        nodedesc = l.getNode()

        for pid in data:
            if len(data[pid]) != 0: 
                for date in sorted(data[pid]['appt'].iterkeys()):

                    for key in nodedesc.iterkeys():

                        if len(data[pid]['appt'][date]['drugclass'])==0:
                            data[pid]['appt'][date]['drugclass']='NR'
                        if len(data[pid]['appt'][date]['drugclass'])==0:
                            data[pid]['appt'][date]['drugclass']='NR'
                        if len(data[pid]['appt'][date]['proc'])==0:
                            data[pid]['appt'][date]['proc']='NR'
                        if len(data[pid]['appt'][date]['diag'])==0:
                            data[pid]['appt'][date]['diag']='NR'

                        if data[pid]['appt'][date]['proc']==nodedesc[key]:
                            data[pid]['appt'][date]['proc']=key
                            
                        if data[pid]['appt'][date]['drugclass']==nodedesc[key]:
                            data[pid]['appt'][date]['drugclass']=key

                        if data[pid]['appt'][date]['diag']==nodedesc[key]:
                            data[pid]['appt'][date]['diag']=key


        return data

    def getSeq(self,data):
        tempVT=dict()
        VT=dict()
        tempDT=dict()
        OT={}
        l = LookUp()
        Vdesc = l.getV()
        obsdesc = l.getO()

        for pid in data:

            VT[pid]=list()
            tempDT[pid]=list()
            tempVT[pid]=list()
            OT[pid]=list()

            for date in sorted(data[pid]['appt']):
                
                for key in Vdesc.iterkeys():                    
                    a=(data[pid]['appt'][date]['type'],data[pid]['appt'][date]['diag'],data[pid]['appt'][date]['proc'],data[pid]['appt'][date]['drugclass'])
                    b=list(a)
                    if b==Vdesc[key]:
                        tempDT[pid].append(data[pid]['appt'][date]['actualdate'])
                        VT[pid].append(key)

                for key in obsdesc.iterkeys():
                    c = data[pid]['appt'][date]['obs']
                    if c==obsdesc[key]:
                        OT[pid].append(key)

        # for pid in OT:
            # for i in range(len(OT[pid])):
            #     print pid, i,'1',OT[pid][i]

        # for pid in VT:
        #     print pid, VT[pid]
        return VT,tempDT,OT

    def addTime(self,VT,tempDT):
        DT = dict()
        for pid in tempDT:
            DT[pid] = list()
            for i in range(len(tempDT[pid])-1):
                try:
                    # diff=(datetime.datetime.strptime(tempDT[pid][i+1],'%Y-%m-%d')-datetime.datetime.strptime(tempDT[pid][i],'%Y-%m-%d')).days
                    # if diff>0 and diff<122:
                       
                    #     diff='na'
                    # elif diff>=122:
                       
                    #     diff='na'
                    # else:
                    #     diff='na'
                    # DT[pid].append(diff)
                   
                    DT[pid].append('na')
                except:
                    pass
        
        visitpair=dict()
        j=0
        for pid in VT:
            for i in range(0,len(VT[pid])-1):
                try:   
                    visitpair[j]=(VT[pid][i],VT[pid][i+1],DT[pid][i])
                    j=j+1
                except:
                    pass


        return visitpair,DT

    def getTrans(self,visitpair,VT,DT):

        pairinput,pairinputdelta=processPair.processPair(visitpair)
        pairoutput=getTr.getTr(pairinput,pairinputdelta)
        getVV.getVV(pairoutput)
        visitpair2,VVseq=self.getVVseq(VT,DT)
        VVseqinput,targetct=processPair2.processPair2(visitpair2)
        VVseqoutput=getTr2.getTr2(VVseqinput,targetct)
        # finalgraph=VVseqoutput
        finalgraph=getGraph.getGraph(VVseqoutput)

        with open(JSON_FILE_OUT, 'w') as outfile:
            json.dump(finalgraph, outfile)

        return finalgraph,pairoutput,VVseq


    def getVVseq(self,VT,DT):
        l = LookUp()
        VVdesc = l.getVV()
        VVseq=dict()
        visitpair=dict()

        j=0
        for pid in VT:
            VVseq[pid]=list()
            for i in range(0,len(VT[pid])-1):
                
                visitpair[j]=list()
                visitpair[j].append(VT[pid][i])
                visitpair[j].append(VT[pid][i+1])

                try:
                    visitpair[j].append(DT[pid][i])
                except:
                    pass

                for t in VVdesc.iterkeys():
                    if visitpair[j]==VVdesc[t]:
                        VVseq[pid].append(t)
                        break

                j = j + 1

        # for pid in VVseq:
        #     for i in range(len(VVseq[pid])):
        #         print pid, i,'1',VVseq[pid][i]
                # print pid,VVseq[pid][i]

        visitpair2={}
        j=0
        for pid in VVseq:
            for i in range(0,len(VVseq[pid])-1):
                visitpair2[j]=(VVseq[pid][i],VVseq[pid][i+1])
                j=j+1
        
        return visitpair2, VVseq


        