
"""
This class represents a base pair in the folded structure of a single-stranded RNA molecule.
"""


class BasePair(object):
    """
    'pos1' and 'pos2' are integer types that represent the two positions of the base pair.
    """
    def __init__(self, pos1, pos2, seq, offset):
        # 'self.pos1' will always be the lower position
        if pos1 < pos2:
            self.pos1 = pos1
            self.pos2 = pos2
        elif pos2 < pos1:
            self.pos1 = pos2
            self.pos2 = pos1
        else:
            raise Exception('A base cannot be paired with itself.')

        self.seq = seq
        self.offset = offset

    def __eq__(self, other):
        return self.pos1 == other.pos1 and self.pos2 == other.pos2

    def __lt__(self, other):
        if self.pos1 != other.pos1:
            return self.pos1 < other.pos1
        else:
            return self.pos2 < other.pos2

    def __hash__(self):
        return hash(str(self.pos1) + ',' + str(self.pos2))

    def __str__(self):
        return '(' + str(self.pos1) + ', ' + str(self.pos2) + ')'
