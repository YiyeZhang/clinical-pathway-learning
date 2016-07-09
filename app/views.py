__author__ = "Yiye Zhang"
from flask import render_template,flash,redirect,request
from app import app
from forms import FormOne, FormThree
import os,thread
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
    path = res['path']
    numvisit = int(res['numvisit'])
    
    c=Data()
    data=c.getData(path,numvisit)
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

# @app.route('/')
# def index():
#   return render_template('index.html')


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


  

