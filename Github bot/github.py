from flask import Flask, request
import json
import csv
import datetime
from dateutil.tz import gettz
from threading import Thread
import pandas as pd

app = Flask('')

@app.route('/',methods=['POST'])
def commit_event():
  data = json.loads(request.data)
  mode='w'

  try:
    df = pd.read_csv('update.csv')
    dt = df.iloc[0,2].split(' ')[0].split('/')
    tdt = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
    if str(tdt.day) == dt[0] and str(tdt.month) == dt[1] and str(tdt.year) == dt[2]:
      mode = 'a'
    else:
      mode = 'w'
  except:
    pass

  print(data['repository']['full_name'])
  print(data['head_commit']['message'])
  print(data['head_commit']['timestamp'])
  print(data['head_commit']['author']['name'])
  print(data['head_commit']['author']['username'])
  print(data['head_commit']['added'])
  print(data['head_commit']['modified'])

  with open('update.csv', mode=mode) as update_repo:
    update_writer = csv.writer(update_repo, delimiter=',')
    t = datetime.datetime.now(tz=gettz('Asia/Kolkata'))
    if mode=='w':
      update_writer.writerow(['Repo Url','Message','Datetime','Commiter Name','Commiter Username','Added Files','Updated Files'])
    update_writer.writerow([data['repository']['full_name'],data['head_commit']['message'],str(t.day)+'/'+str(t.month)+'/'+str(t.year)+" "+str(t.hour)+':'+str(t.minute)+':'+str(t.second),data['head_commit']['author']['name'],data['head_commit']['author']['username'],data['head_commit']['added'],data['head_commit']['modified']])

  return 'OK'

def run():
  app.run(host='0.0.0.0',port=8080)

def git():
  t = Thread(target=run)
  t.start()