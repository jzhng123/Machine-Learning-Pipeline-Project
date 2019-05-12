
from bs4 import BeautifulSoup

import requests
import pandasql as ps
import pandas as pd
import io
import csv

url2 = 'https://raw.githubusercontent.com/xh2389/OpenDataSetNewsPop/master/test.csv'
t = requests.get(url2).content
textdata = pd.read_csv(io.StringIO(t.decode('utf-8')))

# url3='https://raw.githubusercontent.com/thuhlz/OpenDataSetNewsPop/master/10_pop_news_dataset.csv'
# t2 = requests.get(url3).content
# textdata2 = pd.read_csv(io.StringIO(t2.decode('utf-8')))
#
# print(textdata2.columns)


def gettext():
    query = "SELECT url FROM textdata;"
    result = ps.sqldf(query, globals())
    return result

# get url list from test.csv
url_list=[]
url_list_full=[]
T_sql = gettext()
n=T_sql.shape[0]
j=6001
for x in T_sql['url'][6001:]:

    url_list.append(x[:-1])
    url_list_full.append(x)


head_list=[]
text_list=[]
image_links=[]
Has_image=[]
id=[]
i=0
for url in url_list:
    res = requests.get(url+ ".html")

    soup = BeautifulSoup(res.text,"html.parser")
    # print(soup)
    id.append(i)
    head = soup.select("title")[0].text  #get title
    head_list.append(head)

    for p in soup.select("section.article-content"):   #get content
        text = p.text.strip()
    text_list.append(text)

    # img = soup.find_all('img')[0]['src'].encode('utf-8')
    # img2=soup.select("section.article-content")

    imgs=[]
    link = soup.find_all('div')                #get image links
    for d in soup.find_all('div'):
        if d.img:
            if d.img.has_attr('data-image'):
                imgs.append(d.img['data-image'])


    if len(imgs)>1:
        image_links.append(imgs[0])
        Has_image.append(1)
    else:
        image_links.append(' ')
        Has_image.append(0)

    i += 1


test_news={"idx":id,"url":url_list_full,"title":head_list, "text": text_list, "pic":image_links ,"Has_image": Has_image}
test_topnews=pd.DataFrame(data=test_news,index=id)

newsTest_csv=test_topnews.to_csv('/Users/xinxinhuang/Desktop/Test Scrapy/test_news_2.csv',index=False,header=True)

