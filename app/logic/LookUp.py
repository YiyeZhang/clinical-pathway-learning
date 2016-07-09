import json

class LookUp:
    def getNode(self):
        fh = open("data/nodedesc.json",'r')
        nodedesc = json.load(fh)

        return nodedesc

    def getVV(self):

        fh = open("data/VVdesc.json",'r')
        VVdesc = json.load(fh)

        return VVdesc

    def getV(self):
        fh = open("data/Vdesc.json",
                  'r')
        Vdesc = json.load(fh)

        return Vdesc

    def getO(self):
        fh = open("data/obsdesc.json",
                  'r')
        obsdesc = json.load(fh)

        return obsdesc