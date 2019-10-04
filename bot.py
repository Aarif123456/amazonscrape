from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import re
import requests
import lxml
import os
import urllib.parse
import pprint
import itertools
import math  

# py mongo
# tuples into list
# data in dictionary


class AmazonBot:

    def __init__(self, keyword):
        self.driver = webdriver.Firefox(executable_path='C:/geckodriver.exe')
        self.keyword = keyword

    def source_code(self):
        driver = self.driver
        for page in range(1,6):
            url = 'https://www.amazon.com/s?k='+ urllib.parse.quote_plus(self.keyword) 
            if page>1:
                url += '&page='+str(page) +'&ref=sr_pg_'+str(page)
            else:
                url += '&ref=nb_sb_noss_2'
            driver.get(url)
            time.sleep(5)
            test1 = driver.page_source
            with open(self.keyword+str(page)+'.html', 'w', encoding='utf-8') as f:
                f.write(str(test1))
        driver.quit()
    @staticmethod
    def stripElements(i):
        try:
            price = (i.find('span', {"class": "a-offscreen"}).text)
            # print("original price" , price)
            # price = re.findall('(([0-9]*,(\s)*)*[0-9]+\.[0-9]{2})',price)
            # price = price[0][0].replace(",", "")
            price = price.replace(",", "").replace("$", "")
            # print(price)
            # print("price----------------------------------------"+price)
        except AttributeError:
            price = -1 #test this more but 
        try:
            title = (i.h2.text).strip()
            print("title----------------------------------------" +title)
            if(price==-1):
                price = re.findall('(\$)(\s)*(([0-9]*,)*[0-9]+\.[0-9]{2})', str(i))
                if(len(price) > 0):
                    price = price[0][2].replace(",", "")
                else:
                    print("No price found")
                    return None        
            # print("price----------------------------------------")
            # print(price)
            price = (float)(price)
            tag_url = re.findall(
                '(href=")((.*?)dp/[a-zA-Z0-9]{10})(.*?)(")', str(i)) #[0].replace("href=\"", "")
            if(len(tag_url)>0):
                tag_url = tag_url[0][1]
            else:
                print("No URL found")
                return None;
            # print("tag_url---------------------------------------"+tag_url)
            full_url = ("https://www.amazon.com%s" % tag_url)
            # print("full_url---------------------------------------"+full_url)
            tag_image = re.findall(
                '(<img.*)(src=)(\s)*"((.*?)[a-zA-Z0-9]?_\.(jpg|png){1})(\s)*(")(.*?) 1x', str(i))
            if(len(tag_image)>0):
                tag_image = tag_image[0][3]
            else:
                print("No image found")
                return None;
            # print("tag_image---------------------------------------"+tag_image)
            # tag_image = re.findall('https://(.*?)\.(jpg|png){1}', tag_image)[0][0:-1]
            dict = {'Title': str(title), 'Price': str(
                price), 'URL': str(full_url), 'Image': str(tag_image)}
            return dict
        except AttributeError:
            print("----------------parse error--------------------")
            # print(i)  

    def list_layout_amazon(self):
        allItem=[]
        driver = self.driver
        for page in range(1,6):
            source = open(self.keyword+str(page)+'.html', "rb").read()
            soup = bs(source, "html.parser")
            cash = soup.find_all("div", {"class": "sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
            for i in cash:
                dict = AmazonBot.stripElements(i)
                if dict is not None:
                    allItem.append(dict)

        driver.quit()
        return allItem       
    
    def grid_layout(self):
        allItem = []
        driver = self.driver
        for page in range(1,6):
            source = open(self.keyword+str(page)+'.html', "rb").read()
            soup = bs(source, "html.parser")
            cash = soup.find_all("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"})
            for i in cash: #parse elements from html then use                
                dict = AmazonBot.stripElements(i)
                if dict is not None:
                    allItem.append(dict)

        driver.quit()       
        return allItem
        


    
            
    # pprint.pprint(mainNameDict)



# for x in tag_url:
#     tag_url[x]
#     print(relative_url)

# relative_url = re.findall('=".+', str(tag_url[0]))
# print(tag_url)
# relative_url = tag_url.split('="')
# print(str(relative_url))
# final_url = relative_url.split(';')[0]
# print(final_url)
# relative_image = re.findall('<img.*[a-zA-Z0-9]?_\.jpg 1', str(i))[0][0:-2]

# for i in cash:
#     try:
#         title = (i.h2.text)
#         Price = (i.find('span', {"class": 'a-offscreen'}).text)
#         relative_url = re.findall('href=.*;', str(i))
#
#         url = (str(relative_url.group(0)).split(';')[1])
#         #full_url = urllib.parse.urljoin(("https://www.amazon.com/", url))
#         print(relative_url)
#         print('title %s %s' % (title, Price))
#         # f = open("open.html")
#     except AttributeError:
#         print("Finished")
