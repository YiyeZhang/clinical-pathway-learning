from time import gmtime, strftime
from datetime import datetime, timedelta
import sys, getopt, os, tempfile, itertools, numpy
import MySQLdb as mdb
import simplejson
import fnmatch
from numpy import *
import json
# from collections import Counter
import collections
import copy
import datetime
import numpy as np
import csv
#import getNode
#import getSample

JSON_FILE = "/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/data_full.json"

class Patient:
    def __init__(self, parameters):
        self.acct = parameters[0]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % (self.acct)

class Demographics:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.sex = parameters[1]
        self.race = parameters[2]
        self.age = parameters[3]
        self.marry=parameters[4]
        self.location=parameters[5]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % self.sex


class Appointment:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.type = parameters[2]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % self.date


class Clinical_event:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.event = parameters[2]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % (self.event)


class Diagnosis:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.diag = parameters[2]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Diag: acct:%s, diag:%s" % (self.acct, self.diag)


class Drug:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.drug = parameters[2]
        self.drugclass = parameters[3]
        self.type = parameters[4]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % (self.drug)


class Lab:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.test = parameters[2]
        self.results = parameters[3]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % (self.test)


class Vitals:
    def __init__(self, parameters):
        self.acct = parameters[0]
        self.date = str(parameters[1])
        self.bpsys = parameters[2]
        self.bpdia = parameters[3]
        self.weight = parameters[4]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s" % (self.bpsys)


class DataProcess:
    conf = dict()
    conf_filename = "conf.json"

    def __init__(self):
        config_dir = os.path.split(os.path.abspath(__file__))[0]
        # config_dir="."
        self.conf = simplejson.load(open(os.path.join(config_dir, self.conf_filename)))
        self.conn = mdb.connect(self.conf["database"], self.conf["dbuser"], self.conf["dbpass"], self.conf["dbschema"])

    def getConn(self):
        return self.conn

    def readFromDB(self):
        cur = self.conn.cursor()

        cur.execute("select distinct acct from appt_full")
        resultlist_patient = cur.fetchall()

        cur.execute(
            "select distinct acct,sex,race,DATEDIFF('2014-04-01',str_to_date(dob,'%m/%d/%Y')) / 365.25 as age,Marital_Status, Location from masters")
        resultlist_demo = cur.fetchall()

        cur.execute(
            "select distinct acct,str_to_date(date,'%m/%d/%Y'),code from procedures where code in (93975,76775)")
        resultlist_ce = cur.fetchall()

        cur.execute(
            "select distinct acct,str_to_date(date,'%m/%d/%Y'),type from appt_full where type in ('FUP','NEW', 'EXFU','HOSP','B')")
            # "select distinct acct,str_to_date(date,'%m/%d/%Y'),type from appt_full where type!='PD' and type!='VAC' and type!='' and type!='HCON' and date!='' and status!='C' and status!='N'")
        resultlist_ap = cur.fetchall()

        cur.execute("select distinct acct,str_to_date(date,'%m/%d/%Y'), code from diag where date!=''")
        resultlist_cd = cur.fetchall()

        # cur.execute(
        #     "select distinct acct,str_to_date(date,'%m/%d/%Y'), description,class,type from meds m inner join drugclass d on m.`Description`=drugname where class in ('Angiotensin converting enzyme inhibitors','Angiotensin II inhibitors','Loop diuretics','Thiazide diuretics','Potassium-sparing diuretics','Statins','Inhaled corticosteroids','Nasal steroids','Ophthalmic steroids','Topical steroids with anti-infectives','Androgens and anabolic steroids','Topical steroids','sodium_bicarb','Antigout agents','Topical antibiotics','Miscellaneous antibiotics','Calcium channel blocking agents','Antihypertensive combinations','Glycopeptide antibiotics','Antibiotics/antineoplastics','Topical non-steroidal anti-inflammatories','Nonsteroidal anti-inflammatory agents')")

        cur.execute(
            "select distinct acct,str_to_date(date,'%m/%d/%Y'), description,class,type from meds m inner join drugclass d on m.`Description`=drugname")
        resultlist_drug = cur.fetchall()

        cur.execute(
            # "select distinct acct,str_to_date(date,'%m/%d/%Y'),code,results from lab where code in ('GFR', 'Creatinine','Calcium','Albumin','Phosphorus','Carbon Dio','Potassium','Hemoglobin') and date!='' and str_to_date(date,'%m/%d/%Y')>'2009-01-01'")
            "select distinct acct,str_to_date(date,'%m/%d/%Y'),code,results from lab where date!='' and str_to_date(date,'%m/%d/%Y')>'2009-01-01'")
        resultlist_lab = cur.fetchall()

        # cur.execute(
        #     "select acct, str_to_date(date,'%m/%d/%Y'),bpsystolic, bpdiastolic, weight from vitals where date!=''")
        # resultlist_vi = cur.fetchall()

        return resultlist_lab, resultlist_drug, resultlist_cd, resultlist_ap, resultlist_ce, resultlist_demo, resultlist_patient

    def saveDataToJson(self):

        resultlist_lab, resultlist_drug, resultlist_cd, resultlist_ap, resultlist_ce, resultlist_demo, resultlist_patient = self.readFromDB()

        CE = {}
        CE_date = {}

        for res in resultlist_patient:
            p = Patient(res)

            CE[p.acct] = dict()
            CE[p.acct]['appt'] = dict()
            CE[p.acct]['lab'] = dict()
            CE_date[p.acct] = list()
            CE[p.acct]['sex'] = 'NA'
            CE[p.acct]['race'] = 'NA'
            CE[p.acct]['marry'] = 'NA'
            CE[p.acct]['location'] = 'NA'
            CE[p.acct]['age'] = -1

        for res in resultlist_demo:
            demo = Demographics(res)

            try:
                CE[demo.acct]['sex'] = demo.sex
                CE[demo.acct]['age'] = int(demo.age)
                CE[demo.acct]['race'] = demo.race
                CE[demo.acct]['marry'] = demo.marry
                CE[demo.acct]['location'] = demo.location

            except:
                pass

        for res in resultlist_ap:

            ap = Appointment(res)

            if ap.date in CE[ap.acct]['appt']:
                pass
            else:
                CE[ap.acct]['appt'][ap.date] = dict()
                CE[ap.acct]['appt'][ap.date]['type'] = 'NA'
                CE[ap.acct]['appt'][ap.date]['proc'] = list()
                CE[ap.acct]['appt'][ap.date]['diag'] = list()
                CE[ap.acct]['appt'][ap.date]['drug'] = list()
                CE[ap.acct]['appt'][ap.date]['bpsys'] = -1
                CE[ap.acct]['appt'][ap.date]['bpdia'] = -1
                CE[ap.acct]['appt'][ap.date]['bodywt'] = -1
                CE[ap.acct]['appt'][ap.date]['delta'] = 'NA'
                CE[ap.acct]['appt'][ap.date]['actualdate'] = 'NA'

            CE[ap.acct]['appt'][ap.date]['type'] = ap.type
            CE[ap.acct]['appt'][ap.date]['actualdate'] = ap.date

        # for res in resultlist_vi:
        #     vi = Vitals(res)
        #     try:
        #         if vi.date in CE[vi.acct]['appt']:
        #             if (vi.bpsys != '' and vi.bpdia != '' and vi.weight != ''):
        #                 CE[vi.acct]['appt'][vi.date]['bpsys'] = vi.bpsys
        #                 CE[vi.acct]['appt'][vi.date]['bpdia'] = vi.bpdia
        #                 CE[vi.acct]['appt'][vi.date]['bodywt'] = vi.weight
        #         else:
        #             pass
        #     except:
        #         pass

        for res in resultlist_ce:
            ce = Clinical_event(res)

            try:
                if ce.date in CE[ce.acct]['appt']:
                    # print 'add proc'
                    CE[ce.acct]['appt'][ce.date]['proc'].append(ce.event)
                    CE[ce.acct]['appt'][ce.date]['proc'] = sorted(CE[ce.acct]['appt'][ce.date]['proc'])

                else:
                    # print 'no',ce.acct,ce.date
                    pass
            except:
                pass

        for res in resultlist_cd:
            cd = Diagnosis(res)
            try:
                minus1 = datetime.datetime.strptime(cd.date, '%Y-%m-%d') - datetime.timedelta(days=1)
                minus1.strftime('%Y-%m-%d')
                minus2 = datetime.datetime.strptime(cd.date, '%Y-%m-%d') - datetime.timedelta(days=2)
                minus2.strftime('%Y-%m-%d')
                if cd.date in CE[cd.acct]['appt'] and CE[cd.acct]['appt'][cd.date] != 'HOSP' and CE[cd.acct]['appt'][
                    cd.date] != 'B':
                    CE[cd.acct]['appt'][cd.date]['diag'].append(cd.diag)
                    CE[cd.acct]['appt'][cd.date]['diag'] = sorted(CE[cd.acct]['appt'][cd.date]['diag'])
                elif minus1.strftime('%Y-%m-%d') in CE[cd.acct]['appt'] and CE[cd.acct]['appt'][cd.date] != 'HOSP' and \
                                CE[cd.acct]['appt'][cd.date] != 'B':
                    CE[cd.acct]['appt'][minus1.strftime('%Y-%m-%d')]['diag'].append(cd.diag)
                    CE[cd.acct]['appt'][minus1.strftime('%Y-%m-%d')]['diag'] = sorted(
                        CE[cd.acct]['appt'][minus1.strftime('%Y-%m-%d')]['diag'])
                elif minus2.strftime('%Y-%m-%d') in CE[cd.acct]['appt'] and CE[cd.acct]['appt'][cd.date] != 'HOSP' and \
                                CE[cd.acct]['appt'][cd.date] != 'B':
                    CE[cd.acct]['appt'][minus2.strftime('%Y-%m-%d')]['diag'].append(cd.diag)
                    CE[cd.acct]['appt'][minus2.strftime('%Y-%m-%d')]['diag'] = sorted(
                        CE[cd.acct]['appt'][minus2.strftime('%Y-%m-%d')]['diag'])
                else:
                    pass
            except KeyError as ke:
                pass

        for res in resultlist_drug:
            cdrg = Drug(res)

            try:
                plus1 = datetime.datetime.strptime(cdrg.date, '%Y-%m-%d') + datetime.timedelta(days=1)
                if cdrg.date in CE[cdrg.acct]['appt'] and cdrg.date != '1900-01-01':
                    d = dict()
                    d['name'] = cdrg.drug
                    d['class'] = cdrg.drugclass
                    d['type'] = cdrg.type
                    CE[cdrg.acct]['appt'][cdrg.date]['drug'].append(d)
                elif plus1.strftime('%Y-%m-%d') in CE[cdrg.acct]['appt'] and cdrg.date != '1900-01-01':
                    d = dict()
                    d['name'] = cdrg.drug
                    d['class'] = cdrg.drugclass
                    d['type'] = cdrg.type
                    CE[cdrg.acct]['appt'][plus1.strftime('%Y-%m-%d')]['drug'].append(d)

                if cdrg.date == '1900-01-01':
                    firstappt = min(CE[cdrg.acct]['appt'])
                    print 'first', firstappt
                    d = dict()
                    d['name'] = cdrg.drug
                    d['class'] = cdrg.drugclass
                    d['type'] = cdrg.type
                    CE[cdrg.acct]['appt'][firstappt]['drug'].append(d)

            except:
                pass

        for res in resultlist_lab:
            cl = Lab(res)
            try:
                if cl.date in CE[cl.acct]['lab']:
                    pass
                else:
                    CE[cl.acct]['lab'][cl.date] = dict()
                    CE[cl.acct]['lab'][cl.date]['GFR'] = ''
                    CE[cl.acct]['lab'][cl.date]['Creatinine'] = ''
                    CE[cl.acct]['lab'][cl.date]['Calcium'] = ''
                    CE[cl.acct]['lab'][cl.date]['Albumin'] = ''
                    CE[cl.acct]['lab'][cl.date]['Phosphorus'] = ''
                    CE[cl.acct]['lab'][cl.date]['Carbon Dio'] = ''
                    CE[cl.acct]['lab'][cl.date]['Hemoglobin'] = ''
                    CE[cl.acct]['lab'][cl.date]['Potassium'] = ''

                CE[cl.acct]['lab'][cl.date][cl.test] = cl.results
            except:
                pass

        with open(JSON_FILE, 'w') as outfile:
            json.dump(CE, outfile, indent=2, sort_keys=True, separators=(',', ': '))

        return CE


def main():
    d = DataProcess()
    d.saveDataToJson()


def testfun():
    org = ['a', 'b']
    target = ['c', 'a', 'd', 'b']


if __name__ == '__main__':
    main()
 
