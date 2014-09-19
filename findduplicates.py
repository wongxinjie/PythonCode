#----------------------------------
# -*- coding: utf-8 -*-
# Function:python3ﾳÌÐòÉèﾼÆָÄÏÖеĶàÏ̵߳ÄһﾸöÀý×ӣﾬÓÃ4ÕҳöָﾶﾨĿ¼ÏµÄÖظﾴﾵÄÎļþ
# @Coder: Xinjie Wong
# @Date: 2014/09/12
#-----------------------------------
import os
import sys
import Queue
import hashlib
import optparse
import threading
import collections


def print_results(results_queue):
	while True:
		try:
			results = results_queue.get()
			if results:
				print results
		finally:
			results_queue.task_done()

class Worker(threading.Thread):
	Md5_lock = threading.Lock()

	def __init__(self, work_queue, md5_from_filename, results_queue, number):
		threading.Thread.__init__(self)
		self.work_queue = work_queue
		self.md5_from_filename = md5_from_filename
		self.results_queue = results_queue
		self.number = number

	def run(self):
		while True:
			try:
				size, names = self.work_queue.get()
				self.process(size, names)
			finally:
				self.work_queue.task_done()

	def process(self, size, filenames):
		md5s = collections.defaultdict(set)
		for filename in filenames:
			with self.Md5_lock:
				md5 = self.md5_from_filename.get(filename, None)
			if md5 is not None:
				md5s[md5].add(filename)
			else:
				try:
					md5 = hashlib.md5()
					with open(filename, "rb") as fh:
						md5.update(fh.read())
					md5 = md5.digest()
					md5s[md5].add(filename)
					with self.Md5_lock:
						self.md5_from_filename[filename] = md5
				except EnvironmentError:
					continue
		for filenames in md5s.values():
			if len(filenames) == 1:
				continue
			self.results_queue.put("{0}Duplicate files({1:n}bytes)\n\t{2}".format(self.number, 
				size, "\n\t".join(sorted(filenames))))

def main():
	if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
		print 'usage: {0} -thread_count -directory'.format(os.path.basename(sys.argv[0]))
		sys.exit(0)
	opts, path = sys.argv[1:]
	opts = int(opts)
	#opts, path = parse_options()
	data = collections.defaultdict(list)
	for root, dirs, files in os.walk(path):
		for filename in files:
			fullname = os.path.join(root, filename)
			try:
				key = (os.path.getsize(fullname), filename)
			except EnvironmentError:
				continue
			if key[0] == 0:
				continue
			data[key].append(fullname)
	work_queue = Queue.PriorityQueue()
	results_queue = Queue.Queue()
	md5_from_filename = {}
	for i in range(opts):
		number = i+1
		worker = Worker(work_queue, md5_from_filename, results_queue, number)
		worker.deamon = True
		worker.start()

	result_thread = threading.Thread(target=lambda: print_results(results_queue))
	result_thread.deamon = True
	result_thread.start()

	for size, filename in sorted(data):
		names = data[size, filename]
		if len(names) > 1:
			work_queue.put((size, names))
	work_queue.join()
	results_queue.join()


if __name__ == "__main__":
	main()


















			
















