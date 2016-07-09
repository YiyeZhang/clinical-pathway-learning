from datetime import datetime, timedelta
from numpy import *
import json
import copy
import datetime

# import getNode
# import getSample

JSON_FILE = "/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/data_full.json"


# JSON_FILE_OUT = "/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/data_out2.json"

class DataProcess:
    def attachHOSP(self):
        fh = open(JSON_FILE, 'r')
        data = json.load(fh)

        # for pid in data:
        #     b=0
        #     for date in data[pid]['appt']:
        #         if (data[pid]['appt'][date]['type']=='B' or data[pid]['appt'][date]['type']=='HOSP'):
        #             b=b+1
        # print pid,b

        data2 = copy.deepcopy(data)

        for pid in data:
            try:
                for date in sorted(data[pid]['appt'].iterkeys()):

                    if data[pid]['appt'][date]['type'] == 'HOSP':

                        plus = []
                        for i in range(1, 8):
                            plus_t = datetime.datetime.strptime(date, '%Y-%m-%d') + datetime.timedelta(days=i)
                            plus.append(plus_t.strftime('%Y-%m-%d'))

                        for p in plus:
                            try:
                                if data[pid]['appt'][p]['type'] == 'B':
                                    for key in range(len(data[pid]['appt'][p]['diag'])):
                                        data2[pid]['appt'][date]['diag'].append(data2[pid]['appt'][p]['diag'][key])
                                    del data2[pid]['appt'][p]
                            except:
                                pass
            except:
                pass

        return data2

    def sortLab(self, data):
        apptTimeline = dict()
        R = dict()
        for pid in data:
            apptTimeline[pid] = list()
            for l in data[pid]['appt'].iterkeys():
                if datetime.datetime.strptime(l, '%Y-%m-%d') > datetime.datetime.strptime('2009-1-1', '%Y-%m-%d'):
                    apptTimeline[pid].append(l)
            apptTimeline[pid] = sorted(apptTimeline[pid])

        for pid in data:
            R[pid] = dict()
            R[pid]['lab'] = dict()
            addedlab = []

            for i in range(len(apptTimeline[pid])):

                R[pid]['lab'][i] = {}
                for labdate in sorted(data[pid]['lab'].iterkeys()):
                    if (labdate not in addedlab and labdate <= apptTimeline[pid][i]):

                        for labname in sorted(data[pid]['lab'][labdate]):
                            if labname not in R[pid]['lab'][i]:
                                try:
                                    R[pid]['lab'][i][labname] = float(data[pid]['lab'][labdate][labname])

                                except ValueError as ve:

                                    R[pid]['lab'][i][labname] = 0
                            elif (labname in R[pid]['lab'][i] and R[pid]['lab'][i][labname] == 0 and
                                          data[pid]['lab'][labdate][labname] != ''):
                                try:
                                    R[pid]['lab'][i][labname] = float(data[pid]['lab'][labdate][labname])

                                except Exception as e:
                                    pass

                            elif (labname in R[pid]['lab'][i] and R[pid]['lab'][i][labname] != 0 and
                                          data[pid]['lab'][labdate][labname] != ''):

                                try:
                                    R[pid]['lab'][i][labname] = (float(R[pid]['lab'][i][labname]) + float(
                                        data[pid]['lab'][labdate][labname])) / 2
                                except Exception as e:
                                    pass

                        addedlab.append(labdate)
            R[pid]['lab'][i + 1] = {}
            for labdate in sorted(data[pid]['lab'].iterkeys()):
                try:
                    if (labdate not in addedlab and labdate > max(apptTimeline[pid])):
                        for labname in sorted(data[pid]['lab'][labdate]):
                            if labname not in R[pid]['lab'][i + 1]:

                                try:
                                    R[pid]['lab'][i + 1][labname] = float(data[pid]['lab'][labdate][labname])

                                except ValueError as ve:
                                    # print "value error", ve
                                    R[pid]['lab'][i + 1][labname] = 0
                            elif (labname in R[pid]['lab'][i + 1] and R[pid]['lab'][i + 1][labname] == 0 and
                                          data[pid]['lab'][labdate][labname] != ''):

                                try:
                                    R[pid]['lab'][i + 1][labname] = float(data[pid]['lab'][labdate][labname])

                                except Exception as e:
                                    # print data[pid]['lab'][labdate][labname]
                                    pass

                            elif (labname in R[pid]['lab'][i + 1] and R[pid]['lab'][i + 1][labname] != 0 and
                                          data[pid]['lab'][labdate][labname] != ''):
                                try:
                                    R[pid]['lab'][i + 1][labname] = (float(R[pid]['lab'][i + 1][labname]) + float(
                                        data[pid]['lab'][labdate][labname])) / 2

                                except Exception as e:
                                    # print data[pid]['lab'][labdate][labname]
                                    pass
                        addedlab.append(labdate)
                except:
                    pass

        return R

    def timeLine(self, data):
        # fh = open (JSON_FILE,'r')
        # data = json.load(fh)
        for pid in data:
            if 'appt' not in data[pid]:
                data[pid]['appt'] = {}
            if 'marry' not in data[pid]:
                data[pid]['marry'] = 'NA'
            if 'location' not in data[pid]:
                data[pid]['location'] = 'NA'

        sortedlab = self.sortLab(data)
        CE_sorted = {}
        CE_date = {}
        for pid in data:
            CE_date[pid] = list()
            CE_sorted[pid] = {}
            CE_sorted[pid]['appt'] = {}
            CE_sorted[pid]['lab'] = {}
            CE_sorted[pid]['sex'] = data[pid].get('sex', 'NA')
            CE_sorted[pid]['race'] = data[pid].get('race', 'NA')
            CE_sorted[pid]['age'] = data[pid].get('age')
            CE_sorted[pid]['marry'] = data[pid].get('marry')
            CE_sorted[pid]['location'] = data[pid].get('location')

            i = 0

            for key in sorted(data[pid]['appt'].iterkeys()):
                if len(data[pid]['appt']) != 0:
                    CE_sorted[pid]['appt'][i] = data[pid]['appt'][key]
                    i = i + 1

            if ('lab' in data[pid] and pid in sortedlab):
                CE_sorted[pid]['lab'] = sortedlab[pid]['lab']

        for pid in data:
            for key in sorted(data[pid]['appt'].iterkeys()):
                try:
                    tkey = datetime.datetime.strptime(key, '%Y-%m-%d')
                    CE_date[pid].append(tkey)
                except:
                    pass

        for pid in CE_sorted:
            for d in range(0, len(CE_date[pid])):
                try:
                    delta = CE_date[pid][d + 1] - CE_date[pid][d]
                    if delta >= timedelta(days=1) and delta < timedelta(days=93):
                        tdelta = 'less than 3 months'
                    elif delta >= timedelta(days=93) and delta < timedelta(days=186):
                        tdelta = '3 - 6 months'
                    elif delta >= timedelta(days=186):  # and delta<timedelta (days = 365):
                        tdelta = 'at least 6 months'
                    else:
                        tdelta = 'unknown'
                    CE_sorted[pid]['appt'][d]['delta'] = tdelta

                except Exception as e:
                    pass
        return CE_sorted

    def CreateObs(self, data):
        for pid in data:
            for date in data[pid]['appt']:
                data[pid]['appt'][date]['obs'] = list()
                data[pid]['appt'][date]['stage'] = 'n/a'
                data[pid]['appt'][date]['aki'] = 'n/a'

        # if want to keep/omit CKD from hiden states
        for pid in data:
            for date in data[pid]['appt']:
                if 'CKD1' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '1'
                    # data[pid]['appt'][date]['diag'].remove('CKD1')
                if 'CKD2' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '2'
                    # data[pid]['appt'][date]['diag'].remove('CKD2')
                if 'CKD3' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '3'
                    # data[pid]['appt'][date]['diag'].remove('CKD3')
                if 'CKD4' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '4'
                    # data[pid]['appt'][date]['diag'].remove('CKD4')
                if 'CKD5' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '5'
                    # data[pid]['appt'][date]['diag'].remove('CKD5')
                if 'CKD6' in data[pid]['appt'][date]['diag']:
                    data[pid]['appt'][date]['stage'] = '6'
                    # data[pid]['appt'][date]['diag'].remove('CKD6')
                if 'AKI' in data[pid]['appt'][date]:
                    data[pid]['appt'][date]['aki']=='aki'

        for pid in data:
            for date in data[pid]['appt']:
                if data[pid]['appt'][date]['type'] == 'H':
                    data[pid]['appt'][date]['obs'].append('HOSP')
                else:
                    data[pid]['appt'][date]['obs'].append(data[pid]['appt'][date]['stage'])
                    try:
                        data[pid]['appt'][date]['obs'].append(data[pid]['lab'][date]['Albumin'])
                    except:
                        data[pid]['appt'][date]['obs'].append('n/a')
                    try:
                        data[pid]['appt'][date]['obs'].append(data[pid]['lab'][date]['Calcium'])
                    except:
                        data[pid]['appt'][date]['obs'].append('n/a')
                    try:
                        data[pid]['appt'][date]['obs'].append(data[pid]['lab'][date]['Carbon Dio'])
                    except:
                        data[pid]['appt'][date]['obs'].append('n/a')
                    try:
                        data[pid]['appt'][date]['obs'].append(data[pid]['lab'][date]['Hemoglobin'])
                    except:
                        data[pid]['appt'][date]['obs'].append('n/a')
                    try:
                        data[pid]['appt'][date]['obs'].append(data[pid]['lab'][date]['Phosphorus'])
                    except:
                        data[pid]['appt'][date]['obs'].append('n/a')

        for date in data['12037']['appt']:
            print data['12037']['appt'][date]['diag']
            print data['12037']['appt'][date]['obs']

        return data

    def ObsList(self, data):
        obslist = list()
        for pid in data:
            if len(data[pid]) != 0:
                for date in data[pid]['appt']:
                    if len(data[pid]['appt'][date]['obs']) != 0:
                        obslist.append(data[pid]['appt'][date]['obs'])

        obslist_distinct = [list(t) for t in set(map(tuple, obslist))]

        obsdesc = dict()
        for t in range(0, len(obslist_distinct)):
            if obslist_distinct[t] != '':
                obsdesc['O' + str(t)] = obslist_distinct[t]

        with open("/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/obsdesc.json",
                  'w') as outfile:
            json.dump(obsdesc, outfile)
        return obslist_distinct

    def cleanData(self, data):
        for pid in data:

            # if type(data[pid]['age'])==int:
            #     if int(data[pid]['age'])<55 and int(data[pid]['age'])>18:
            #         data[pid]['age']='18_54'
            #     elif (int(data[pid]['age'])>=55 and int(data[pid]['age'])<65):
            #             data[pid]['age']='55_64'
            #     elif (int(data[pid]['age'])>=65 and int(data[pid]['age'])<75):
            #             data[pid]['age']='65_74'
            #     elif int(data[pid]['age'])>=75:
            #         data[pid]['age']="75+"
            if data[pid]['race'] == 'White':
                pass
            elif data[pid]['race'] == 'Black/African American':
                pass
            else:
                data[pid]['race'] = 'Other'
            # if data[pid]['marry']=='Married':
            #     data[pid]['marry']='Married'
            #     print 'marry'
            # elif data[pid]['marry']=='':
            #     data[pid]['marry']=''
            #     print 'Na'
            # else:
            #     data[pid]['marry']='NotMarried'
            #     print 'not'

            if data[pid]['location'] == 'Baden Office':
                data[pid]['location'] = 'Beaver'
            elif data[pid]['location'] == 'Cecil':
                data[pid]['location'] = 'Washington'
            elif data[pid]['location'] == 'Chippewa':
                data[pid]['location'] = 'Beaver'
            elif data[pid]['location'] == 'Hopewell Office':
                data[pid]['location'] = 'Bedford'
            elif data[pid]['location'] == 'McMURRAY Office':
                data[pid]['location'] = 'Washington'
            elif data[pid]['location'] == 'Southpointe':
                data[pid]['location'] = 'Washington'
            elif data[pid]['location'] == 'StClair Office':
                data[pid]['location'] = 'Allegheny'
            elif data[pid]['location'] == 'Washington Office':
                data[pid]['location'] = 'Washington'
            elif data[pid]['location'] == 'Waynesburg Office':
                data[pid]['location'] = 'Greene'

            for date in data[pid]['appt']:
                data[pid]['appt'][date]['stage'] = ''
                if data[pid]['appt'][date]['type'] == 'PTEDU':
                    data[pid]['appt'][date]['type'] = 'E'
                if data[pid]['appt'][date]['type'] == 'EXFU':
                    data[pid]['appt'][date]['type'] = 'O'
                if data[pid]['appt'][date]['type'] == 'BIOP':
                    data[pid]['appt'][date]['type'] = 'O'
                if data[pid]['appt'][date]['type'] == 'NEW':
                    data[pid]['appt'][date]['type'] = 'O'
                if data[pid]['appt'][date]['type'] == 'FUP':
                    data[pid]['appt'][date]['type'] = 'O'
                if data[pid]['appt'][date]['type'] == 'B':
                    data[pid]['appt'][date]['type'] = 'H'
                if data[pid]['appt'][date]['type'] == 'HOSP':
                    data[pid]['appt'][date]['type'] = 'H'
                if data[pid]['appt'][date]['type'] == 'ESRD':
                    data[pid]['appt'][date]['type'] = 'E'

                for i in range(len(data[pid]['appt'][date]['proc'])):
                    if data[pid]['appt'][date]['proc'][i] == 76775:
                        data[pid]['appt'][date]['proc'][i] = 'Ultrasound'
                    elif data[pid]['appt'][date]['proc'][i] == 93975:
                        data[pid]['appt'][date]['proc'][i] = 'Doppler'

                for d in range(0, len(data[pid]['appt'][date]['diag'])):
                    if data[pid]['appt'][date]['diag'][d] != '':
                        if (data[pid]['appt'][date]['diag'][d][0:1] == 'E' or data[pid]['appt'][date]['diag'][d][
                                                                              0:1] == 'e'):
                            data[pid]['appt'][date]['diag'][d] = 'Other'
                        elif (data[pid]['appt'][date]['diag'][d][0:1] == 'V' or data[pid]['appt'][date]['diag'][d][
                                                                                0:1] == 'v'):
                            # data[pid]['appt'][date]['diag'][d]='Transplant'
                            data[pid]['appt'][date]['diag'][d] = 'Other'
                        # elif (int(float(data[pid]['appt'][date]['diag'][d]))==401 or int(float(data[pid]['appt'][date]['diag'][d]))==405):
                        #     data[pid]['appt'][date]['diag'][d]='HP'
                        # elif (int(float(data[pid]['appt'][date]['diag'][d]))==250):
                        #     data[pid]['appt'][date]['diag'][d]='DM'
                        # elif int(float(data[pid]['appt'][date]['diag'][d])) == 584:
                        #     data[pid]['appt'][date]['diag'][d] = 'AKI'
                        # SEE LINE 215
                        elif (data[pid]['appt'][date]['diag'][d] == '585.1'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD1'
                        elif (data[pid]['appt'][date]['diag'][d] == '585.2'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD2'
                        elif (data[pid]['appt'][date]['diag'][d] == '585.3'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD3'
                        elif (data[pid]['appt'][date]['diag'][d] == '585.4'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD4'
                        elif (data[pid]['appt'][date]['diag'][d] == '585.5'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD5'
                        elif (data[pid]['appt'][date]['diag'][d] == '585.6'):
                            data[pid]['appt'][date]['diag'][d] = 'CKD6'
                        # elif data[pid]['appt'][date]['diag'][d] == '276.2':
                        #     data[pid]['appt'][date]['diag'][d] = 'Acidosis'
                        # elif data[pid]['appt'][date]['diag'][d] == '782.3':
                        #     data[pid]['appt'][date]['diag'][d] = 'Edema'
                        # elif (data[pid]['appt'][date]['diag'][d] == '276.5'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Volume Depletion'
                        # elif (data[pid]['appt'][date]['diag'][d] == '276.8'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Hypokalemia'
                        # elif (data[pid]['appt'][date]['diag'][d] == '458.9'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Hypotension'
                        # elif (data[pid]['appt'][date]['diag'][d] == '599.6'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Urinary Obstruction'
                        # elif (data[pid]['appt'][date]['diag'][d] == '728.88'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Rhabdomyolysis'
                        # elif (data[pid]['appt'][date]['diag'][d] == '584.5'):
                        #     data[pid]['appt'][date]['diag'][d] = 'ATN'
                        # elif (int(float(data[pid]['appt'][date]['diag'][d])) == 580 or int(
                        #         float(data[pid]['appt'][date]['diag'][d])) == 582):
                        #     data[pid]['appt'][date]['diag'][d] = 'Glomerulonephritis'
                        # elif data[pid]['appt'][date]['diag'][d] == '276.7':
                        #     data[pid]['appt'][date]['diag'][d] = 'Hyperkalemia'
                        # elif (int(float(data[pid]['appt'][date]['diag'][d])) >= 280 and int(
                        #         float(data[pid]['appt'][date]['diag'][d])) <= 285):
                        #     data[pid]['appt'][date]['diag'][d] = 'Anemia'
                        # elif (data[pid]['appt'][date]['diag'][d] == '79*1.0' or data[pid]['appt'][date]['diag'][
                        #     d] == '791'):
                        #     data[pid]['appt'][date]['diag'][d] = 'Proteinuria'
                        # elif (int(float(data[pid]['appt'][date]['diag'][d])) == 252 or int(
                        #         float(data[pid]['appt'][date]['diag'][d])) == 588):
                        #     data[pid]['appt'][date]['diag'][d] = 'Hyperparathyroidism'
                        # elif data[pid]['appt'][date]['diag'][d] == '275.3':
                        #     data[pid]['appt'][date]['diag'][d] = 'Hyperphosphatemia'
                        else:
                            data[pid]['appt'][date]['diag'][d] = 'Other'

                try:
                    data[pid]['appt'][date]['diag'] = list(set(data[pid]['appt'][date]['diag']))
                    data[pid]['appt'][date]['diag'].remove('Other')

                except Exception as e:
                    pass

            for date in data[pid]['lab']:
                try:
                    if ('Hemoglobin' in data[pid]['lab'][date] and data[pid]['lab'][date][
                        'Hemoglobin'] != 'Not Done' and data[pid]['lab'][date]['Hemoglobin'] != ''):
                        if float(data[pid]['lab'][date]['Hemoglobin']) < 13 and float(
                                data[pid]['lab'][date]['Hemoglobin']) > 0 and data[pid]['sex'] == 'Male':
                            data[pid]['lab'][date]['Hemoglobin'] = 'caution'
                        elif float(data[pid]['lab'][date]['Hemoglobin']) >= 13 and data[pid]['sex'] == 'Male':
                            data[pid]['lab'][date]['Hemoglobin'] = 'normal'
                        elif float(data[pid]['lab'][date]['Hemoglobin']) < 12 and float(
                                data[pid]['lab'][date]['Hemoglobin']) > 0 and data[pid]['sex'] == 'Female':
                            data[pid]['lab'][date]['Hemoglobin'] = 'caution'
                        elif float(data[pid]['lab'][date]['Hemoglobin']) > 12 and data[pid]['sex'] == 'Female':
                            data[pid]['lab'][date]['Hemoglobin'] = 'normal'
                        else:
                            data[pid]['lab'][date]['Hemoglobin'] = 'n/a'
                    else:
                        pass
                except:
                    pass

                try:
                    if ('Calcium' in data[pid]['lab'][date] and data[pid]['lab'][date]['Calcium'] != ''):
                        if (float(data[pid]['lab'][date]['Calcium']) < 8.4 and float(
                                data[pid]['lab'][date]['Calcium']) > 0):
                            data[pid]['lab'][date]['Calcium'] = 'low'
                        elif (float(data[pid]['lab'][date]['Calcium']) <= 9.5 and float(
                                data[pid]['lab'][date]['Calcium']) >= 8.4):
                            data[pid]['lab'][date]['Calcium'] = 'normal'
                        elif float(data[pid]['lab'][date]['Calcium']) > 9.5:
                            data[pid]['lab'][date]['Calcium'] = 'high'
                        else:
                            data[pid]['lab'][date]['Calcium'] = 'n/a'
                    else:
                        pass
                except:
                    pass

                try:
                    if ('Albumin' in data[pid]['lab'][date] and data[pid]['lab'][date]['Albumin'] != ''):
                        if (float(data[pid]['lab'][date]['Albumin']) < 4 and float(
                                data[pid]['lab'][date]['Albumin']) > 0):
                            data[pid]['lab'][date]['Albumin'] = 'caution'

                        elif float(data[pid]['lab'][date]['Albumin']) >= 4:
                            data[pid]['lab'][date]['Albumin'] = 'normal'
                        else:
                            data[pid]['lab'][date]['Albumin'] = 'n/a'
                    else:
                        data[pid]['lab'][date]['Albumin'] = 'n/a'
                except:
                    pass
                try:
                    if ('Phosphorus' in data[pid]['lab'][date] and data[pid]['lab'][date]['Phosphorus'] != '') and (
                                    'CKD5' not in data[pid]['appt'][date]['diag'] and 'CKD6' not in
                                data[pid]['appt'][date][
                                    'diag']):
                        if (float(data[pid]['lab'][date]['Phosphorus']) < 2.7 and float(
                                data[pid]['lab'][date]['Phosphorus']) > 0):
                            data[pid]['lab'][date]['Phosphorus'] = 'low'
                        elif float(data[pid]['lab'][date]['Phosphorus']) >= 2.7 and float(
                                data[pid]['lab'][date]['Phosphorus']) <= 4.6:
                            data[pid]['lab'][date]['Phosphorus'] = 'normal'
                        elif float(data[pid]['lab'][date]['Phosphorus']) > 4.6:
                            data[pid]['lab'][date]['Phosphorus'] = 'high'
                        else:
                            data[pid]['lab'][date]['Phosphorus'] = 'n/a'
                    elif ('Phosphorus' in data[pid]['lab'][date] and data[pid]['lab'][date]['Phosphorus'] != '') and (
                            'CKD5' in data[pid]['appt'][date][
                            'diag'] or 'CKD6' in data[pid]['appt'][date]['diag']):
                        if (float(data[pid]['lab'][date]['Phosphorus']) < 3.5 and float(
                                data[pid]['lab'][date]['Phosphorus']) > 0):
                            data[pid]['lab'][date]['Phosphorus'] = 'low'
                        elif float(data[pid]['lab'][date]['Phosphorus']) >= 3.5 and float(
                                data[pid]['lab'][date]['Phosphorus']) <= 5.5:
                            data[pid]['lab'][date]['Phosphorus'] = 'normal'
                        elif float(data[pid]['lab'][date]['Phosphorus']) > 5.5:
                            data[pid]['lab'][date]['Phosphorus'] = 'high'
                        else:
                            data[pid]['lab'][date]['Phosphorus'] = 'n/a'

                except:
                    pass
                # try:
                #     if ('Potassium' in data[pid]['lab'][date] and data[pid]['lab'][date]['Potassium'] != ''):
                #         if (float(data[pid]['lab'][date]['Potassium']) < 3.5 and float(
                #                 data[pid]['lab'][date]['Potassium']) > 0):
                #             data[pid]['lab'][date]['Potassium'] = 'low'
                #         elif (float(data[pid]['lab'][date]['Potassium']) <= 5.0 and float(
                #                 data[pid]['lab'][date]['Potassium']) >= 3.5):
                #             data[pid]['lab'][date]['Potassium'] = 'normal'
                #         elif float(data[pid]['lab'][date]['Potassium']) > 5.0:
                #             data[pid]['lab'][date]['Potassium'] = 'high'
                #         else:
                #             data[pid]['lab'][date]['Potassium'] = 'n/a'
                #     else:
                #         pass
                # except:
                #     pass
                try:
                    if ('Carbon Dio' in data[pid]['lab'][date] and data[pid]['lab'][date]['Carbon Dio'] != ''):
                        if (float(data[pid]['lab'][date]['Carbon Dio']) < 22 and float(
                                data[pid]['lab'][date]['Carbon Dio']) > 0):
                            data[pid]['lab'][date]['Carbon Dio'] = 'low'
                        elif float(data[pid]['lab'][date]['Carbon Dio']) >= 22:
                            data[pid]['lab'][date]['Carbon Dio'] = 'normal'
                        else:
                            data[pid]['lab'][date]['Carbon Dio'] = 'n/a'
                    else:
                        pass
                except:
                    pass

                try:
                    if ('Creatinine' in data[pid]['lab'][date] and data[pid]['lab'][date]['Creatinine'] != '' and
                                data[pid]['lab'][date]['Creatinine'] > 0):
                        if data[pid]['sex'] == 'Male':
                            if float(data[pid]['lab'][date]['Creatinine']) < 0.5:
                                data[pid]['lab'][date]['Creatinine'] = 'low'
                            elif (float(data[pid]['lab'][date]['Creatinine']) <= 1.5 and float(
                                    data[pid]['lab'][date]['Creatinine']) >= 0.5):
                                data[pid]['lab'][date]['Creatinine'] = 'normal'
                            elif (float(data[pid]['lab'][date]['Creatinine']) > 1.5):
                                data[pid]['lab'][date]['Creatinine'] = 'high'
                            else:
                                data[pid]['lab'][date]['Creatinine'] = 'n/a'
                        elif data[pid]['sex'] == 'Female':
                            if float(data[pid]['lab'][date]['Creatinine']) < 0.6:
                                data[pid]['lab'][date]['Creatinine'] = 'low'
                            elif (float(data[pid]['lab'][date]['Creatinine']) <= 1.2 and float(
                                    data[pid]['lab'][date]['Creatinine']) >= 0.6):
                                data[pid]['lab'][date]['Creatinine'] = 'normal'
                            elif (float(data[pid]['lab'][date]['Creatinine']) > 1.2):
                                data[pid]['lab'][date]['Creatinine'] = 'high'
                            else:
                                data[pid]['lab'][date]['Creatinine'] = 'n/a'
                    else:
                        pass
                except:
                    pass

                try:
                    if ('GFR' in data[pid]['lab'][date] and data[pid]['lab'][date]['GFR'] != ''):
                        if (float(data[pid]['lab'][date]['GFR']) < 15 and float(data[pid]['lab'][date]['GFR']) > 0):
                            for i in range(1, 7):
                                if 'CKD%s' % i not in data[pid]['appt'][date]['diag']:
                                    data[pid]['appt'][date]['diag'].append('CKD5')
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i == 5:
                                    break
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i != 5:
                                    data[pid]['appt'][date]['diag'].remove('CKD%s' % i)
                                    data[pid]['appt'][date]['diag'].append('CKD5')

                        elif (float(data[pid]['lab'][date]['GFR']) < 30 and float(data[pid]['lab'][date]['GFR']) >= 15):
                            for i in range(1, 7):
                                if 'CKD%s' % i not in data[pid]['appt'][date]['diag']:
                                    data[pid]['appt'][date]['diag'].append('CKD4')
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i == 4:
                                    break
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i != 4:
                                    data[pid]['appt'][date]['diag'].remove('CKD%s' % i)
                                    data[pid]['appt'][date]['diag'].append('CKD4')

                        elif (float(data[pid]['lab'][date]['GFR']) < 60 and float(data[pid]['lab'][date]['GFR']) >= 30):
                            for i in range(1, 7):
                                if 'CKD%s' % i not in data[pid]['appt'][date]['diag']:
                                    data[pid]['appt'][date]['diag'].append('CKD3')
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i == 3:
                                    break
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i != 3:
                                    data[pid]['appt'][date]['diag'].remove('CKD%s' % i)
                                    data[pid]['appt'][date]['diag'].append('CKD3')

                        elif (float(data[pid]['lab'][date]['GFR']) < 90 and float(data[pid]['lab'][date]['GFR']) >= 60):
                            for i in range(1, 7):
                                if 'CKD%s' % i not in data[pid]['appt'][date]['diag']:
                                    data[pid]['appt'][date]['diag'].append('CKD2')
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i == 2:
                                    break
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i != 2:
                                    data[pid]['appt'][date]['diag'].remove('CKD%s' % i)
                                    data[pid]['appt'][date]['diag'].append('CKD2')

                        elif float(data[pid]['lab'][date]['GFR']) >= 90:
                            for i in range(1, 7):
                                if 'CKD%s' % i not in data[pid]['appt'][date]['diag']:
                                    data[pid]['appt'][date]['diag'].append('CKD1')
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i == 1:
                                    break
                                elif 'CKD%s' % i in data[pid]['appt'][date]['diag'] and i != 1:
                                    data[pid]['appt'][date]['diag'].remove('CKD%s' % i)
                                    data[pid]['appt'][date]['diag'].append('CKD1')
                        else:
                            data[pid]['lab'][date]['GFR'] = 'n/a'
                    else:
                        pass
                except Exception as e:
                    pass

        # for date in range(0, len(data['12037']['appt'])):
        #     print "cleandata", date, data['12037']['appt'][date]['drug']

        return data

    def attachGFR(self, data):
        for pid in data:
            c_age = float(data[pid]['age'])
            for date in data[pid]['lab']:

                try:
                    yeardiff = 2014 - datetime.datetime.strptime(data[pid]['appt'][date]['actualdate'], '%Y-%m-%d').year
                    age = c_age - yeardiff
                    if ((data[pid]['lab'][date]['GFR'] == 0 or data[pid]['lab'][date]['GFR'] == '') and
                                data[pid]['appt'][date]['bodywt'] > 0):
                        if data[pid]['sex'] == 'Male':
                            wtinkg = float(data[pid]['appt'][date]['bodywt']) * 0.453592
                            cr = float(data[pid]['lab'][date]['Creatinine'])
                            eGFR = ((140 - age) * wtinkg) / (72 * cr)
                        elif data[pid]['sex'] == 'Female':
                            wtinkg = float(data[pid]['appt'][date]['bodywt']) * 0.453592
                            cr = float(data[pid]['lab'][date]['Creatinine'])
                            eGFR = ((140 - age) * wtinkg * 0.85) / (72 * cr)
                        else:
                            eGFR = 0
                        data[pid]['lab'][date]['GFR'] = eGFR
                except:
                    pass
        return data

    def attachHPDM(self, data):
        for pid in data:
            hp = False
            for date in data[pid]['appt']:
                if 'HP' in data[pid]['appt'][date]['diag']:
                    hp = True
                    break
            if hp == True:
                for i in data[pid]['appt']:
                    if 'HP' not in data[pid]['appt'][i]['diag']:
                        data[pid]['appt'][i]['diag'].append('HP')
            else:
                pass

        for pid in data:
            dm = False
            for date in data[pid]['appt']:
                if 'DM' in data[pid]['appt'][date]['diag']:
                    dm = True
                    break
            if dm == True:
                for i in data[pid]['appt']:
                    if 'DM' not in data[pid]['appt'][i]['diag']:
                        data[pid]['appt'][i]['diag'].append('DM')
            else:
                pass

        return data

    def attachCKD(self, data):

        for pid in data:
            for date in sorted(data[pid]['appt'].iterkeys()):
                data[pid]['appt'][date]['diag'] = list(set(data[pid]['appt'][date]['diag']))
                if data[pid]['appt'][date]['type'] != 'H':
                    if ('CKD1' in data[pid]['appt'][date]['diag'] and 'CKD2' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD1' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                            elif 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD1')
                        except:
                            pass
                    if ('CKD1' in data[pid]['appt'][date]['diag'] and 'CKD3' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD1' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD3')
                            elif 'CKD3' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD1')
                        except:
                            pass
                    if ('CKD1' in data[pid]['appt'][date]['diag'] and 'CKD4' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD1' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD4')
                            elif 'CKD4' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD1')
                        except:
                            pass
                    if ('CKD1' in data[pid]['appt'][date]['diag'] and 'CKD5' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD1' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD5')
                            elif 'CKD5' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD1')
                        except:
                            pass
                    if ('CKD2' in data[pid]['appt'][date]['diag'] and 'CKD3' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD3' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                            elif 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD3')
                        except:
                            pass
                    if ('CKD2' in data[pid]['appt'][date]['diag'] and 'CKD4' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD4')
                            elif 'CKD4' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                        except:
                            pass
                    if ('CKD2' in data[pid]['appt'][date]['diag'] and 'CKD5' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD5' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                            elif 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD5')
                        except:
                            pass
                    if ('CKD2' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                            elif 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                        except:
                            pass
                    if ('CKD3' in data[pid]['appt'][date]['diag'] and 'CKD4' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD3' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD4')
                            elif 'CKD4' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD3')
                        except:
                            pass
                    if ('CKD3' in data[pid]['appt'][date]['diag'] and 'CKD5' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD3' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD5')
                            elif 'CKD5' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD3')
                        except:
                            pass
                    if ('CKD4' in data[pid]['appt'][date]['diag'] and 'CKD5' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD4' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD5')
                            elif 'CKD5' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD4')
                        except:
                            pass
                    if ('CKD1' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD1' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                            elif 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD1')
                        except:
                            pass
                    if ('CKD2' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD2' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                            elif 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD2')
                        except:
                            pass
                    if ('CKD3' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD3' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                            elif 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD3')
                        except:
                            pass
                    if ('CKD4' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD4' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                            elif 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD4')
                        except:
                            pass
                    if ('CKD5' in data[pid]['appt'][date]['diag'] and 'CKD6' in data[pid]['appt'][date]['diag']):
                        try:
                            if 'CKD5' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD6')
                            elif 'CKD6' in data[pid]['appt'][date + 1]['diag']:
                                data[pid]['appt'][date]['diag'].remove('CKD5')
                        except:
                            pass

        for date in range(0, len(data['12037']['appt'])):
            print "testprint", date, data['12037']['appt'][date]['type'], data['12037']['appt'][date]['diag']

        return data

    def sortData(self, data):

        for pid in data:
            for j in data[pid]['appt'].iterkeys():
                data[pid]['appt'][j]['proc'] = sorted(data[pid]['appt'][j]['proc'])
                data[pid]['appt'][j]['diag'] = sorted(data[pid]['appt'][j]['diag'])
                data[pid]['appt'][j]['drugclass'] = sorted(data[pid]['appt'][j]['drugclass'])

        # for date in range(0, len(data['12037']['appt'])):
        #     print "final", date, data['12037']['appt'][date]['type'], data['12037']['appt'][date]['diag']
        #     print "final", date, data['12037']['appt'][date]['proc'], data['12037']['appt'][date]['drug']

        with open(
                "/Users/yiyezhang/Dropbox/python_projects/ckdplatform_current/data/thesis/postDefense/data_processed.json",
                'w') as outfile:
            json.dump(data, outfile)

    def attachDrug(self, data):
        # for date in range(0, len(data['12037']['appt'])):
        #     for i in range(len(data['12037']['appt'][date]['drug'])):
        #         print "initial", date, data['12037']['appt'][date]['drug'][i]['class']

        p = 0
        for pid in data:
            for date in range(0, len(data[pid]['appt'])):
                for dr in range(len(data[pid]['appt'][date]['drug'])):
                    if str(data[pid]['appt'][date]['drug'][dr]['class']).find('ntibiotics') == -1:
                        if data[pid]['appt'][date]['drug'][dr]['type'] == 'P:' or data[pid]['appt'][date]['drug'][dr][
                            'type'] == 'R:':

                            drugname = data[pid]['appt'][date]['drug'][dr]['name']
                            flag2 = True
                            for d in range(int(date) + 1, len(data[pid]['appt'])):
                                if len(data[pid]['appt'][d]['drug']) == 0:
                                    drug = {}
                                    drug['name'] = data[pid]['appt'][date]['drug'][dr]['name']
                                    drug['class'] = data[pid]['appt'][date]['drug'][dr]['class']
                                    drug['type'] = 'A:'
                                    data[pid]['appt'][d]['drug'].append(drug)

                                elif len(data[pid]['appt'][d]['drug']) > 0:
                                    for dr2 in range(len(data[pid]['appt'][d]['drug'])):
                                        if drugname in data[pid]['appt'][d]['drug'][dr2].itervalues() and \
                                                        data[pid]['appt'][d]['drug'][dr2]['type'] == 'D:':
                                            flag2 = False
                                            break

                                        elif drugname in data[pid]['appt'][d]['drug'][dr2].itervalues() and \
                                                        data[pid]['appt'][d]['drug'][dr2]['type'] != 'D:':
                                            pass
                                        elif drugname not in data[pid]['appt'][d]['drug'][dr2].itervalues():
                                            drug = {}
                                            drug['name'] = data[pid]['appt'][date]['drug'][dr]['name']
                                            drug['class'] = data[pid]['appt'][date]['drug'][dr]['class']
                                            drug['type'] = 'A:'
                                            data[pid]['appt'][d]['drug'].append(drug)
                                            break
                                        else:
                                            print "This is not happening."
                                            pass
                                if flag2 == False:
                                    break

            p = p + 1

        # for date in range(0, len(data['12037']['appt'])):
        #     for i in range(len(data['12037']['appt'][date]['drug'])):
        #         print "final", date, i, data['12037']['appt'][date]['drug'][i]['class'], \
        #             data['12037']['appt'][date]['drug'][i]['type']

        # for pid in data:
        #  
        #     for date in range(0,len(data[pid]['appt'])):
        #         for dr in range(len(data[pid]['appt'][date]['drug'])):

        #             if data[pid]['appt'][date]['drug'][dr]['type']=='D:':
        #                 drugname=data[pid]['appt'][date]['drug'][dr]['name']
        #                 dt=False
        #                 for d in range(int(date)-1,-1,-1):
        #                     print d,'d',date,'date'
        #                     if len(data[pid]['appt'][d]['drug'])>0:
        #                         for dr2 in range(len(data[pid]['appt'][d]['drug'])):
        #                             if drugname in data[pid]['appt'][d]['drug'][dr2].itervalues() and (data[pid]['appt'][d]['drug'][dr2]['type']=='P:' or data[pid]['appt'][d]['drug'][dr2]['type']=='R:'):
        #                                 print 'D'
        #                                 dt=True
        #                                 break

        #                             elif drugname not in data[pid]['appt'][d]['drug'][dr2].itervalues() :
        #                                 drug={}
        #                                 drug['name']=data[pid]['appt'][date]['drug'][dr]['name']
        #                                 drug['class']=data[pid]['appt'][date]['drug'][dr]['class']
        #                                 drug['type']=data[pid]['appt'][date]['drug'][dr]['type']
        #                                 data[pid]['appt'][d]['drug'].append(drug)
        #                             else:
        #                                 pass
        #                     elif len(data[pid]['appt'][d]['drug'])==0:
        #                         drug={}
        #                         drug['name']=data[pid]['appt'][date]['drug'][dr]['name']
        #                         drug['class']=data[pid]['appt'][date]['drug'][dr]['class']
        #                         drug['type']=data[pid]['appt'][date]['drug'][dr]['type']
        #                         data[pid]['appt'][d]['drug'].append(drug) 

        #                 if dt:
        #                     break

        return data

    def getDrugClass(self, data):
        for pid in data:
            for date in data[pid]['appt']:
                data[pid]['appt'][date]['drugclass'] = list()
        for pid in data:
            for date in data[pid]['appt']:
                for dr in data[pid]['appt'][date]['drug']:
                    data[pid]['appt'][date]['drugclass'].append(dr['class'])
                data[pid]['appt'][date]['drugclass'] = list(set(data[pid]['appt'][date]['drugclass']))

                for i in range(len(data[pid]['appt'][date]['drugclass'])):
                    if data[pid]['appt'][date]['drugclass'][i] == 'Loop diuretics':
                        data[pid]['appt'][date]['drugclass'][i] = 'DR'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Thiazide diuretics':
                        data[pid]['appt'][date]['drugclass'][i] = 'DR'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Potassium-sparing diuretics':
                        data[pid]['appt'][date]['drugclass'][i] = 'DR'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Angiotensin converting enzyme inhibitors':
                        data[pid]['appt'][date]['drugclass'][i] = 'ACE'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Angiotensin II inhibitors':
                        data[pid]['appt'][date]['drugclass'][i] = 'ARB'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                        # elif data[pid]['appt'][date]['drugclass'][i]=='Calcium channel blocking agents':
                        #     data[pid]['appt'][date]['drugclass'][i]='AH'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                        # elif data[pid]['appt'][date]['drugclass'][i]=='Antihypertensive combinations':
                        #     data[pid]['appt'][date]['drugclass'][i]='AH'
                        # data[pid]['appt'][date]['drugclass'][i]='Other'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Statins':
                        data[pid]['appt'][date]['drugclass'][i] = 'ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Topical steroids with anti-infectives':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Nonsteroidal anti-inflammatory agents':
                    #     data[pid]['appt'][date]['drugclass'][i]='NSAID'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Ophthalmic steroids':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Topical steroids':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Inhaled corticosteroids':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Androgens and anabolic steroids':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Nasal steroids':
                    #     data[pid]['appt'][date]['drugclass'][i]='ST'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Topical antibiotics':
                    #     data[pid]['appt'][date]['drugclass'][i]='AB'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Miscellaneous antibiotics':
                    #     data[pid]['appt'][date]['drugclass'][i]='AB'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Glycopeptide antibiotics':
                    #     data[pid]['appt'][date]['drugclass'][i]='AB'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Antibiotics/antineoplastics':
                    #     data[pid]['appt'][date]['drugclass'][i]='AB'
                    elif data[pid]['appt'][date]['drugclass'][i] == 'Proton pump inhibitors':
                        data[pid]['appt'][date]['drugclass'][i] = 'PPI'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Glucocorticoids':
                    #     data[pid]['appt'][date]['drugclass'][i]='GC'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Platelet aggregation inhibitors':
                    #     data[pid]['appt'][date]['drugclass'][i]='PAI'
                    # elif data[pid]['appt'][date]['drugclass'][i]=='Salicylates':
                    #     data[pid]['appt'][date]['drugclass'][i]='SL'
                    else:
                        data[pid]['appt'][date]['drugclass'][i] = 'Other'

        for pid in data:
            for date in data[pid]['appt']:
                data[pid]['appt'][date]['drugclass'] = list(set(data[pid]['appt'][date]['drugclass']))
                try:
                    data[pid]['appt'][date]['drugclass'].remove('Other')

                except:
                    pass
        return data


def main():
    d = DataProcess()
    d1 = d.attachHOSP()
    d2 = d.timeLine(d1)
    d3 = d.attachGFR(d2)
    d4 = d.cleanData(d3)
    d5 = d.attachHPDM(d4)
    d6 = d.attachCKD(d5)
    data = d.attachDrug(d6)
    data2 = d.CreateObs(data)
    d.ObsList(data2)
    data3 = d.getDrugClass(data2)
    d.sortData(data3)


def testfun():
    org = ['a', 'b']
    target = ['c', 'a', 'd', 'b']


if __name__ == '__main__':
    main()
