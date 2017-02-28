
from ct_file_parser import parse_ct_file
from CountedHairpin import CountedHairpin


class MfoldOutput:
    """
    Creates an MfoldOutput object using 'ct_file_url' and places it in the destination list 'dest_list' at index 'i'.
    """
    @staticmethod
    def thread_create(dest_list, i, ct_fil_url):
        dest_list[i] = MfoldOutput(ct_fil_url)

    """
    input the url of the ct file for all of the predicted structures
    """
    def __init__(self, ct_file_url):
        self.structures = parse_ct_file(ct_file_url)

        if len(self.structures) == 0:
            raise Exception("No structures found in ct file: " + ct_file_url)

        self.hp_counts = self.count_hairpins()

    def count_hairpins(self):
        counts = {}

        for s in self.structures:
            for hp in s.hairpins:
                if hp in counts:
                    counts[hp] += 1
                else:
                    counts[hp] = 1

        counted = []

        for hp in counts:
            counted.append(CountedHairpin(hp, counts[hp], len(self.structures)))

        counted.sort(reverse=True)
        return counted
