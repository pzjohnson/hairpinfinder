
from BasePair import BasePair
from Hairpin import Hairpin

"""
Contains the class definition for the Structure class, which represents a predicted structure output by mfold for a
single-stranded RNA sequence.
"""


class Structure(object):
    @staticmethod
    def thread_create(dest_list, i, sid, seq, bp_map, base_pairs, offset):
        dest_list[i] = Structure(sid, seq, bp_map, base_pairs, offset)

    """
    'sid' is an integer type used to identify the structure
    'seq' is a Sequence object representing the RNA sequence for the structure
    'base_pairs' is a list of BasePair objects
    'offset' represents the 'sequence numbering offset' parameter on mfold

    note that this __init__() function filters the input list of base pairs to remove repeats of the same base pair,
    thus self.base_pairs will be a set in mathematical terms (though not an actual Python Set type)
    """
    def __init__(self, sid, seq, base_pairs, offset):
        self.sid = sid
        self.seq = seq
        self.offset = offset

        self.base_pairs = base_pairs
        self.base_pairs.sort(reverse=True)

        # parse the hairpins in the structure
        self.hairpins = self.parse_hairpins()

    def __lt__(self, other):
        return self.sid - other.id

    def __eq__(self, other):
        return self.sid == other.id

    def __hash__(self):
        return hash(self.sid)

    """
    Returns a list of Hairpin objects representing the hairpins in the structure.
    """
    def parse_hairpins(self):
        hairpins = []

        if len(self.base_pairs) == 0:
            return hairpins

        is_hairpin = True
        top = 0

        for i in range(len(self.base_pairs) - 1):
            prev_bp = self.base_pairs[i]
            next_bp = self.base_pairs[i + 1]

            if is_hairpin:
                end = False
                stem = None

                if next_bp.pos1 != prev_bp.pos1 - 1 or next_bp.pos2 != prev_bp.pos2 + 1:
                    end = True
                    stem = self.base_pairs[top:i + 1]
                    is_hairpin = False
                elif i == len(self.base_pairs) - 2:
                    end = True
                    stem = self.base_pairs[top:]

                if end:
                    hairpins.append(Hairpin(self.seq, stem, self.offset))

            if next_bp.pos1 < prev_bp.pos1 and next_bp.pos2 < prev_bp.pos1:
                is_hairpin = True
                top = i + 1

        # if there is a hairpin at the very 5' end of the structure with a stem that has only one base pair
        if top == len(self.base_pairs) - 1:
            hairpins.append(Hairpin(self.seq, [self.base_pairs[-1]], self.offset))

        return hairpins
