# encoding:utf-8
# written with AKKO 3108V2
__author__ = 'Zhaozitian'

import os
import json
import re
import bs4
import urllib
from bs4 import BeautifulSoup

def json_generate(folderPath):
	jsonAll = []
	stopwords = []
	file = open('./stopwords.txt', encoding = 'utf-8')
	for line in file:
		stopwords.append(line)
	file.close()
	jsonfile = open('./preprocessed.json', 'w+')
	for file in getfiles(folderPath):
		htmlfile = open(folderPath + '/' + file, encoding = 'utf-8')
		htmlhandle = htmlfile.read()
		soup = BeautifulSoup(htmlhandle, 'lxml')
		temp = {}
		temp['url'] = url
		temp['segmented title'] = file.split('\'')
		for i in temp['segmented title']:
			if i in stopwords:
				temp['segmented title'].remove(i)
		temp['segmented_paragraphs'] = []
		for line in htmlfile:
			temp['segmented_paragraphs'].append(line)
		temp['file_name'] = files
		#jsonfile.dumps(temp)
		#print(temp)
		jsonfile.write(json.dumps(temp) + '\n')

		#jsonAll.append(json.dumps(temp))


	#jsonfile = open('./preprocessed.json', 'wb+')
	#jsonfile.write(jsonAll)
	jsonfile.close()


def getfiles(folderPath):
	return os.listdir(folderPath)




