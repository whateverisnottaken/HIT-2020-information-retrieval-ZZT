# encoding:utf-8
# written with AKKO 3108V2
__author__ = 'Zhaozitian'

import queue
import json
import pyltp
from pyltp import Segmentor
import bs4
import os
import re


'''class Segment:
	def __init__(self):
		print('initialized.')'''

def process(folderPath):
	for file in getfiles(folderPath):
		oldName = folderPath + '/' + file
		segmentor = Segmentor()
		segmentor.load('F:/cws/cws.model')
		words = segmentor.segment(file[0:-6])
		newName = folderPath + '/' + '\''.join(words) + '.html'
		segmentor.release()
		os.rename(oldName, newName)

def getfiles(folderPath):
	return os.listdir(folderPath)

