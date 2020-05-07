#encoding:utf-8
#written with Akko 3018V2
__author = 'Zhaozitian'

import re
import urllib.request
import urllib
import queue
import threading
import os

queue = queue.Queue()
visited = set()
cnt = 0

class Handle(threading.Thread):
	def __init__(self, queue, opener, news_name):
		threading.Thread.__init__(self)
		self.queue = queue
		self.opener = opener
		self.news_name = news_name
		self.lock = threading.Lock()

	def save_data(self, data, filename):
		if not os.path.exists('F:/news'):
			os.mkdir('F:/news')
		try:
			fout = open('F:/news/' + filename + '.html', 'wb+')
			fout.write(data)
		except IOError as e:

			print(len(filename))

	def find_title(self,data):
		data = data.decode('utf-8')
		begin = data.find('title') + 6
		end = str(data).find('\r\n',begin)
		if end > begin + 30:
			end = begin + 30
		title = data[begin:end]
		#title = str(cnt)
		return title

	def run(self):
		global cnt
		global visited
		while True:
			url = self.queue.get()
			self.lock.acquire()
			cnt += 1
			print('fetched ' + str(cnt-1) + ' targets; ' + 'now fetching: ' + url)
			self.lock.release()
			try:
				res = self.opener.open(url, timeout=1000)
			except Exception as e:
				if hasattr(e, 'reason'):
					print('reason:', e.reason)
				elif hasattr(e, 'code'):
					print('error code:', e.code)
				cnt -= 1
				self.queue.task_done()
				continue
			else:
				data = res.read()
			title = self.find_title(data)
			self.save_data(data,title)

			data = data.decode('utf-8')
			news_urls = re.compile('/' + self.news_name + '/' + '\d*' + '/' + '\S*' + '/page.htm')
			for url in news_urls.findall(data):
				print(url)
				url = 'http://hitgs.hit.edu.cn' + url
				if url not in visited:
					self.queue.put(url)
					visited |= {url}
					print('加入队列---》' + url)
			self.queue.task_done()

def init(startTime, number=10):
	global cnt
	global visited
	news_name = startTime.lower()
	th_num = int(number)
	url = 'http://hitgs.hit.edu.cn/tzgg/list.htm'
	opener = urllib.request.build_opener(urllib.request.HTTPHandler)
	headers = [
		('User-Agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko')
	]
	urllib.request.install_opener(opener)
	opener.addheaders = headers

	queue.put(url)
	visited |= {url}
	cnt = 0

	for i in range(th_num):
		t = Handle(queue,opener,news_name)
		t.setDaemon(True)
		t.start()
	queue.join()
	print('------finished-----')
	print('fetched ' + str(cnt) + ' targets.')

if __name__ == '__main__':
	init()