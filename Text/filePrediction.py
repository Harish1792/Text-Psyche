# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 22:37:59 2017

@author: Harikrishnan
"""


import pandas as kungfu
import re
from nltk.corpus import stopwords
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.externals import joblib
import os 

def predictFile():
    print ("inside function")
    #dataList = []
    #dataList.append(param)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dataFrame = kungfu.read_csv(dir_path+"/File/Input/Input.csv")
    ans = ProcessInput(dataFrame,dir_path)
    EXTmodel = joblib.load(dir_path+"/File/EXT_model.pkl")
    CONmodel = joblib.load(dir_path+"/File/CON_model.pkl")
    AGRmodel = joblib.load(dir_path+"/File/AGR_Model.pkl")
    NEUmodel = joblib.load(dir_path+"/File/NEU_model.pkl")
    OPNmodel = joblib.load(dir_path+"/File/OPN_model.pkl")
    ext = EXTmodel.predict(ans)
    print("EXT",ext)
    con = CONmodel.predict(ans)
    agr = AGRmodel.predict(ans)
    neu = NEUmodel.predict(ans)
    opn = OPNmodel.predict(ans)
    dataFrame['EXT'] = ext
    dataFrame['con'] = con
    dataFrame['agr'] = agr
    dataFrame['neu'] = neu
    dataFrame['opn'] = opn
    dataFrame.to_csv(dir_path+"/File/File_Prediction.csv")
    print ("writing to file")
    return dataFrame


def ProcessInput(data,dir_path):
    print ("Processing Input file")
    empath_def_categories = kungfu.read_csv(dir_path+"/File/CategoryANDSeedTerms.csv")
    empath_Processed_list = empathdata_preprocessing(empath_def_categories)
    matchedListFrame = find_matching_words(dataClean(data),empath_Processed_list)
    print ("done with ProcessInput")
    return matchedListFrame


def empathdata_preprocessing(empath):
    main_list =[]
    print ("In Empath Preprocessing")
    for i in range(0,194):
        col_list = []
        for j in range(1,170):
            col_list.append(empath.ix[i,j])
        main_list.append(col_list)
    #print ("function done")    
    return main_list

def dataClean(data_to_be_cleaned):  
    punct_removed = []
    for index,row in data_to_be_cleaned.iterrows():
        temp =  re.sub("[^a-zA-Z]"," ",row['TEXT']) 
        temp = temp.lower()
        temp = temp.split()
        punct_removed.append( temp)
    data_to_be_cleaned['Review'] = kungfu.Series(punct_removed,data_to_be_cleaned.index)    
    del data_to_be_cleaned['TEXT']
    return data_to_be_cleaned

def find_matching_words(edited_data,main_list):
    categList = []
    print ("In Matching Words")
    for index,value in edited_data.iterrows():
        tmpList = value['Review']
        oneRow = []
        for wordList in main_list:
                match = [x for x in tmpList if x in wordList]  
                #oneRow.append(len(set(tmpList)&set(wordList)))          
                oneRow.append(len(match))
        categList.append(oneRow)   
    return categList

def find_matching_words2(edited_data,main_list):
    categList = []
    print ("In Matching Words")    
    tmpList = edited_data
    oneRow= [] 
    for wordList in main_list:
        match = [x for x in tmpList if x in wordList]  
        #oneRow.append(len(set(tmpList)&set(wordList)))         
        oneRow.append(len(match))
        #print (len(match))
    categList.append(oneRow)   
    return categList
