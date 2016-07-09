import json

class LookUp:
    def getNode(self):
        fh = open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/nodedesc.json",'r')
        nodedesc = json.load(fh)

        return nodedesc

    def getVV(self):

        fh = open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/VVdesc.json",'r')
        VVdesc = json.load(fh)

        return VVdesc

    def getV(self):
        fh = open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/Vdesc.json",
                  'r')
        Vdesc = json.load(fh)

        return Vdesc

    def getO(self):
        fh = open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/obsdesc.json",
                  'r')
        obsdesc = json.load(fh)

        return obsdesc