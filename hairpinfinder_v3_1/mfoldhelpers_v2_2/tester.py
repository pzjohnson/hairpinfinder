
import threading

import time

from MfoldOutput import MfoldOutput


start_time = time.time()

num = 8

dest_list = []

for i in range(num):
    dest_list.append(None)

threads = []

for i in range(num):
    t = threading.Thread(target=MfoldOutput.thread_create,
                         args=(dest_list,
                               i,
                               "http://unafold.rna.albany.edu/cgi-bin/ct.cgi?ID=17Feb05-16-17-11&NAME=sort"))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print time.time() - start_time


no_thread_start = time.time()

for i in range(num):
    MfoldOutput("http://unafold.rna.albany.edu/cgi-bin/ct.cgi?ID=17Feb05-16-17-11&NAME=sort")

print time.time() - no_thread_start
