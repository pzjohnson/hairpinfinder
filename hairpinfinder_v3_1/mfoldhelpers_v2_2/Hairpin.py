
from LoopAlignment_v2_0.LoopAlignment import LoopAlignment

"""
This class represents a hairpin in a single-stranded RNA molecule.
"""


class Hairpin(object):
    """
	'seq' is the Sequence object for the RNA sequence
	'stem' is a list of BasePair objects representing the base pairs in the stem of the hairpin
	'offset' is the sequence numbering offset for the positions that the bases are labeled with
	"""
    def __init__(self, seq, stem, offset):
        self.seq = seq
        self.offset = offset

        if len(stem) == 0:
            raise Exception("Attempted to create a Hairpin object with a stem with zero base pairs.")

        self.stem = stem
        self.stem.sort(reverse=True)

        self.loop_seq = self.seq.get_substring(self.stem[0].pos1 + 1, self.stem[0].pos2 - 1, offset)

    def __str__(self):
        string = ""

        string += "stem: ["

        for bp in self.stem:
            string += bp.__str__() + ","

        string += "], loop: " + self.loop_seq
        return string

    def __lt__(self, other):
        if self.stem[0].pos1 != other.stem[0].pos1:
            return self.stem[0].pos1 < other.stem[0].pos1

        if self.stem[0].pos2 != other.stem[0].pos2:
            return self.stem[0].pos2 < other.stem[0].pos2

        return len(self.stem) > len(other.stem)

    def __eq__(self, other):
        return self.stem[0].__eq__(other.stem[0]) and self.stem[0].pos1 == other.stem[0].pos1

    def __hash__(self):
        return hash(str(self.stem[-1].pos1) + "," +
                    str(self.stem[0].pos1) + "," +
                    str(self.stem[0].pos2))

    def similar_to(self, other):
        smaller = self.loop_seq
        bigger = other.loop_seq

        if len(other.loop_seq) < len(self.loop_seq):
            smaller = other.loop_seq
            bigger = self.loop_seq

        if len(self.loop_seq) < 3 and len(other.loop_seq) < 3:
            if smaller in bigger:
                return True

            return False
        elif len(self.loop_seq) == 1 or len(other.loop_seq) == 1:
            return False
        elif len(smaller) == 2 and len(bigger) > 3:
            return False
        elif len(smaller) == 3 and len(bigger) > 5:
            return False

        if smaller in bigger:
            return True

        la = LoopAlignment(self.loop_seq, other.loop_seq)

        if la.local_length == 0:
            return False
        elif len(smaller) * 1.2 < la.local_length:
            return False

        if la.num_matches * 1.2 < len(smaller):
            return False

        return True
