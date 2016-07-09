class printData:
    def printOut(self,ET):
        # for pid in ET:
        #     if ET[pid]['age'] <50:
        #         age=0
        #     elif ET[pid]['age'] <70:
        #         age=1
        #     elif ET[pid]['age']>=70:
        #         age=2
        #     if ET[pid]['race']=='White':
        #         race='White'
        #     elif ET[pid]['race']=='Black/African American':
        #         race='Black'
        #     else:
        #         race='Other'
        #     if ET[pid]['sex']=='Female':
        #         sex=0
        #     else:
        #         sex=1

        #     print pid,sex,age

        # for pid in ET:
        #     flag=False
        #     for date in ET[pid]['appt']:
        #         if 'AKI' in ET[pid]['appt'][date]['diag']:
        #             flag=True
        #             break
        #     if flag==True:
        #         print pid

        # avgdiff = []
        # for pid in ET:
        #     diff = (
        #     datetime.datetime.strptime(ET[pid]['appt'][1]['actualdate'], '%Y-%m-%d') - datetime.datetime.strptime(
        #         ET[pid]['appt'][0]['actualdate'], '%Y-%m-%d')).days
        #     diff1 = diff = (
        #     datetime.datetime.strptime(ET[pid]['appt'][2]['actualdate'], '%Y-%m-%d') - datetime.datetime.strptime(
        #         ET[pid]['appt'][1]['actualdate'], '%Y-%m-%d')).days
        #     diff2 = diff = (
        #     datetime.datetime.strptime(ET[pid]['appt'][3]['actualdate'], '%Y-%m-%d') - datetime.datetime.strptime(
        #         ET[pid]['appt'][2]['actualdate'], '%Y-%m-%d')).days
        #     avgdiff.append(diff)
        #     avgdiff.append(diff1)
        #     avgdiff.append(diff2)
        #
        # print "average time gap", numpy.std(avgdiff)

        for pid in ET:
            for date in ET[pid]['appt']:

                ET[pid]['appt'][date]['A'] = {}
                ET[pid]['appt'][date]['AKI'] = {}
                ET[pid]['appt'][date]['W'] = {}
                ET[pid]['appt'][date]['Acidosis'] = {}
                ET[pid]['appt'][date]['D'] = {}
                ET[pid]['appt'][date]['P'] = {}
                ET[pid]['appt'][date]['S'] = {}
                # if 'TDR' in ET[pid]['appt'][date]['drugclass'] and 'PDR' in ET[pid]['appt'][date]['drugclass'] and 'LDR' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['A']=1
                # elif 'PDR' in ET[pid]['appt'][date]['drugclass'] and 'LDR' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['A']=2
                # elif 'PDR' in ET[pid]['appt'][date]['drugclass'] and 'TDR' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['A']=3
                # elif 'TDR' in ET[pid]['appt'][date]['drugclass'] and 'LDR' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['A']=4
                # elif 'TDR' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['A']=5
                # if ('ACE' in ET[pid]['appt'][date]['drugclass'] or 'ARB' in ET[pid]['appt'][date]['drugclass']) and 'DR' in ET[pid]['appt'][date]['drugclass'] and 'ST' in ET[pid]['appt'][date]['drugclass']:
                # if ('ACE' in ET[pid]['appt'][date]['drugclass'] and 'ARB' in ET[pid]['appt'][date]['drugclass']):
                #     ET[pid]['appt'][date]['A']=1
                # else:
                #     ET[pid]['appt'][date]['A']=0
                # if 'PPI' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['P']=1
                # else:
                #     ET[pid]['appt'][date]['P']=0
                if 'PPI' in ET[pid]['appt'][date]['drugclass']:
                    ET[pid]['appt'][date]['D'] = 1
                else:
                    ET[pid]['appt'][date]['D'] = 0
                # if 'ST' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['S']=1
                # else:
                #     ET[pid]['appt'][date]['S']=0
                # if 'AH' in ET[pid]['appt'][date]['drugclass'] or 'ARB' in ET[pid]['appt'][date]['drugclass']:
                #     ET[pid]['appt'][date]['W']=1
                # else:
                #     ET[pid]['appt'][date]['W']=0
                if 'AKI' in ET[pid]['appt'][date]['diag'] or ET[pid]['appt'][date]['type'] == 'H':
                    ET[pid]['appt'][date]['AKI'] = 1
                else:
                    ET[pid]['appt'][date]['AKI'] = 0
                    # if 'Acidosis' in ET[pid]['appt'][date]['diag']:
                    #     ET[pid]['appt'][date]['Acidosis']=1
                    # else:
                    #     ET[pid]['appt'][date]['Acidosis']=2

                    # print ET[pid]['appt'][date]['drugclass']
        l0 = []
        l1 = []
        l2 = []
        l3 = []
        a0 = []
        a1 = []
        a2 = []
        a3 = []
        stage4l = []
        stage8l = []
        for pid in ET:
            if ET[pid]['age'] < 50:
                age = 0
            elif ET[pid]['age'] < 70:
                age = 1
            elif ET[pid]['age'] >= 70:
                age = 2
            if ET[pid]['race'] == 'White':
                race = 0  # white
            elif ET[pid]['race'] == 'Black/African American':
                race = 1  # black
            else:
                race = 2  # other
            if ET[pid]['sex'] == 'Female':
                sex = 0
            else:
                sex = 1
            # stage8=''
            # chronic=''
            # if ET[pid]['lab'][8].get('GFR')<15 and ET[pid]['lab'][8].get('GFR')>0:
            #     stage8='5'
            #     worsen8=1
            # elif ET[pid]['lab'][8].get('GFR')<30 and ET[pid]['lab'][8].get('GFR')>=15:
            #     stage8='4'
            #     worsen8=1
            # elif ET[pid]['lab'][8].get('GFR')<45 and ET[pid]['lab'][8].get('GFR')>=30:
            #     stage8='1'  #3B
            #     worsen8=0
            # elif ET[pid]['lab'][8].get('GFR')<60 and ET[pid]['lab'][8].get('GFR')>=45:
            #     stage8='3'  #3A
            #     worsen8=0
            # elif ET[pid]['lab'][8].get('GFR')<90 and ET[pid]['lab'][8].get('GFR')>=60:
            #     stage8='2'
            #     worsen8=0
            # elif ET[pid]['lab'][8].get('GFR')>=90:
            #     stage8='2'
            #     worsen8=0
            # else:
            #     worsen8=0
            #     stage8='2'

            # if 'HP' in ET[pid]['appt'][1]['diag'] and 'DM' in ET[pid]['appt'][1]['diag']:
            #     chronic=1 #hpdm
            # if 'HP' in ET[pid]['appt'][1]['diag'] and 'DM' not in ET[pid]['appt'][1]['diag']:
            #     chronic ='HP'
            if 'DM' in ET[pid]['appt'][1]['diag']:
                dm = 1
            else:
                dm = 0

            stage4 = ''
            worsen = ''
            if ET[pid]['lab'][4].get('GFR') < 15 and ET[pid]['lab'][4].get('GFR') > 0:
                stage4 = '5'
                worsen = 1
            elif ET[pid]['lab'][4].get('GFR') < 30 and ET[pid]['lab'][4].get('GFR') >= 15:
                stage4 = '4'
                worsen = 1
            elif ET[pid]['lab'][4].get('GFR') < 45 and ET[pid]['lab'][4].get('GFR') >= 30:
                stage4 = '1'  # 3B
                worsen = 1
            elif ET[pid]['lab'][4].get('GFR') < 60 and ET[pid]['lab'][4].get('GFR') >= 45:
                stage4 = '3'  # 3A
                worsen = 1
            elif ET[pid]['lab'][4].get('GFR') <= 90 and ET[pid]['lab'][4].get('GFR') >= 60:
                stage4 = '2'
                worsen = 0
            elif ET[pid]['lab'][4].get('GFR') > 90:
                stage4 = '1'
                worsen = 0
            else:
                stage4 = '2'
                worsen = 0

            # stage12=''

            if ET[pid]['lab'][0].get('GFR') < 15 and ET[pid]['lab'][0].get('GFR') > 0:
                stage = '5'
                worsen12 = 1
            elif ET[pid]['lab'][0].get('GFR') < 30 and ET[pid]['lab'][0].get('GFR') >= 15:
                stage = '4'
                worsen12 = 1
            elif ET[pid]['lab'][0].get('GFR') < 45 and ET[pid]['lab'][0].get('GFR') >= 30:
                stage = '1'  # 3B
                worsen12 = 0
            elif ET[pid]['lab'][0].get('GFR') < 60 and ET[pid]['lab'][0].get('GFR') >= 45:
                stage = '3'  # 3A
                worsen12 = 0
            elif ET[pid]['lab'][0].get('GFR') < 90 and ET[pid]['lab'][0].get('GFR') >= 60:
                stage = '2'
                worsen12 = 0
            elif ET[pid]['lab'][0].get('GFR') >= 90:
                stage = '2'
                worsen12 = 0
            else:
                worsen12 = 0
                stage = '2'

            print pid, stage, sex, age, race, dm, ET[pid]['marry'], ET[pid]['location'], ET[pid]['lab'][4].get('GFR'), \
            ET[pid]['appt'][0]['AKI'], ET[pid]['appt'][0]['D'], ET[pid]['appt'][1]['AKI'], ET[pid]['appt'][1]['D'], \
            ET[pid]['appt'][2]['AKI'], ET[pid]['appt'][2]['D'], ET[pid]['appt'][3]['AKI'], ET[pid]['appt'][3]['D']
            # stage4, worsen,ET[pid]['appt'][0]['P'],ET[pid]['appt'][1]['P'],ET[pid]['appt'][2]['P'],ET[pid]['appt'][3]['P'],ET[pid]['appt'][0]['D'],ET[pid]['appt'][1]['D'],ET[pid]['appt'][2]['D'],ET[pid]['appt'][3]['D'],ET[pid]['appt'][0]['S'],ET[pid]['appt'][1]['S'],ET[pid]['appt'][2]['S'],ET[pid]['appt'][3]['S']
            # testset
            # print pid,ET[pid]['lab'][8].get('GFR'),ET[pid]['appt'][4]['AKI'],ET[pid]['appt'][4]['D'],ET[pid]['appt'][5]['AKI'],ET[pid]['appt'][5]['D'],ET[pid]['appt'][6]['AKI'],ET[pid]['appt'][6]['D'],ET[pid]['appt'][7]['AKI'],ET[pid]['appt'][7]['D']
            # stage8,worsen, ,ET[pid]['appt'][4]['P'],ET[pid]['appt'][5]['P'],ET[pid]['appt'][6]['P'],ET[pid]['appt'][7]['P'],ET[pid]['appt'][4]['D'],ET[pid]['appt'][5]['D'],ET[pid]['appt'][6]['D'],ET[pid]['appt'][7]['D'],ET[pid]['appt'][4]['S'],ET[pid]['appt'][5]['S'],ET[pid]['appt'][6]['S'],ET[pid]['appt'][7]['S']

            # print pid,stage8, stage12,ET[pid]['lab'][12].get('GFR'),ET[pid]['appt'][8]['AKI'],ET[pid]['appt'][8]['D'],ET[pid]['appt'][9]['AKI'],ET[pid]['appt'][9]['D'],ET[pid]['appt'][10]['AKI'],ET[pid]['appt'][10]['D'],ET[pid]['appt'][11]['AKI'],ET[pid]['appt'][11]['D']

        return
