class Seq:
    "A class for representing sequence objects"


def __init__(self, strbases):
    for x in strbases:
        if (x != "A") and (x != "T") and (x != "G") and (x != "C"):
            print("Invalid sequence detected")
            self.strbases = "ERROR"
            return

    print("New sequence created!")
    self.strbases = strbases


def __str__(self):
    return self.strbases


def len(self):
    return len(self.strbases)

pass

def print_seqs(seq_list):
    for i in range(0,len(seq_list)):
        print("Sequence ",i, "Length:", seq_list[i].len , seq_list[i])


# -- Main prog
print_seqs([Seq("ACT"), Seq("GATA"), Seq("CAGATA")])

