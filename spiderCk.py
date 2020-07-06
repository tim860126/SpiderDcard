from ckiptagger import WS, POS, NER
from snownlp import SnowNLP
import pandas as pd
import requests
import re
import os
import numpy as np
import matplotlib
from matplotlib.font_manager import *
import matplotlib.pyplot as plt

matplotlib.matplotlib_fname()

keyword=['抽菸','宿舍','社團','活動','同性','同志','通識','性騷擾','警衛','停車','教官','學生會','老師','遺失','換課','選課','女二宿','共A','共B','共C','共D','共E','車棚']
ws = WS("C:/Users/shengkai/Documents/dcard爬蟲/data")
pos = POS("C:/Users/shengkai/Documents/dcard爬蟲/data")
ner = NER("C:/Users/shengkai/Documents/dcard爬蟲/data")
f2 = open("篩選後.html", "w" ,encoding = 'utf-8')
f3 = open("篩選前.html", "w" ,encoding = 'utf-8')
f2.write("<!doctype html><html><head><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'></head><link rel='stylesheet' type='text/css' href='custom.css' /><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css' integrity='sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh' crossorigin='anonymous'><body><center><div class='container table-responsive'><table class='table table-bordered table-active' width=800 height=200 border=1><tr><thead class='thead-dark'><th>標題</th><th>關鍵字</th><th>情感分析</th><th>原文網址</th><th>文章日期</th></thead></tr>")
f3.write("<!doctype html><html><head><meta name='viewport' content='width=device-width, initial-scale=1, shrink-to-fit=no'></head><link rel='stylesheet' type='text/css' href='custom.css' /><link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css' integrity='sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh' crossorigin='anonymous'><body><center><div class='container table-responsive'><table class='table table-bordered table-active' width=800 height=200 border=1><tr><thead class='thead-dark'><th>標題</th><th>關鍵字</th><th>情感分析</th><th>原文網址</th><th>文章日期</th></thead></tr>")
deaddate=6
datecontent=[]
datenum=[]
keywordcontent=[]
keywordnum=[]
likecontent=[]
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
def Crawl(ID):
    keywordtemp=[]
    getkeyword=0
    link = 'https://www.dcard.tw/_api/posts/' + str(ID)
    requ = requests.get(link)
    rejs = requ.json()
    month=int(rejs['createdAt'][5:7])
    day=rejs['createdAt'][8:10]
    checkday=0
    checkkeyword=0
    #日期收集與文章數量計算
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
        #取得文章內圖片網址並下載
        if len(rejs['media']) >0:
            os.makedirs('C:/Users/shengkai/Documents/dcard爬蟲/img/'+str(rejs['id']),exist_ok=True)
        for i in range(len(rejs['media'])):
            #print(rejs['media'][i]['url'])
            r=requests.get(rejs['media'][i]['url'])
            with open('C:/Users/shengkai/Documents/dcard爬蟲/img/'+str(rejs['id'])+'/'+str(i)+'.png','wb') as f:
                f.write(r.content)
        #處理文章內容-去除圖片網址與換行        
        text=rejs['content']
        title=rejs['title']
       
        results = re.compile(r'[http|https]*://[a-zA-Z0-9.?/&=:%-]*', re.S)
        text = re.sub(results, '',text)
        results = re.compile(r'\n', re.S)
        text = re.sub(results, '',text)
        #全文關鍵字檢索
        f3.write("<tr><td>"+str(title)+"</td>")
        f3.write("<td>")
        for i in range(len(keyword)):
            if text.find(keyword[i]) !=-1 or title.find(keyword[i]) !=-1:
                getkeyword=1
                #計算找到關鍵字的數量
                for j in range(len(keywordcontent)):
                    if keywordcontent[j] == keyword[i]:
                        checkkeyword=1
                        keywordnum[j]=keywordnum[j]+1
                if checkkeyword==0:
                    keywordcontent.append(keyword[i])   
                    keywordnum.append(1)
                checkkeyword=0        
                f3.write(str(keyword[i])+" ")
        f3.write("</td>")        
        if getkeyword==1:
            f2.write("<tr><td>"+str(title)+"</td>")
            f2.write("<td>")
            for i in range(len(keyword)):
                if text.find(keyword[i]) !=-1 or title.find(keyword[i]) !=-1:
                    getkeyword=1
                    keywordtemp.append(keyword[i])
                    f2.write(str(keyword[i])+" ")
                    print('關鍵字:'+keyword[i])
            f2.write("</td>")
        #ckip斷詞
        ws_results = ws([text])
        pos_results = pos(ws_results)
        ner_results = ner(ws_results, pos_results)
        print(ws_results)
        print(pos_results)
          
        f = open("./"+str(rejs['id'])+".txt", "w" ,encoding = 'utf-8')

        s = SnowNLP(text)

        s_senti = s.sentiments

        print('此篇情感分數')
        print(s_senti)
        f.write("此篇情感分數\n")
        f.write(str(s_senti)+"\n")

        if getkeyword==1:
            f2.write("<td>")
            if s_senti >= 0.6:
                #f2.write("此篇分析為正面"+str(s_senti))
                f2.write("此篇分析為正面")
            elif s_senti <= 0.6:
                #f2.write("此篇分析為負面"+str(s_senti))
                f2.write("此篇分析為負面")
            f2.write("</td>")
            f2.write("<td><a href='https://www.dcard.tw/f/nptu/p/"+str(ID)+"'>點我</a></td><td>"+str(month)+"-"+day+"</td></tr>")
            
        f3.write("<td>")    
        if s_senti >= 0.6:
            #f3.write("此篇分析為正面"+str(s_senti))
            f3.write("此篇分析為正面")
        elif s_senti <= 0.6:
            #f3.write("此篇分析為負面"+str(s_senti))
            f3.write("此篇分析為負面")
        f3.write("</td>")
        f3.write("<td><a href='https://www.dcard.tw/f/nptu/p/"+str(ID)+"'>點我</a></td><td>"+str(month)+"-"+day+"</td></tr>")  
        x=0
        x2=0
        f.write("文章內容:")
        for i in range(len(ws_results[0])):
            f.write(ws_results[0][i])
        f.write("\n")
        for i in range(len(ws_results[0])):
            s = SnowNLP(ws_results[0][i])
            f.write("分詞"+str(i+1)+":"+ws_results[0][i]+"\n")
            s_token = s.words
            print(s_token)
            #for j in range(len(s_token[i])-1):
                #f.write(s_token[i][j]+"\n")
            s_senti = s.sentiments
            print(s_senti)
            f.write(str(s_senti)+"\n")
            if s.sentiments > 0.5:
                x=x+1
                f.write("積極\n")
                print ('積極')
            elif s.sentiments <= 0.5:
                x2=x2+1
                f.write("消極\n")
                print ('消極')
            f.write("-------------------\n")
        f.write(str(x)+"\n")
        f.write(str(x2)+"\n")
        f.close()
        print('積極:',x)
        print('消極:',x2)
        #print(text)
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
              #'reactions':rejs['reactions'],
              #'topics':rejs['topics'],
               '關鍵字':keywordtemp,}],
              #'media':rejs['media']}],
              #columns=['ID','title','content','excerpt','createdAt','updatedAt','commentCount','forumName','forumAlias','gender','likeCount','reactions','topics','media']
              columns=['ID','標題','內文','回應次數','性別','點讚數','關鍵字','createdAt']
            ))
    else:
        print('不符合月份:'+rejs['createdAt'])
url = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=50'
#url2 = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=10'
resq = requests.get(url)
rejs = resq.json()
df = pd.DataFrame()
for i in range(len(rejs)):
        kk=Crawl(rejs[i]['id'])
        df = df.append(kk,ignore_index=True)
# for j in range(5):
    # last = str(int(df.tail(1).ID)) 
    # url = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=100&before=' + last
    # resq = requests.get(url)
    # rejs = resq.json()
    # for i in range(len(rejs)):
        # kk=Crawl(rejs[i]['id'])
        # df = df.append(kk,ignore_index=True)
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
plt.plot(range(len(datecontent)),datenum,'-',color='b')
plt.plot(range(len(datecontent)),datenum,'.',color='r')
#plt.show()
plt.tight_layout()
plt.savefig('postnum', dpi=400)

fig = plt.figure()
plt.xticks(range(len(datecontent)),datecontent, rotation=45)
plt.ylim(1,max(likecontent)+3)
plt.ylabel(u'愛心數量')
plt.xlabel(u'發文日期')
plt.plot(range(len(datecontent)),likecontent,'-',color='b')
plt.plot(range(len(datecontent)),likecontent,'.',color='r')
#plt.show()
plt.tight_layout()
plt.savefig('like.png', dpi=400)

fig = plt.figure()
plt.xticks(range(len(keywordcontent)),keywordcontent, rotation=45)
plt.ylim(0,max(keywordnum)+3)
plt.ylabel(u'關鍵字出現次數')
plt.xlabel(u'關鍵字')
plt.bar(range(len(keywordnum)),keywordnum)
#plt.show()
plt.tight_layout()
plt.savefig('keyword.png', dpi=400)


f2.write("</table></div><div class='container custom-container-width'><img src='like.png' class='img-fluid' alt='Responsive image'><img src='postnum.png' class='img-fluid' alt='Responsive image'><img src='keyword.png' class='img-fluid' alt='Responsive image'></div>")
f2.write("</center></body><script src='https://code.jquery.com/jquery-3.4.1.slim.min.js' integrity='sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n' crossorigin='anonymous'></script><script src='https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js' integrity='sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo' crossorigin='anonymous'></script><script src='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js' integrity='sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6' crossorigin='anonymous></script></html>")
f2.close
f3.write("</table></div><div class='container custom-container-width'><img src='like.png' class='img-fluid' alt='Responsive image'><img src='postnum.png' class='img-fluid' alt='Responsive image'><img src='keyword.png' class='img-fluid' alt='Responsive image'></div>")
f3.write("</center></body><script src='https://code.jquery.com/jquery-3.4.1.slim.min.js' integrity='sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n' crossorigin='anonymous'></script><script src='https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js' integrity='sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo' crossorigin='anonymous'></script><script src='https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js' integrity='sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6' crossorigin='anonymous></script></html>")
f3.close
df.to_excel('C:/Users/shengkai/Documents/dcard爬蟲/熱門.xlsx')
print(keywordcontent)
print(keywordnum)