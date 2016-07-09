import json
from app.logic.LookUp import LookUp

class PrintNode:
    def desc(self):
        l=LookUp()
        nodedesc = l.getNode()
        Vdesc = l.getV()

        nodedesclist=list()
        for v in sorted(Vdesc.iterkeys()):
            d=dict()
            d['name']=v
            d['type']=Vdesc[v][0]+'type'
            d['diagnosis']=sorted(nodedesc.get(Vdesc[v][1],'-'))
            # d['diagnosis']=Vdesc[v][1]
            d['proc']=nodedesc.get(Vdesc[v][2],'-')
            d['med']=nodedesc.get(Vdesc[v][3],'-')
            nodedesclist.append(d)

        # for v in sorted(Vdesc.iterkeys()):
        #     d=dict()
        #     newv=[x.strip() for x in v.split(',')]
        #     newv2=[y.replace("u","") for y in newv]
        #     newv3=[z.replace("'","") for z in newv2]
        #     newv4=[z.replace("[","") for z in newv3]
        #     newv5=[z.replace("]","") for z in newv4]
        #     # print newv3[0],'d',newv3[1],'d',newv3[2],'d',newv3[3]
        #     d['name']=Vdesc[v]
        #     d['type']=newv5[0]+'type'
        #     d['diagnosis']=sorted(nodedesc.get(newv5[1],'-'))
        #     # d['diagnosis']=Vdesc[v][1]
        #     # d['proc']=nodedesc.get(newv5[2],'-')
        #     d['med']=nodedesc.get(newv5[2],'-')
        #     nodedesclist.append(d)
            # print d['type'],d['diagnosis'],d['proc'],d['med']
        
        return nodedesclist