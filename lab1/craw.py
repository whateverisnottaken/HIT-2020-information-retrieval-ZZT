# encoding:utf-8
# written with AKKO 3108V2
__author__ = 'Zhaozitian'

import Handle
from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.font
import threading
import queue
import random

gui_que = queue.Queue()

class Generator(threading.Thread):


	def __init__(self, root):
		threading.Thread.__init__(self)
		self.progress = ''
		self.root = root
		self.createFrame()
		self.createFrameTop()

	def createFrameTop(self):
		self.frm_top_label = tk.Label(self.root, text = 'Zhao Zitian \'s Crawler', font = ('stencil', 15), foreground = random.choice(['red']))
		self.frm_top_label.grid(row = 0, column = 0, padx = 10, pady = 10)

	def createFrame(self):
		self.frm = tk.LabelFrame(self.root)
		self.frm.grid(row = 1, column = 0, padx = 5, pady = 10)

		self.frm_label_name = tk.Label(self.frm, text='BlogName:', font=('stencil', 11))
		self.frm_label_name.grid(row=0, column=0, padx=5, pady=10)

		self.frm_entry_name = tk.Entry(self.frm)
		self.frm_entry_name.grid(row=0, column=1, padx=5, pady=10)

		self.frm_label_num = tk.Label(self.frm, text='ThreadNum:', font=('stencil', 11))
		self.frm_label_num.grid(row=1, column=0, padx=5, pady=10)

		default_value = StringVar()
		default_value.set('10')
		self.frm_entry_num = tk.Entry(self.frm, textvariable=default_value)
		self.frm_entry_num.grid(row=1, column=1, padx=5, pady=10)

		self.frm_button_cancel = tk.Button(self.frm, text='  Cancel  ', command=self.root.quit, font=('stencil', 11))
		self.frm_button_cancel.grid(row=2, column=0, padx=25, pady=10)

		self.frm_button_download = tk.Button(self.frm, text='Download', command=self.download, font=('stencil', 11))
		self.frm_button_download.grid(row=2, column=1, padx=5, pady=10)

	def createFrameBottom(self):
		self.frm_bottom_label = tk.Label(self.root, text=self.progress)
		self.frm_bottom_label.grid(row=2, column=0)

	def download(self):
		self.name = self.frm_entry_name.get()
		self.num = self.frm_entry_num.get()
		self.createFrameBottom()
		self.progress = 'Downloading...'
		if self.name == '':
			messagebox.showwarning('Warning', 'It seems like you didn\'t enter the blog name.')
		elif not self.num.isdigit():
			messagebox.showwarning('Warning', 'It seems like that \'' + self.num + '\' isn\'t a good  number.')
		elif int(self.num) == 0:
			messagebox.showwarning('Warning', 'Nope. I think 0 threads is too few.')
		else:
			gui_que.put(self.name)
			self.progress += 'please wait...'
			self.frm_bottom_label.config(text=self.progress)

	def run(self):
		while True:
			name = gui_que.get()
			Handle.init(name, int(self.num))
			tasks = Handle.queue.unfinished_tasks
			if tasks == 0:
				self.progress += "done!!!"
				self.frm_bottom_label.config(text=self.progress)
			if Handle.cnt == 0:
				messagebox.showerror('Error', 'Can not download. Please check internet.')
			else:
				messagebox.showinfo('Download Succeeded',
									'Download ' + str(Handle.cnt - 1) + ' blogs, saved in ./blog directory')
			gui_que.task_done()

def center_window(w=300, h=220):
	# get screen width and height
	ws = root.winfo_screenwidth()
	hs = root.winfo_screenheight()
	# calculate position x, y
	x = (ws / 2) - (w / 2)
	y = (hs / 2) - (h / 2)
	root.geometry('%dx%d+%d+%d' % (w, h, x, y))

if __name__ == '__main__':
	root = tk.Tk()
	root.title('lab1_crawler')
	center_window()
	t = Generator(root)
	t.setDaemon(True)
	t.start()
	root.mainloop()
