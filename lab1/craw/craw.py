# encoding:utf-8
# written with AKKO 3108V2
__author__ = 'Zhaozitian'

import Handle
import Segment
import JsonGenerate
from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font
import threading
import queue
import random

gui_que = queue.Queue()

class Generator(threading.Thread):

	flag = 0
	
	def __init__(self, root):
		threading.Thread.__init__(self)
		self.progress = ''
		self.root = root
		self.createFrame()
		self.createFrameTop()

	def createFrameTop(self):
		self.frm_top_label = tk.Label(self.root, text = 'Zhao Zitian \'s Crawler', font = ('stencil', 15), foreground = 'red')
		self.frm_top_label.grid(row = 0, column = 0, padx = 10, pady = 10)

	def createFrame(self):
		self.frm = tk.LabelFrame(self.root)
		self.frm.grid(row = 1, column = 0, padx = 5, pady = 10)

		self.frm_label_name = tk.Label(self.frm, text='Start Time:', font=('stencil', 11))
		self.frm_label_name.grid(row=0, column=0, padx=5, pady=10)

		self.frm_entry_name = tk.Entry(self.frm)
		self.frm_entry_name.grid(row=0, column=1, padx=5, pady=10)

		self.frm_label_num = tk.Label(self.frm, text='Thread Num:', font=('stencil', 11))
		self.frm_label_num.grid(row=1, column=0, padx=5, pady=10)

		default_value = StringVar()
		default_value.set('10')
		self.frm_entry_num = tk.Entry(self.frm, textvariable=default_value)
		self.frm_entry_num.grid(row=1, column=1, padx=5, pady=10)

		self.frm_label_num = tk.Label(self.frm, text='Download Path:', font=('stencil', 11))
		self.frm_label_num.grid(row=2, column=0, padx=5, pady=10)
		self.frm_label_num2 = tk.Label(self.frm, text='G:\\news\\', font=('times new roman', 11))
		self.frm_label_num2.grid(row=2, column=1, padx=5, pady=10)

		self.frm_button_cancel = tk.Button(self.frm, text='       Cancel      ', command=self.root.quit, font=('stencil', 11), background = 'red', foreground = 'white')
		self.frm_button_cancel.grid(row=3, column=0, padx=25, pady=10)

		self.frm_button_download = tk.Button(self.frm, text='    Download     ', command=self.download, font=('stencil', 11), background = 'green', foreground = 'white')
		self.frm_button_download.grid(row=3, column=1, padx=25, pady=10)

		self.frm_button_process = tk.Button(self.frm, text=' NLP Process ', command=self.segment, font=('stencil', 11), background = 'blue', foreground = 'white')
		self.frm_button_process.grid(row=4, column=0, padx=25, pady=10)

		self.frm_button_generate = tk.Button(self.frm, text='json Generate', command=self.jsonGenerate, font=('stencil', 11), background = 'dark orange', foreground = 'white')
		self.frm_button_generate.grid(row=4, column=1, padx=25, pady=10)

	def createFrameBottom(self):
		self.frm_bottom_label = tk.Label(self.root, text=self.progress)
		self.frm_bottom_label.grid(row=2, column=0)

	def download(self):
		self.startTime = self.frm_entry_name.get()
		self.num = self.frm_entry_num.get()
		self.createFrameBottom()
		flag = 1
		self.progress = 'Downloading...'
		if self.startTime == '':
			messagebox.showwarning('Warning', 'It seems like you didn\'t enter the start time.')
		elif not self.num.isdigit():
			messagebox.showwarning('Warning', 'It seems like that \'' + self.num + '\' isn\'t a good  number.')
		elif int(self.num) == 0:
			messagebox.showwarning('Warning', 'Nope. I think 0 threads is too few.')
		else:
			gui_que.put(self.startTime)
			self.progress += 'please wait...'
			self.frm_bottom_label.config(text=self.progress)

	def jsonGenerate(self):
		JsonGenerate.json_generate('F:/news')

	def segment(self):
		Segment.process('F:/news')

	def run(self):
		while True:
			name = gui_que.get()
			Handle.init(name, int(self.num))
			tasks = Handle.queue.unfinished_tasks
			if tasks == 0:
				self.progress += "done!"
				self.frm_bottom_label.config(text=self.progress)
			if Handle.cnt == 0:
				messagebox.showerror('Error', 'Can not download. Please check internet.')
			else:
				messagebox.showinfo('Download Succeeded',
									'Download ' + str(Handle.cnt - 1) + ' news, saved in ./news directory')
			gui_que.task_done()

def center_window(w=362, h=340):
	# get screen width and height
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	# calculate position x, y
	x = (ws / 2) - (w / 2)
	y = (hs / 2) - (h / 2)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))

if __name__ == '__main__':
	flag = 0
	root = tk.Tk()
	root.title('lab1_crawler')
	center_window()
	t = Generator(root)
	t.setDaemon(True)
	t.start()
	root.mainloop()
