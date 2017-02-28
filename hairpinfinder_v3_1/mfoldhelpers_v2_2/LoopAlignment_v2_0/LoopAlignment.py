
from CONSTANTS import *

"""
This class represents a pairwise alignment between the loop sequences of two RNA hairpins.
"""


class LoopAlignment(object):
    all_alignments = {}

    @staticmethod
    def max_index(values):
        if len(values) == 0:
            return None

        max_value = values[0]
        max_index = 0

        for i in range(1, len(values)):
            if values[i] > max_value:
                max_value = values[i]
                max_index = i

        return max_index

    def __init__(self, loop1, loop2):
        if len(loop1) == 0 or len(loop2) == 0:
            raise Exception("Attempted to align a loop sequence of length zero.")

        self.loop1 = loop1.upper()
        self.loop2 = loop2.upper()

        self.alignment1 = ""
        self.alignment2 = ""

        self.num_matches = None
        self.local_length = None

        self.align_loops()

    def align_loops(self):
        # initialize to zero for safety
        self.num_matches = 0
        self.local_length = 0

        # check to see if an alignment of the given loop sequences has already been done
        first = self.loop1
        second = self.loop2

        if self.loop2 < self.loop1:
            first = self.loop2
            second = self.loop1

        first_and_second = first + "," + second

        # if the alignment has already been done
        if first_and_second in LoopAlignment.all_alignments:
            prev_alignment = LoopAlignment.all_alignments[first_and_second]

            self.alignment1 = prev_alignment.alignment1
            self.alignment2 = prev_alignment.alignment2
            self.num_matches = prev_alignment.num_matches
            self.local_length = prev_alignment.local_length

            return

        # create the 2D matrix to perform the computations for the alignment of 'self.loop1' and 'self.loop2' in
        matrix = []

        row1 = []

        for i in range(len(self.loop2) + 1):
            row1.append([0])

        matrix.append(row1)

        for i in range(1, len(self.loop1) + 1):
            row = [[0]]

            for j in range(1, len(self.loop2) + 1):
                row.append([0, 0, 0])

            matrix.append(row)

        # perform the computations for the alignment
        for i in range(1, len(self.loop1) + 1):
            for j in range(1, len(self.loop2) + 1):
                left = matrix[i][j - 1][LoopAlignment.max_index(matrix[i][j - 1])]

                if i == len(self.loop1):
                    matrix[i][j][0] = left
                else:
                    matrix[i][j][0] = left + GAP

                top_left = matrix[i - 1][j - 1][LoopAlignment.max_index(matrix[i - 1][j - 1])]

                if self.loop1[i - 1] == self.loop2[j - 1]:
                    matrix[i][j][1] = top_left + MATCH
                else:
                    matrix[i][j][1] = top_left + MISMATCH

                top = matrix[i - 1][j][LoopAlignment.max_index(matrix[i - 1][j])]

                if j == len(self.loop2):
                    matrix[i][j][2] = top
                else:
                    matrix[i][j][2] = top + GAP

        i = len(self.loop1)
        j = len(self.loop2)

        while i > 0 and j > 0:
            prev = LoopAlignment.max_index(matrix[i][j])

            if prev == 0:
                self.alignment1 += '-'
                self.alignment2 += self.loop2[j - 1]

                if i != len(self.loop1):
                    self.local_length += 1

                j -= 1
            elif prev == 1:
                self.alignment1 += self.loop1[i - 1]
                self.alignment2 += self.loop2[j - 1]

                if self.loop1[i - 1] == self.loop2[j - 1]:
                    self.num_matches += 1

                self.local_length += 1

                i -= 1
                j -= 1
            elif prev == 2:
                self.alignment1 += self.loop1[i - 1]
                self.alignment2 += '-'
                i -= 1

                if j != len(self.loop2):
                    self.local_length += 1

        if i > 0:
            while i > 0:
                self.alignment1 += self.loop1[i - 1]
                self.alignment2 += '-'
                i -= 1
        elif j > 0:
            while j > 0:
                self.alignment1 += '-'
                self.alignment2 += self.loop2[j - 1]
                j -= 1

        self.alignment1 = self.alignment1[::-1]
        self.alignment2 = self.alignment2[::-1]

        # add this alignment to the dictionary of all alignments
        LoopAlignment.all_alignments[first_and_second] = self

    def total_length(self):
        return len(self.alignment1)

    def print_alignment(self):
        line1 = ""

        for char in self.alignment1:
            line1 += char

        line2 = ""

        for char in self.alignment2:
            line2 += char

        print line1
        print line2
