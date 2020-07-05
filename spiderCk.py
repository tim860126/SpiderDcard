from ckiptagger import WS, POS, NER
from snownlp import SnowNLP
import pandas as pd
import requests
import re
import os
import numpy as np
import matplotlib.pyplot as plt
keyword=['抽菸','宿舍','社團','活動','同性','同志','通識','性騷擾','警衛','停車','教官','學生會','老師','遺失','換課','選課','女二宿','共A','共B','共C','共D','共E','車棚']
ws = WS("C:/Users/shengkai/Documents/dcard爬蟲/data")
pos = POS("C:/Users/shengkai/Documents/dcard爬蟲/data")
ner = NER("C:/Users/shengkai/Documents/dcard爬蟲/data")
f2 = open("篩選後.html", "w" ,encoding = 'utf-8')
f3 = open("篩選前.html", "w" ,encoding = 'utf-8')
f2.write("<html><body><center><table width=800 height=200 border=1><tr><th>標題</th><th>關鍵字</th><th>情感分析</th><th>原文網址</th><th>文章日期</th></tr>")
f3.write("<html><body><center><table width=800 height=200 border=1><tr><th>標題</th><th>關鍵字</th><th>情感分析</th><th>原文網址</th><th>文章日期</th></tr>")
deaddate=7
datecontent=[]
def Crawl(ID):
    keywordtemp=[]
    getkeyword=0
    link = 'https://www.dcard.tw/_api/posts/' + str(ID)
    requ = requests.get(link)
    rejs = requ.json()
    month=int(rejs['createdAt'][5:7])
    day=rejs['createdAt'][0:10]
    checkday=0
    for i in range(len(datecontent)):
        if datecontent[i] == day:
            checkday=1
         
    if month == deaddate:
        print('yes')
        if checkday==0:
            datecontent.append(day)
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
            f2.write("<td><a href='https://www.dcard.tw/f/nptu/p/"+str(ID)+"'>點我</a></td><td>"+day+"</td></tr>")
            
        f3.write("<td>")    
        if s_senti >= 0.6:
            #f3.write("此篇分析為正面"+str(s_senti))
            f3.write("此篇分析為正面")
        elif s_senti <= 0.6:
            #f3.write("此篇分析為負面"+str(s_senti))
            f3.write("此篇分析為負面")
        f3.write("</td>")
        f3.write("<td><a href='https://www.dcard.tw/f/nptu/p/"+str(ID)+"'>點我</a></td><td>"+day+"</td></tr>")  
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
            [{#'ID':rejs['id'],
              '標題':rejs['title'],
              '內文':rejs['content'],
              #'excerpt':rejs['excerpt'],
              #'createdAt':rejs['createdAt'],
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
              columns=['標題','內文','回應次數','性別','點讚數','關鍵字']
            ))
    else:
        print('no')
url = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=50'
#url2 = 'https://www.dcard.tw/_api/forums/nptu/posts?popular=false&limit=10'
resq = requests.get(url)
rejs = resq.json()
df = pd.DataFrame()
for i in range(len(rejs)):
    df = df.append(Crawl(rejs[i]['id']),ignore_index=True)
print(df.shape)
df

fig = plt.figure()
plt.xticks(range(len(datecontent)),datecontent, rotation=45)
plt.show()

f2.write("</table></body></center></html>")
f2.close
f3.write("</table></body></center></html>")
f3.close
df.to_excel('C:/Users/shengkai/Documents/dcard爬蟲/熱門.xlsx')
print(datecontent)