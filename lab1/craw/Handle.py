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
	def __init__(self, queue, opener, blog_name):
		threading.Thread.__init__(self)
		self.queue = queue
		self.opener = opener
		self.blog_name = blog_name
		self.lock = threading.Lock()

	def save_data(self, data, filename):
		if not os.path.exists('blog'):
			blog_path = os.path.join(os.path.abspath('.'),'blog')
			os.mkdir(blog_path)
		try:
			fout = open('./blog/' + filename + '.html', 'wb+')
			fout.write(data)
		except IOError as e:

			print(len(filename))

	def find_title(self,data):
		data = data.decode('utf-8')
		begin = data.find('title') + 6
		end = str(data).find('\r\n',begin)
		if end > begin + 10:
			end = begin + 10
		title = str(cnt)
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
			blog_urls = re.compile('/' + self.blog_name + '/article/details/' + '\d*')
			for url in blog_urls.findall(data):
				url = 'http://blog.csdn.net' + url
				if url not in visited:
					self.queue.put(url)
					visited |= {url}
					# print('加入队列---》' + url)
			self.queue.task_done()

def init(name, number=10):
	global cnt
	global visited
	blog_name = name.lower()
	th_num = int(number)
	url = 'http://blog.csdn.net/' + blog_name + '/'
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
		t = Handle(queue,opener,blog_name)
		t.setDaemon(True)
		t.start()
	queue.join()
	print('------finished-----')
	print('fetched ' + str(cnt) + ' targets.')

if __name__ == '__main__':
	init()