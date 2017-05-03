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
import numpy
import operator

def predictTextData(param):
    print ("inside function")
    dataList = []
    #dataList.append(param)
    ans = ProcessInput(param)
    EXTmodel = joblib.load("C:\\Users\\Harikrishnan\\Documents\\Python\\work\\EXT_model.pkl")
    CONmodel = joblib.load("C:\\Users\\Harikrishnan\\Documents\\Python\\work\\CON_model.pkl")
    AGRmodel = joblib.load("C:\\Users\\Harikrishnan\\Documents\\Python\\work\\AGR_Model.pkl")
    NEUmodel = joblib.load("C:\\Users\\Harikrishnan\\Documents\\Python\\work\\NEU_model.pkl")
    OPNmodel = joblib.load("C:\\Users\\Harikrishnan\\Documents\\Python\\work\\OPN_model.pkl")
    ext = EXTmodel.predict_proba(ans)
    con = CONmodel.predict_proba(ans)
    agr = AGRmodel.predict_proba(ans)
    neu = NEUmodel.predict_proba(ans)
    opn = OPNmodel.predict_proba(ans)
    print ("Printing type of")
    print type(ext)
    result = {"Extraversion":ext[0][1]*100,"Neuroticism":neu[0][1]*100,"Agreeableness":agr[0][1]*100,"Conscientiousness":con[0][1]*100,"Openness":opn[0][1]*100}
    charcater = max(result.iteritems(), key=operator.itemgetter(1))[0]
    result = {"Extraversion":ext[0][1]*100,"Neuroticism":neu[0][1]*100,"Agreeableness":agr[0][1]*100,"Conscientiousness":con[0][1]*100,"Openness":opn[0][1]*100,"Character":charcater}
    dataList.append(numpy.amax(ext))
    dataList.append(numpy.amax(con))
    dataList.append(agr[0][1])
    dataList.append(neu[0][1])
    dataList.append(opn[0][1])
    return result


def ProcessInput(data):
    print (data)
    empath_def_categories = kungfu.read_csv("C:\\Users\\Harikrishnan\\Desktop\\Empath\\CategoryANDSeedTerms.csv")
    empath_Processed_list = empathdata_preprocessing(empath_def_categories)
    matchedListFrame = find_matching_words2(data,empath_Processed_list)
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
    #for index,row in data_to_be_cleaned.iterrows():
    print ("inside dataclean")
    #print (type(data_to_be_cleaned))
    temp =  re.sub("[^a-zA-Z]"," ",data_to_be_cleaned)
    #print ("After ddd")
    temp = temp.lower()
    temp = temp.split()
    #punct_removed.append( temp)
    #data_to_be_cleaned['Review'] = kungfu.Series(punct_removed,data_to_be_cleaned.index)    
    #del data_to_be_cleaned['TEXT']
    return temp

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
