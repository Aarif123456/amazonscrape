from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup as bs
import re
import requests
import lxml
import os
import urllib.parse

# py mongo
# tuples into list
# data in dictionary


class AmazonBot:

    def __init__(self):
        self.driver = webdriver.Firefox(executable_path='C:/Users/Gabe Gomer/PycharmProjects/geckodriver.exe')

    def source_code(self, keyword):
        driver = self.driver
        url = ('https://www.amazon.com/s?k='+ urllib.parse.quote_plus(keyword) +'&ref=nb_sb_noss_2')
        driver.get(url)
        time.sleep(5)
        pussy = driver.page_source
        with open('pussy.html', 'w', encoding='utf-8') as f:
            f.write(str(pussy))
        driver.quit()

    def list_layout_amazon(self):
        allItem=[]
        driver = self.driver
        source = open("pussy.html", "rb").read()
        soup = bs(source, "html.parser")
        cash = soup.find_all("div", {"class": "sg-col-20-of-24 s-result-item sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28"})
        for i in cash:
            try:
                title = (i.h2.text).strip()
                price = (i.find('span', {"class": 'a-offscreen'}).text)
                tag_url = re.findall('href=.*/[a-zA-Z0-9]{10}', str(i))[0].replace("href=\"", "")
                full_url = ("https://www.amazon.com%s" % tag_url)
                tag_image = re.findall('(<img.*)(src=)(.*[a-zA-Z0-9]?_\.jpg) 1x', str(i))[0][2]
                tag_image = re.findall('https://.*\.jpg"', tag_image)[0][0:-1]
                # print(full_url)
                # print(title)
                # print(price)
                # print(full_url)
                # print(tag_image)
                dict = {'Title': str(title), 'Price': str(price), 'URL': str(full_url), 'Image': str(tag_image)}
                allItem.append(dict)


                # print(dict['Title'])
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
        source = open("pussy.html", "rb").read()
        soup = bs(source, "html.parser")
        cash = soup.find_all("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"})
        for i in cash:
            try:
                title = (i.h2.text).strip()
                price = (i.find('span', {"class": "a-offscreen"}).text)

                tag_url = re.findall('href=.*/[a-zA-Z0-9]{10}', str(i))[0].replace("href=\"", "")
                full_url = ("https://www.amazon.com%s" % tag_url)
                # print(full_url)
                tag_image = re.findall('(<img.*)(src=)(.*[a-zA-Z0-9]?_\.jpg) 1x', str(i))[0][2]
                tag_image = re.findall('https://.*\.jpg"', tag_image)[0][0:-1]

                dict = {'Title': str(title), 'Price': str(price), 'URL': str(full_url), 'Image': str(tag_image)}
                allItem.append(dict)
                # print(dict[0])

                # print(title)
                # print(price)
                # print(full_url)
                # print(tag_image)
            except AttributeError:
                print("Finished")
        return allItem
        driver.quit()


gg = AmazonBot()
# gg.source_code('mouse')
print(gg.list_layout_amazon())
print(gg.grid_layout())

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
#         price = (i.find('span', {"class": 'a-offscreen'}).text)
#         relative_url = re.findall('href=.*;', str(i))
#
#         url = (str(relative_url.group(0)).split(';')[1])
#         #full_url = urllib.parse.urljoin(("https://www.amazon.com/", url))
#         print(relative_url)
#         print('Title %s %s' % (title, price))
#         # f = open("open.html")
#     except AttributeError:
#         print("Finished")
