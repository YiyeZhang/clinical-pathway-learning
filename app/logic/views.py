from flask import render_template,flash,redirect,request
from app import app
from forms import FormOne, FormThree
import os,thread
#import MySQLdb as mdb
import sys,getopt,os,tempfile,itertools
from numpy import *
from app.logic.Sequence import Sequence
from app.logic.printNodedesc2 import PrintVVNode
from app.logic.getData import Data
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
    # c.getStats(data)
    # data=c.Match(gender,age,Diag,GFR,Hemo,Pho,Alb,Cal,CO2,Creat,Pot)
    nummatchpt=c.matchpt(data)
    s=Sequence()
    # results_list,VT,GT,HT,PT,AT,CT,CO,CR,KT,TR,VVT = s.getSeq(data)
    # results_list,VT,TR,VVT = s.getSeq(data)
    results_list,VT,TR = s.getSeq(data)
    # print 'source','target','weight','count','scount','tcount'
    # for i in range(len(results_list)):
    #   print results_list[i]['source'],results_list[i]['target'],results_list[i]['weight'],results_list[i]['count'],results_list[i]['count_source'],results_list[i]['count_target']
    # f=Seq()
    # f.findSeq(results_list)
    # h=HMM()
    # states_d,start_prob,tr_prob,em_prob=h.prepareSeq(VT,GT,HT,PT,AT,CT,CO,CR,TR)
    # states_d,start_prob,tr_prob,em_prob=h.prepareSeq(VVT,GT,HT,PT,AT,CT,CO,CR,KT)
    # v=Viterbi()
    # obs=list()
    # obs.append('hohohoho')
    # obs.append('30be4.3.')
    # obs.append('30be4.3.')
    # obs.append('30be4.3.')
    # obs.append('30n/4.ab')
    # obs.append('30n/4.ab')
    
    # try:
    #   prob,path=v.viterbi(states_d,obs,start_prob,tr_prob,em_prob)
    # except KeyError as ke:
    #   print "no matching observations", ke
  
    # f=FB()
    # fb=f.fwd_bkw(obs,states_d,start_prob,tr_prob,em_prob,end_state)
    # for line in fb:
    #   print(' '.join(map(str, line)))
    # states_d_array,start_prob_array,tr_prob_array,em_prob_array=makeArray(states_d,start_prob,tr_prob,em_prob)
    
    # hmm = HMM2()
    # hmm.pi = start_prob_array
    # hmm.A = tr_prob_array
    # hmm.B = em_prob_array
    
    # observations,states = hmm.simulate(10)

    return render_template('result.html', results_list=results_list,nummatchpt=nummatchpt)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/step1')
def step1():
  return render_template('step1.html')

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
    fh = open ('data/jamia/data_out2.json','r')
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


  

