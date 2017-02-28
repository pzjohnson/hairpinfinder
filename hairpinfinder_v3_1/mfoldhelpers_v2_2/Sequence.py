
"""
This class represents a single-stranded RNA sequence.
"""


class Sequence(object):
    """
    'name', 'seq_type', and 'seq' should be strings.

    'name' is used to identify the sequence.
	'seq_type' is the type of molecule for the sequence (e.g. DNA, RNA, protein)
    'seq' is the sequence itself.

    Note that in this implementation, for two RNA sequences to be recognized as different, they must have different
    names.
    """
    def __init__(self, name, seq_type, seq):
        self.name = name
        self.seq_type = seq_type
        self.seq = seq

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def get_name(self):
        return self.name

    def get_length(self):
        return len(self.seq)

    """
    Input the start and end positions of the substring you wish to extract. Note that the input start and end positions
    should NOT be zero indexed.

    The substring returned will include the start and end positions.
    """
    def get_substring(self, start, end, offset):
        start -= offset
        end -= offset

        if start < 1 or start > len(self.seq) or end < 1 or end > len(self.seq):
            raise Exception("Start or end position for substring of " + self.name + " sequence is out of bounds: " +
                            "[start: " + str(start) + "], [end: " + str(end) + "]")

        if start > end:
            raise Exception("Start position of substring must be less than or equal to end position of substring.")

        return self.seq[start - 1:end]
