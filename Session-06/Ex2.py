class Seq:
    "A class for representing sequence objects"
    def __init__(self, strbases):

        for x in strbases:
            if (x != "A") and (x != "T") and (x != "G") and (x !="C"):
                print("Invalid seq detcted")
                self.strbases = "ERROR"
                return
        print("New sequence created!")
        self.strbases = strbases

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

    pass

#--Main program

def print_seqs(seq_list):
    for e in range(len(seq_list)):
        print("Sequence", e, ": (Length:",  seq_list[e].len(), ")",  seq_list[e])

print_seqs([Seq("ACT"), Seq("GATA"), Seq("CAGATA")])
