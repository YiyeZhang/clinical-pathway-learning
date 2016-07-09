__author__ = "Yiye Zhang"
from flask import render_template,flash,redirect,request
from app import app
from forms import FormOne, FormThree
import os,thread
#import MySQLdb as mdb
import sys,getopt,os,tempfile,itertools
from app.logic.Sequence import Sequence
from app.logic.printNodedesc2 import PrintVVNode
from app.logic.getData import Data
from app.logic.printData import printData
from app.logic.printNodedesc import PrintNode
from gexf import Gexf
import json

@app.route('/new')
def new_index():
  
  return render_template("index_new.html")

@app.route('/submit',methods=['POST'])
def submit():
    res = json.loads(request.form['user_input_total'])
    age = res['age']
    gender = res['gender']
    weight = res['weight']
    Diag=list()
    Diaglist=list()
    for i in range(len(res['visits_info'])):
      Diaglist=list()
      for j in range(len(res['visits_info'][i]['diagnosis'])):
        Diaglist.append(res['visits_info'][i]["diagnosis"][j]['name'])
      Diag.append(Diaglist)
    print Diag
    GFR=list()
    for i in range(len(res['visits_info'])):
      try:
        GFR.append(res['visits_info'][i]["GFR"]['name'])
      except:
        GFR.append("")
    print "GFR:", GFR
    Hemo=list()
    for i in range(len(res['visits_info'])):
      try:
        Hemo.append(res['visits_info'][i]["Hemo"]['name'])
      except:
        Hemo.append("")
    print "Hemo:", Hemo
    Alb=list()
    for i in range(len(res['visits_info'])):
      try:
        Alb.append(res['visits_info'][i]["Albumin"]['name'])
      except:
        Alb.append("")
    Creat=list()
    print "Alb",Alb
    for i in range(len(res['visits_info'])):
      try:
        Creat.append(res['visits_info'][i]["Crt"]['name'])
      except:
        Creat.append("")
    print "Creat",Creat
    Pho=list()
    for i in range(len(res['visits_info'])):
      try:
        Pho.append(res['visits_info'][i]["Pho"]['name'])
      except:
        Pho.append("")
    print "Pho:", Pho
    Cal=list()
    for i in range(len(res['visits_info'])):
      try:
        Cal.append(res['visits_info'][i]["Cal"]['name'])
      except:
        Cal.append("")
    print "Cal:", Cal
    CO2=list()
    for i in range(len(res['visits_info'])):
      try:
        CO2.append(res['visits_info'][i]["CO2"]['name'])
      except:
        CO2.append("")
    print "CO2:", CO2
    Pot=list()
    for i in range(len(res['visits_info'])):
      try:
        Pot.append(res['visits_info'][i]["Pot"]['name'])
      except:
        Pot.append("")
    print "Pot:", Pot

    c=Data()
    data=c.getData()
    p=printData()
    #p.printOut(data)

    nummatchpt=c.matchpt(data)

    s=Sequence()
    nodes=s.getNodes(data)
    VT, tempDT,OT=s.getSeq(nodes)
    visitpair,DT=s.addTime(VT,tempDT)
    results_list,pairoutput,VVT=s.getTrans(visitpair,VT,DT)

    # print 'source','target','weight','count','scount','tcount'
    # for i in range(len(results_list)):
    #   print results_list[i]['source'],results_list[i]['target'],results_list[i]['weight'],results_list[i]['count'],results_list[i]['count_source'],results_list[i]['count_target']

    return render_template('result_old.html', results_list=results_list,nummatchpt=nummatchpt)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/step1')
def step1():
  return render_template('step1.html')

# @app.route('/step2', methods = ['GET', 'POST'])
# def result():
#   # weight=request.form['prob']
#   print "xxx:",request.form
#   gender=request.form['gender']
#   age=int(request.form['age'])
#   weight=int(request.form['weight'])
  
#   bpdia_para=list()
#   if request.form.has_key('DBP0') and request.form['DBP0']!='':
#     bpdia_para.append(request.form['DBP0'])
#   if request.form.has_key('DBP1') and request.form['DBP1']!='':
#     bpdia_para.append(request.form['DBP1'])

#   bpsys_para=list()
#   if request.form.has_key('SBP0') and request.form['SBP0']!='':
#     bpsys_para.append(request.form['SBP0'])
#   if request.form.has_key('SBP1') and request.form['SBP1']!='':
#     bpsys_para.append(request.form['SBP1'])

#   optim_para=list()
#   if request.form.has_key('diaglist0') and request.form['diaglist0']!='':
#     optim_para.append(request.form['diaglist0'].split(","))
#   if request.form.has_key('diaglist1') and request.form['diaglist1']!='':
#     optim_para.append(request.form['diaglist1'].split(","))
#   if request.form.has_key('diaglist2') and request.form['diaglist2']!='':
#     optim_para.append(request.form['diaglist2'].split(","))
#   if request.form.has_key('diaglist3') and request.form['diaglist3']!='':
#     optim_para.append(request.form['diaglist3'].split(","))
  
#   gfr_para=list()
#   if request.form.has_key('GFR0') and request.form['GFR0']!='':
#     gfr_para.append(request.form['GFR0'])
#   if request.form.has_key('GFR1') and request.form['GFR1']!='':
#     gfr_para.append(request.form['GFR1'])
  
#   hemo_para=list()
#   if request.form.has_key('hemo0') and request.form['hemo0']!='':
#     hemo_para.append(request.form['hemo0'])
#   if request.form.has_key('hemo1') and request.form['hemo1']!='':
#     hemo_para.append(request.form['hemo1'])

#   cal_para=list()
#   if request.form.has_key('cal0') and request.form['cal0']!='':
#     cal_para.append(request.form['cal0'])
#   if request.form.has_key('cal1') and request.form['cal1']!='':
#     cal_para.append(request.form['cal1'])

#   alb_para=list()
#   if request.form.has_key('alb0') and request.form['alb0']!='':
#     alb_para.append(request.form['alb0'])
#   if request.form.has_key('alb1') and request.form['alb1']!='':
#     gfr_para.append(request.form['alb1'])

#   pho_para=list()
#   if request.form.has_key('pho0') and request.form['pho0']!='':
#     pho_para.append(request.form['pho0'])
#   if request.form.has_key('pho1') and request.form['pho1']!='':
#     pho_para.append(request.form['pho1'])

#   CO2_para=list()
#   if request.form.has_key('CO20') and request.form['CO20']!='':
#     CO2_para.append(request.form['CO20'])
#   if request.form.has_key('CO21') and request.form['CO21']!='':
#     CO2_para.append(request.form['CO21'])

#   ACR_para=list()
#   if request.form.has_key('ACR0') and request.form['ACR0']!='':
#     ACR_para.append(request.form['ACR0'])
#   if request.form.has_key('ACR1') and request.form['ACR1']!='':
#     ACR_para.append(request.form['ACR1'])

#   bpdia_para, bpdia_para, bpsys_para, optim_para, gfr_para, hemo_para,cal_para,alb_para,pho_para,CO2_para, ACR_para = test.preptest1()

#   print "after override"
#   print bpdia_para
#   print bpsys_para
#   print optim_para
#   print gfr_para
#   print hemo_para
#   print cal_para
#   print alb_para
#   print pho_para
#   print CO2_para
#   print ACR_para
  
#   c=DataProcess()
#   data=c.getData(gender,age,bpsys_para,bpdia_para,optim_para,gfr_para,hemo_para,cal_para,alb_para, pho_para,CO2_para,ACR_para)
#   nummatchpt=c.matchpt(data)
#   results_list = c.getSeq(data)
#   # for i in range(len(results_list)):
#   #   print results_list[i]
#   return render_template('result.html', results_list=results_list,nummatchpt=nummatchpt)

@app.route('/nodedesc')
def nodedesc():
  c=PrintNode()
  nodedesclist=c.desc()
  return render_template('nodedesc.html',nodedesclist=nodedesclist)

@app.route('/VVdesc')
def VVdesc():
  c=PrintVVNode()
  VVdesclist=c.desc()
  return render_template('VVdesc.html',VVdesclist=VVdesclist)

@app.route('/graph')
def graph():
    fh = open ('data/data_out2.json','r')
    data = json.load(fh)
    nodelist = set()
    for d in data:
        nodelist.add(d['source'])
        nodelist.add(d['target'])


    gexf = Gexf("Yiye Zhang","Test graph")
    graph=gexf.addGraph("directed", "static","testing graph")

    for i in nodelist:
        graph.addNode(i,i)

    k=0
    for d in data:
        graph.addEdge(k,d['source'],d['target'], weight=d['weight'])
        k=k+1

    output_file=open("app/static/g.gexf","w")
    gexf.write(output_file)


    return render_template('graph.html')


  

