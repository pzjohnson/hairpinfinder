
import urllib2

import threading

from Sequence import Sequence
from BasePair import BasePair
from Structure import Structure


"""
Parses the contents of a ct file from mfold. Generates Structure objects based on the contents of the ct file.
"""


# input the url of the ct file
def parse_ct_file(url):
    """
    Produces a list of Structure objects based on the contents of a ct file.
    """

    response = urllib2.urlopen(url)
    lines = response.read().splitlines()

    if len(lines) < 2:
        raise Exception("No structures found in ct file: " + url)

    # parse RNA sequence (as a Sequence object)
    seq = parse_seq(lines)

    # parse sequence numbering offset
    offset = parse_offset(lines)

    # parse structures
    structures = []

    for i in range(len(lines) / (seq.get_length() + 1)):
        structures.append(None)

    threads = []

    for i in range(len(structures)):
        t = threading.Thread(target=parse_structure,
                             args=(structures, i,
                                   lines[i * (seq.get_length() + 1):(i + 1) * (seq.get_length() + 1)], seq, offset))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return structures


def parse_seq_name(lines):
    return "".join(lines[0].split('\t', 1)[1].split(' ')[5:])


def parse_seq(lines):
    seq_name = parse_seq_name(lines)

    seq_length = int(lines[0].split('\t', 1)[0])

    seq = ""

    for i in range(1, seq_length + 1):
        seq += lines[i].split('\t', 2)[1]

    return Sequence(seq_name, 'RNA', seq)


def parse_offset(lines):
    items = lines[1].split('\t')
    return int(items[5]) - int(items[0])


def parse_structure(structures_list, i, lines, seq, offset):
    base_pairs = []

    for line in lines[1:]:
        items = line.split('\t')
        pos1 = int(items[5])
        pos2 = int(items[4])

        if pos2 != 0 and pos1 < pos2 + offset:
            base_pairs.append(BasePair(pos1, pos2 + offset, seq, offset))

    structures_list[i] = Structure(i, seq, base_pairs, offset)
