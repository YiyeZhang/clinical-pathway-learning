import csv
from sklearn.cross_validation import KFold
from sklearn import cross_validation

class Sample:
    def getSample(self):
        sample = list()
        cr = csv.reader(open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/HMMsample.csv", "rb"))
        # cr = csv.reader(open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/Diuretics/transplant.csv","rb"))
        for row in cr:
            sample.append(row)

        return sample[0]

    def getSubgroup(self, group):
        s = list()
        sample = open(
            '/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/HMM_subgroup.csv','rU')
        sample_f = csv.reader(sample, delimiter=',')

        for row in sample_f:
            if group=='0':
                s.append(row[0])
            elif row[1] == group:
                s.append(row[0])
        return s
