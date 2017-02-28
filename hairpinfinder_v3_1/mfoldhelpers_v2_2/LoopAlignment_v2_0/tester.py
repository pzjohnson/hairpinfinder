
import time

from LoopAlignment import LoopAlignment


start_time = time.time()

for i in range(100):
    LoopAlignment("uuagcc", "uagccuu")

print time.time() - start_time

"""
pa = LoopAlignment("uagac", "uugac")
pa.print_alignment()
print "num matches: " + str(pa.num_matches)
print "local length: " + str(pa.local_length)
"""
