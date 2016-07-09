from getV import Structure
from getSample import Sample
from numpy import *
import json

JSON_FILE = "data/sample_data.json"

class Data:
    def getData(self,path,numvisit):

        fh = open(path,'r')
        data = json.load(fh)
        s = Sample()
        sample=s.getSample() 

        ET={}
        
        for pid in data:
            # if len(data[pid]['appt'])>=numvisit and str(pid) in sample:
            if len(data[pid]['appt'])>=numvisit:
                
                ET[pid]={}
                ET[pid]['age']=data[pid]['age']
                ET[pid]['sex']=data[pid]['sex']
                ET[pid]['race']=data[pid]['race']
                ET[pid]['marry']=data[pid]['marry']
                ET[pid]['location']=data[pid]['location']
                ET[pid]['appt']={}
                ET[pid]['lab']={}
                j=0
                for key in range(0,len(data[pid]['appt'])):
                    try:
                        ET[pid]['appt'][j]=data[pid]['appt'][str(key)]
                        j=j+1
                        
                    except Exception as e:
                        pass

                j2=0
                for key2 in range(len(data[pid]['lab'])):
                    try:
                        ET[pid]['lab'][j2]=data[pid]['lab'][str(key2)]
                        j2=j2+1    
                        
                    except Exception as e:
                        pass

        matchpt=len(ET)
        print "match patient",matchpt

        t=Structure()
        node=t.getNode(ET)
        t.getV(node,ET)

        with open(JSON_FILE, 'w') as outfile:
            json.dump(ET, outfile)

        return ET

    def matchpt(self,ET):
        matchpt=len(ET)
        return matchpt

def main():
    d=Data()
    d.getData()

if __name__ == '__main__':
    main()         
            
