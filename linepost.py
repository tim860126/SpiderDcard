from __future__ import unicode_literals
import pandas as pd
import requests
import re
import os
import dateutil.parser
import datetime
import numpy as np
import matplotlib
from matplotlib.font_manager import *
import matplotlib.pyplot as plt
import time
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import LineBotApiError
import configparser
import random
actkeyword=['社團','志工','學生會','活動中心','獎學金','營隊','議會','畢聯會','畢業典禮','活二','活一','課指組']
livekeyword=['生輔組','宿舍','女二宿','民生宿舍','屏商宿舍','抽宿舍','學雜費減免','就學貸款','住宿','服務學習','遺失','不見','蕙蘭','復旦','樓長']
savekeyword=['肺炎','健康檢查','抽菸','戒菸','健康','健檢','學餐','健康中心']
solderkeyword=['兵單','兵役','打架','毒品','國防','車禍','停車場','車棚','軍訓','安全','小偷','偷竊','抽菸','校安中心']
genderkeyword=['性騷擾','性平','同性','憂鬱','性別平等','自殘','自殺','割腕','出櫃','gay','輔導','諮商']
matplotlib.matplotlib_fname()
deaddate=7
datecontent=[]
datenum=[]
likecontent=[]
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
livelist=[]
actlist=[]
savelist=[]
solderlist=[]
genderlist=[]
keywordtemp=[]
senti=[]
now=time.strftime("%Y-%m-%d", time.localtime()) 
filename=str(now)+".html"
folderpath="C:/xampp/htdocs/"
fhtml = open("C:/xampp/htdocs/"+filename, "w" ,encoding = 'utf-8')
fhtml.write("<!doctype html><html><head><meta http-equiv='Content-Type' content='text/html; charset=UTF-8' /><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'></head><link rel='stylesheet' type='text/css' href='custom.css' /><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css' integrity='sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh' crossorigin='anonymous'><body><center><div class='container custom-container-width'>")
def Crawl(ID):
    link = 'https://www.dcard.tw/_api/posts/' + str(ID)
    requ = requests.get(link)
    rejs = requ.json()
    month=int(rejs['createdAt'][5:7])
    day=rejs['createdAt'][8:10]
    checkday=0
    for i in range(len(datecontent)):
        if datecontent[i] == day:
            checkday=1
            datenum[i]=datenum[i]+1
            print(day+':文章數量'+str(datenum[i]))
            if int(likecontent[i])<int(rejs['likeCount']):
                likecontent[i]=rejs['likeCount']
    if month == deaddate:
        print('符合月份')
        if checkday==0:
            datecontent.append(day)
            datenum.append(1)
            likecontent.append(rejs['likeCount'])
        # for i in range(len(rejs['media'])):
            # print(rejs['media'][i]['url'])
            # r=requests.get(rejs['media'][i]['url'])
            # with open('C:/Users/shengkai/Documents/dcard爬蟲/img/'+str(i)+str(ID)+'.png','wb') as f:
                # f.write(r.content)
        month=rejs['createdAt'][5:7]
        month=int(month)
       
        return(pd.DataFrame(
            data=
            [{'ID':rejs['id'],
              '標題':rejs['title'],
              '內文':rejs['content'],
              #'excerpt':rejs['excerpt'],
              'createdAt':rejs['createdAt'],
              #'updatedAt':rejs['updatedAt'],
              '回應次數':rejs['commentCount'],
              #'forumName':rejs['forumName'],
              #'forumAlias':rejs['forumAlias'],
              '性別':rejs['gender'],
              '點讚數':rejs['likeCount'],
              '回應數':rejs['reactions'],
              #'topics':rejs['topics'],
               '關鍵字':keywordtemp,
               '情感分析':senti}],
              #'media':rejs['media']}],
              #columns=['ID','title','content','excerpt','createdAt','updatedAt','commentCount','forumName','forumAlias','gender','likeCount','reactions','topics','media']
              columns=['ID','標題','內文','回應次數','性別','點讚數','關鍵字','createdAt','情感分析']
            ))
    else:
        print('不符合月份:'+rejs['createdAt'])
def getList(keyword,df,name):
    temp=[]
    keywordcontent=[]
    tempcontent=[]
    keywordnum=[]
    gf = pd.DataFrame()
    getkeyword=0
    checkkeyword=0
    tempcheckkeyword=0
    for i in range(len(df)):
        tempcontent=[]
        text=df.at[i,'內文']
        title=df.at[i,'標題']
        
        for j in range(len(keyword)):
            if text.find(keyword[j]) !=-1 or title.find(keyword[j]) !=-1:
                temp.append(i)
                getkeyword=1
                for k in range(len(keywordcontent)):
                    if keywordcontent[k] == keyword[j]:
                        checkkeyword=1
                        keywordnum[k]=keywordnum[k]+1
                for k in range(len(tempcontent)):
                    if tempcontent[k] == keyword[j]:
                        tempcheckkeyword=1   
                if checkkeyword==0:
                    tempcontent.append(keyword[j])
                    keywordcontent.append(keyword[j])
                    keywordnum.append(1)
                if tempcheckkeyword==0:
                    tempcontent.append(keyword[j])
                tempcheckkeyword=0
                checkkeyword=0
        if getkeyword==1:
            gg=pd.DataFrame(
                        data=
                        [{'ID':df.at[i,'ID'],
                          '標題':df.at[i,'標題'],
                          '內文':df.at[i,'內文'],
                          'createdAt':df.at[i,'createdAt'],
                          '回應次數':df.at[i,'回應次數'],
                          '性別':df.at[i,'性別'],
                          '點讚數':df.at[i,'點讚數'],
                          '關鍵字':tempcontent,
                          '情感分析':df.at[i,'情感分析']}],
                          columns=['ID','標題','內文','回應次數','性別','點讚數','關鍵字','createdAt','情感分析']
                        )
            gf = gf.append(gg,ignore_index=True)
            gf.to_excel('./'+str(deaddate)+'/'+name+'.xlsx')
        getkeyword=0
    if len(keywordnum)>0:        
        fig = plt.figure()
        plt.xticks(range(len(keywordcontent)),keywordcontent, rotation=45)
        plt.ylim(0,max(keywordnum)+3)
        plt.ylabel(u'關鍵字出現次數')
        plt.xlabel(u'關鍵字')
        plt.title("關鍵字出現統計")
        plt.bar(range(len(keywordnum)),keywordnum)
        #plt.show()
        plt.tight_layout()
        plt.savefig(folderpath+str(now)+str(name)+'.jpg', dpi=400)
    return temp
            

url = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=100'
#url2 = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=10'
resq = requests.get(url)
rejs = resq.json()
df = pd.DataFrame()
for i in range(len(rejs)):
        kk=Crawl(rejs[i]['id'])
        df = df.append(kk,ignore_index=True)
for j in range(1):
    last = str(int(df.tail(1).ID)) 
    url = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=100&before=' + last
    resq = requests.get(url)
    rejs = resq.json()
    for i in range(len(rejs)):
        kk=Crawl(rejs[i]['id'])
        df = df.append(kk,ignore_index=True)
print(df.shape)
df

print(datenum)
print(datecontent)
datenum.reverse()
datecontent.reverse()
fig = plt.figure()
plt.xticks(range(len(datecontent)),datecontent, rotation=45)
plt.ylim(1,max(datenum)+3)
plt.ylabel(u'發文數量')
plt.xlabel(u'發文日期')
plt.title("發文日期趨勢圖")
plt.plot(range(len(datecontent)),datenum,'-',color='b')
plt.plot(range(len(datecontent)),datenum,'.',color='r')
#plt.show()
plt.tight_layout()
plt.savefig('postnum', dpi=300)

fig = plt.figure()
plt.xticks(range(len(datecontent)),datecontent, rotation=45)
plt.ylim(1,max(likecontent)+3)
plt.ylabel(u'愛心數量')
plt.xlabel(u'發文日期')
plt.title("愛心最多發文日期")
plt.plot(range(len(datecontent)),likecontent,'-',color='b')
plt.plot(range(len(datecontent)),likecontent,'.',color='r')
#plt.show()
plt.tight_layout()
plt.savefig('like.png', dpi=300)

# frame=df.sort_values('likeCount',ascending=False).index
# for i in range(3):
    # print(df.at[frame[i],'likeCount'])

frame=df.sort_values('回應次數',ascending=False).index

for i in range(3):
    print(df.at[frame[i],'回應次數'])
    
dfgenF=len(df[df['性別']=='F'])
dfgenM=len(df[df['性別']=='M'])
dfgender=[dfgenF,dfgenM]
genderlabel=['女生','男生']
gendercolor=['#ff0000', '#5b00ae']
fig = plt.figure()
plt.pie(dfgender,labels=genderlabel,colors=gendercolor,autopct = "%0.2f%%",center = (0,0))
plt.legend(loc = "best")
plt.title("發文男女比例")
#plt.show()
plt.savefig('gender.png', dpi=300)
def printlist(df):
    print(len(df))
    for i in range(len(df)):
        print(df.at[i,'標題'])
def printlimit(dfname,limit,limitname):
    if os.path.isfile("./"+str(deaddate)+"/"+dfname+".xlsx"):
        fhtml.write("<h1>"+dfname+"</h1>")
        fhtml.write("<div class='container table-responsive'><table class='table table-bordered table-active' width=800 height=200 border=1><tr><thead class='thead-dark'><th>標題</th><th>回應次數</th><th>網頁連結</th></thead></tr>")
        f2 = open("./"+str(deaddate)+"/"+dfname+".txt", "w" ,encoding = 'utf-8')
        gf=pd.read_excel("./"+str(deaddate)+"/"+dfname+".xlsx")
        printlist(gf)
        index=gf.sort_values(limitname,ascending=False).index
        if len(index):
            print(index)
            if len(index)<limit:
                limit=len(index)
            for i in range(limit):
                if int(gf.at[index[i],'回應次數'])>5:
                    fhtml.write("<tr><td>"+str(gf.at[index[i],'標題'])+"</td><td>回應次數:"+str(gf.at[index[i],'回應次數'])+"</td><td><a href='https://www.dcard.tw/f/nptu/p/"+str(str(gf.at[index[i],'ID']))+"'>點我</a></td></tr>")
                    
                    print(gf.at[index[i],'標題'])
                    f2.write(str(gf.at[index[i],'標題']))
                    f2.write("\n")
                    
                    print(gf.at[index[i],limitname])
                    f2.write(str(gf.at[index[i],limitname]))
                    f2.write("\n")
                    
                    print(gf.at[index[i],'ID'])
                    f2.write(str(gf.at[index[i],'ID']))
                    f2.write("\n")     
            fhtml.write("</table>")
            if os.path.isfile(folderpath+str(now)+dfname+".jpg"):
                fhtml.write("<img src='"+str(now)+dfname+".jpg' class='img-fluid' alt='Responsive image'>")
            fhtml.write("</div>")
        else:
            print('空值')
        

livelist=getList(livekeyword,df,'生活輔導組')

actlist=getList(actkeyword,df,'學生活動發展組')

savelist=getList(savekeyword,df,'衛生保健組')

solderlist=getList(solderkeyword,df,'軍訓暨校安中心')

genderlist=getList(genderkeyword,df,'學生諮商中心')

printlimit('生活輔導組',3,'回應次數')

printlimit('學生活動發展組',3,'回應次數')

printlimit('衛生保健組',3,'回應次數')

printlimit('軍訓暨校安中心',3,'回應次數')

printlimit('學生諮商中心',3,'回應次數')

fhtml.write("</div></center></body><script src='https://code.jquery.com/jquery-3.4.1.slim.min.js' integrity='sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n' crossorigin='anonymous'></script><script src='https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js' integrity='sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo' crossorigin='anonymous'></script><script src='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js' integrity='sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6' crossorigin='anonymous></script></html>")
fhtml.close
df.to_excel('./'+str(deaddate)+'/'+'活動.xlsx')

app = Flask(__name__)
htmlurl ='https://8400df67a06c.ngrok.io/'

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()

config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))

handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

to="Ue98936edb078d121bad2755ae2e11589"

# try:
    # line_bot_api.push_message(to, TextSendMessage(text='最新資訊'+htmlurl+filename))
# except LineBotApiError as e:
    # # error handle
    # raise e
