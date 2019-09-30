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
        url = ('https://www.amazon.com/s?k='+ urllib.parse.quote_plus(self.keyword) +'&ref=nb_sb_noss_2')
        driver.get(url)
        time.sleep(5)
        test1 = driver.page_source
        with open(self.keyword+'.html', 'w', encoding='utf-8') as f:
            f.write(str(test1))
        driver.quit()

    def list_layout_amazon(self):
        allItem=[]
        driver = self.driver
        source = open(self.keyword+'.html', "rb").read()
        soup = bs(source, "html.parser")
        cash = soup.find_all("div", {"class": "sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
        for i in cash:
            try:
                title = (i.h2.text).strip()
                Price = (i.find('span', {"class": 'a-offscreen'}).text)
                Price = re.findall('[0-9]+\.[0-9]{2}',Price)                    
                tag_url = re.findall('href=.*/[a-zA-Z0-9]{10}', str(i))[0].replace("href=\"", "")
                full_url = ("https://www.amazon.com%s" % tag_url)
                tag_image = re.findall('(<img.*)(src=)(.*[a-zA-Z0-9]?_\.(jpg|png){1}) 1x', str(i))[0][2]
                tag_image = re.findall('https://.*\.jpg"', tag_image)[0][0:-1]
                # print(full_url)
                # print(title)
                # print(Price)
                # print(full_url)
                # print(tag_image)
                dict = {'title': str(title), 'Price': str(Price), 'URL': str(full_url), 'Image': str(tag_image)}
                allItem.append(dict)


                # print(dict['title'])
                # print(dict['Price'])
                # print(dict['URL'])
                # print(dict['Image'])

            except AttributeError:
                print("Finished")

        driver.quit()
        return allItem

    def grid_layout(self):
        allItem = []
        driver = self.driver
        source = open(self.keyword+'.html', "rb").read()
        soup = bs(source, "html.parser")
        cash = soup.find_all("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"})
        for i in cash:
            try:
                title = (i.h2.text).strip()
                price = (i.find('span', {"class": "a-offscreen"}).text)
                price = re.findall('[0-9]+\.[0-9]{2}',price)
                tag_url = re.findall(
                    'href=.*/[a-zA-Z0-9]{10}', str(i))[0].replace("href=\"", "")
                full_url = ("https://www.amazon.com%s" % tag_url)

                tag_image = re.findall(
                    '(<img.*)(src=)(.*[a-zA-Z0-9]?_\.(jpg|png){1}) 1x', str(i))[0][2]

                dict = {'title': str(title), 'Price': str(
                    price), 'URL': str(full_url), 'Image': str(tag_image)}
                allItem.append(dict)

            except AttributeError:
                print("Finished")
        return allItem
        driver.quit()


    
            
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
