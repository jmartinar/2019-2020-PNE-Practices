import pathlib

class Seq:
    """"A class for representing sequence objects"""
    def __init__(self, strbases):
        if strbases == '':
            print("NULL Seq created!")
            self.strbases = "NULL"
        else:
            for e in strbases:
                if e not in ["A", "C", "T", "G"]:
                    print("INVALID seq")
                    self.strbases = "ERROR"
                    return
            print("New sequence created!")
            self.strbases = strbases

    def __str__(self):
        return self.strbases

    def len(self):
        for e in self.strbases:
            if e not in ["A", "C", "T", "G"]:
                return 0
        return len(self.strbases)

    def count_base(self, base):
        count_base = 0
        if self.strbases == '':
            return 0
        else:
            for e in self.strbases:
                if e not in ["A", "C", "T", "G"]:
                    return 0
                else:
                    if e in base:
                        count_base += 1
            return count_base

    def count(self):
        count_A = 0
        count_C = 0
        count_T = 0
        count_G = 0
        counter_list = []
        bases = ["A", "C", "T", "G"]
        if self.strbases == '':
            counter_list.append(count_A)
            counter_list.append(count_C)
            counter_list.append(count_T)
            counter_list.append(count_G)
            dict1 = dict(zip(bases, counter_list))
            return dict1
        else:
            for e in self.strbases:
                if e not in bases:
                    counter_list.append(count_A)
                    counter_list.append(count_C)
                    counter_list.append(count_T)
                    counter_list.append(count_G)
                    dict1 = dict(zip(bases, counter_list))
                    return dict1
                else:
                    if e in bases[0]:
                        count_A += 1
                    elif e in bases[1]:
                        count_C += 1
                    elif e in bases[2]:
                        count_T += 1
                    elif e in bases[3]:
                        count_G += 1
            counter_list.append(count_A)
            counter_list.append(count_C)
            counter_list.append(count_T)
            counter_list.append(count_G)
            dict2 = dict(zip(bases, counter_list))
            return dict2
    def reverse(self):
        rev_seq = ''
        if self.strbases == 'NULL':
            return self.strbases
        else:
            for e in self.strbases[::-1]:
                if e not in ["A", "C", "T", "G"]:
                    rev_seq = 'ERROR'
                    return rev_seq

                else:
                    rev_seq += e
        return (rev_seq)

    def complement(self):
        comp_seq = ""
        if self.strbases == 'NULL':
            return self.strbases
        else:
            for e in self.strbases:
                if e not in ["A", "C", "T", "G"]:
                    comp_seq = 'ERROR'
                    return comp_seq
                else:
                    if e in "A":
                        comp_seq += "T"
                    if e in "T":
                        comp_seq += "A"
                    if e in "C":
                        comp_seq += "G"
                    if e in "G":
                        comp_seq += "C"
            return (comp_seq)

    def read_fasta(self, filename):
        file_lines = pathlib.Path(filename).read_text().split("\n")
        body = (file_lines[1:])
        final_str = ''.join(body)
        final_str = Seq(final_str)
        self.strbases = final_str
        return (final_str)


    pass