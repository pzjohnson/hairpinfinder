
import time

from HairpinFinder import HairpinFinder


start_time = time.time()

hpf = HairpinFinder("http://unafold.rna.albany.edu/cgi-bin/ct.cgi?ID=17Feb05-16-17-11&NAME=sort",
                    ["http://unafold.rna.albany.edu/cgi-bin/ct.cgi?ID=17Feb05-16-17-11&NAME=sort"])

print time.time() - start_time
