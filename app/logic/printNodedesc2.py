import json
from app.logic.LookUp import LookUp

class PrintVVNode:
    def desc(self):
        l=LookUp()
        VVdesc=l.getVV()
        VVdesclist=list()
        for v in sorted(VVdesc.iterkeys()):
            d=dict()
            d['name']=v
            d['source']=VVdesc[v][0]    
            d['target']=VVdesc[v][1]
            d['delta']=VVdesc[v][2]
            VVdesclist.append(d)

        return VVdesclist
