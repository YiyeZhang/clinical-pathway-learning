import json

class LookUp:
    def getNode(self):
        fh = open("/Users/yiyezhang/github/clinical-pathway-learning/data/nodedesc.json",'r')
        nodedesc = json.load(fh)

        return nodedesc

    def getVV(self):

        fh = open("/Users/yiyezhang/github/clinical-pathway-learning/data/VVdesc.json",'r')
        VVdesc = json.load(fh)

        return VVdesc

    def getV(self):
        fh = open("/Users/yiyezhang/github/clinical-pathway-learning/data/Vdesc.json",
                  'r')
        Vdesc = json.load(fh)

        return Vdesc

    def getO(self):
        fh = open("/Users/yiyezhang/github/clinical-pathway-learning/data/obsdesc.json",
                  'r')
        obsdesc = json.load(fh)

        return obsdesc