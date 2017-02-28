
"""
This class represents a hairpin that is conserved among multiple RNA sequences.
"""


class ConservedHairpin(object):
    """
    'target' is the CountedHairpin object that similar hairpins were found for.
    'matches' is a list of CountedHairpin objects whose hairpins are similar to the target hairpin.
    """
    def __init__(self, target, matches):
        self.target = target
        self.matches = matches

    def __lt__(self, other):
        return self.target.__lt__(other.target)
