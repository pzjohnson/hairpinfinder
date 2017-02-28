
import threading

from mfoldhelpers_v2_2.MfoldOutput import MfoldOutput
from mfoldhelpers_v2_2.ConservedHairpin import ConservedHairpin

"""
This purpose of this class is to allow for comparisons between hairpins from the predicted
structures of different RNA sequences.
"""


class HairpinFinder(object):
    """
    'target' should be the URL for the ct file for the sequence of interest.
    'others' should be a list of ct file URLs that the other sequences that the target sequence will be compared to.

    'self.target' will be the MfoldOutput object of the target ct file.
    'self.others' will be a list of MfoldOutput objects for the other ct files.
    """
    def __init__(self, target, others):
        outputs = []

        for i in range(len(others) + 1):
            outputs.append(None)

        threads = []

        t = threading.Thread(target=MfoldOutput.thread_create, args=(outputs, 0, target))
        threads.append(t)
        t.start()

        for i in range(len(others)):
            t = threading.Thread(target=MfoldOutput.thread_create, args=(outputs, i + 1, others[i]))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        self.target = outputs[0]
        self.others = outputs[1:]

        self.conserved = self.find_hairpins()

    def find_hairpins(self):
        conserved = []

        for i in range(len(self.target.hp_counts)):
            conserved.append(None)

        threads = []

        for i in range(len(conserved)):
            t = threading.Thread(target=HairpinFinder.find_matches,
                                 args=(conserved, i, self.target.hp_counts[i], self.others))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        return conserved

    @staticmethod
    def find_matches(dest_list, i, target, others):
        matches = []

        for other in others:
            for other_count in other.hp_counts:
                if target.hp.similar_to(other_count.hp):
                    matches.append(other_count)

        dest_list[i] = ConservedHairpin(target, matches)
