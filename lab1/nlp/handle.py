#encoding:utf-8
__author = 'Zhaozitian'
#written with Akko 3018V2

import re
import urllib.request
import urllib
import queue
import threading
import os

queue = queue.Queue()
visited = set()
cnt = 0

class handle(threading.Thread):
	def __init__(self, queue, opener, blog_name):
		threading.Thread.__init__(self)
		self.queue = queue
		self.opener = opener
		self.blog_name = blog_name
		self.lock = threading.Lock()

if __name__ == '__main__':
	print ('asd')