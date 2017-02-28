
"""
This class is a pairing between a Hairpin object and the number of structures predicted by mfold that the hairpin
appears in.
"""


class CountedHairpin(object):
    """
    'hp' is a Hairpin object.
    'count' is the number of structures predicted by mfold that the hairpin appears in.
    'sample_size' is the total number of structures predicted by mfold.
    """
    def __init__(self, hp, count, num_structures):
        self.hp = hp
        self.count = count
        self.num_structures = num_structures
        self.score = float(self.count) / self.num_structures

    def __lt__(self, other):
        if self.score != other.score:
            return self.score < other.score

        return self.hp.__lt__(other.hp)

    def __str__(self):
        return self.hp.__str__() + "," + str(self.count)
