from pymongo import MongoClient
import pymongo
import datetime
from bot import AmazonBot
import pprint
import pygame as pg
import PySimpleGUI as sg
import re
import itertools
import math  

def getDict(exampleList): #use dictionary to create clusters
    mainPriceDict = {}
    mainNameDict = {}
    mainURLDict = {}
    mainImageDict = {}
    relevantSet = set()

    # pprint.pprint(exampleList)
    for h in exampleList:
        # print(h)
        if(h==""):
            continue
        title = h['Title']
        price = (float)(h['Price'].strip())
        URL = h['URL']
        img = h['Image']
        mainList = title.strip().lower().replace("[", "").replace("(", "").replace(")", "").replace(",", "").replace("!", "").replace(":", " ").replace(" and ", " ").replace(" on ", " ").replace(" or ", " ").replace("-", " ").replace("]", " ").replace(" the " ," ").replace(" with " , " ").replace(" in " , "").replace(" for " , " ").replace(" an " , "").replace(" a " , "").replace("'", "").split(" ")
        title = h['Title'] #reget title so it is reloaded
        # print("pretrim")
        # print(mainList)
        mainList = list(dict.fromkeys(mainList))
        mainList = list(filter(None, mainList)) 
        # print("posttrim")
        # print(mainList)
        mainList = mainList[0:9]
        # print("cap")
        # print(mainList)
        mainSet = set(mainList) #don't need empty element
        # print("set")
        # print(mainSet)
        subSet=[]
        if(price=="" or title=="" or img =="" or URL == ""): #if error in problem skip over 
            continue
        for i in range(1,len(mainSet)): # go through entire list to make shit
                subSet=set(itertools.combinations(mainSet,i))
                for subElement in subSet: #for each combination of elements
                        if(subElement == ""):
                            continue
                        # print(subElement)
                        if(subElement in mainPriceDict):
                                mainPriceDict[subElement].append(price)
                                mainNameDict[subElement].append(title)
                                mainURLDict[subElement].append(URL)
                                mainImageDict[subElement].append(img)
                                 #if element list is bigger than one than we can compare to other element
                                relevantSet.add(subElement)
                        #can append other thing **
                        else: #create array with element
                                mainPriceDict[subElement] = [price]
                                mainNameDict[subElement] = [title]
                                mainURLDict[subElement] = [URL]
                                mainImageDict[subElement] = [img]                
    #pprint.pprint(relevantSet)
    #print("hella relevant")
    # pprint.pprint(mainPriceDict)
    #pprint.pprint(mainNameDict)
    # pprint.pprint(mainURLDict)
    #pprint.pprint(mainImageDict)
    #print("prices")
    meanDict = {}
    # countDict = {}
    moreRelevantSet = set()
    for i in relevantSet:
        # print(i)
        # print(mainPriceDict[i])
        count = 0
        sums = 0
        for j in mainPriceDict[i]:
            try:
                sums = sums + (j)
                count = count + 1
            except Exception as e:
                print(sums)
                print(count)
                print(e)
                print("Exception on "+j)
                continue
        try:
            if(count != 0):
                meanDict[i] = float(sums / count)
            if count > 3: #get elements whose means are a valid measurement
                moreRelevantSet.add(i)
        except Exception as e:
            print(e)
            continue
        
    
    # pprint.pprint(meanDict)
    #print("MEAN!")
    sumSquared =0 
    numCount = 0
    relevantVariance = {}
    for i in moreRelevantSet: #get the keys whose means are valid to find their variance
    # for i in relevantSet:
        numCount = 0
        sumSquared =0
        for j in mainPriceDict[i]:
            try:#for variance we get the sum(((value(x)-mean(x))^2)
                mean = (meanDict[i])
                #the try statement allows the code to keep functioning even if an invalid value was parsed
                difference = mean -  (j) 
                differenceSquared = difference * difference
                sumSquared += differenceSquared
                numCount = numCount + 1
            except Exception as e:
                continue
        if(numCount>0):
            relevantVariance[i] = (float)(sumSquared/numCount) #explicitely converting to float to show that I want to mantain accuracy
    # pprint.pprint(moreRelevantSet)
    # pprint.pprint(relevantVariance)
    # print("Variance")
    # goodDeal = False
    outPut =[]
    # for i in moreRelevantSet:
    categoryPrompt=['steal','awesome deal','pretty good deal']
    for i in relevantVariance:
        for j in range(len(mainPriceDict[i])): 
        #iterate through the same items whose mean were considered relevant and compare them
            num = mainPriceDict[i][j] 
            mean = (meanDict[i])
            try:
                sd = math.sqrt(relevantVariance[i])
                if(sd == 0): #make sure standard deviation was not 0 
                    continue
                zScore = (num-mean)/sd
            except Exception as e:
                print(e)
                continue
            title = mainNameDict[i][j]
            category = " ".join(i)
            text = " The item " + title
            # print(zScore)
            if zScore<-1.4:
                text = text + " is a "+categoryPrompt[int(round(zScore))+3] +" in the category of a " + category
                text = text + " with the price of price ${0:.2f}\n".format(num)
                text = text + "Which can be found at " +  mainURLDict[i][j] +"\n"
                outPut.append(text)
                print(text)
                #can only load up image
    if len(outPut) == 0 :
        print("Sorry there were no thrifty deals on the searched page:(")
        
# All the stuff inside your window.
layout = [  [sg.Text('Please type a keyword for this program to check prices to on Amazon')],
            [sg.Text('Enter something: '), sg.InputText()],
            [sg.Button('Search'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Thrifty for Amazon', layout)
text_input = []
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    text_input = values[0]
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break
    elif event in (None, "Search"):
        break
window.close()


# create an object of the Amazon Bot class
emsee = AmazonBot(text_input) #text_input
emsee.source_code()  # run the source code
# this collects the list layout as a list of dictionaries
outPutA = getDict(emsee.list_layout_amazon())
# this collects the grid layout as a list of dictionaries
outputB = getDict(emsee.grid_layout())



# try:
#     listDisplayA = outPutA['Display']
#     listStoreA = outPutA['Store']
# except Exception as e:
#     listDisplayA =[]
#     listStoreA = []
    
# try:
#     listDisplayB = outPutB['Display']
#     listStoreB = outPutB['Store']
# except Exception as e:
#     listDisplayB =[]
#     listStoreB = []
    
main_Display_list = []  # this will hold the final list of the two



main_Store_list = []  # this will hold the final list of the two

# this if block checks if either one of the list is empty
# if len(listStoreA) == 0 and len(listStoreB) != 0:
#     # print("You are in condition a")
#     main_Store_list = listStoreB
# if len(listStoreB) == 0 and len(listStoreA) != 0:
#     # print("You are in condition a")
#     main_Store_list = listStoreA
# else:
#     # print("You are in condition b")
#     main_Store_list = listStoreA.extend(listStoreB)

# client --> database --> collection --> documents

# this connects to my pymongo atlas account
client = pymongo.MongoClient(
    "mongodb+srv://emsee:magic2@network-dx1rg.mongodb.net/test?retryWrites=true&w=majority")

# this makes a db object called magicDB
magicDB = client["magicDB"]

# this makes a collection object called main_collection
main_collection = magicDB["main_collection"]

post = {}
# this for loop loads the contents of the web scraped list into the main_collection
# every dictionary element in the main_Store_list is considered a document
# for post in main_Display_list:
#      print(post['Text'])
#      post_id = main_collection.insert_one(post).inserted_id
                #post['Title']#have to display
                #outputDict['URL'] # we should make limkable
        #outputDict['Image']#screen.blit -> downloaded imge
                #outputDict['Category'] #Diplsay
   
    # this inserts the documents into the collection and gives each an id
   

# prompt to delete collection documents after use
if(input("do you want to delete collection documents? ") == "y"):
    result = main_collection.delete_many({})

# the method below will get a list of collection names of which data can be downloaded from
# pprint.pprint(magicDB.list_collection_names())
