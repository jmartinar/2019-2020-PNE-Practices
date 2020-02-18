class Seq:
    "A class for representing sequence objects"
    def __init__(self, strbases):
        self.strbases = strbases
        print("New seq created!")

    def __str__(self):
        return self.strbases

    def len(self):
        return len(self.strbases)

    pass

class Gene(Seq):
    pass

# -- Main prog
s1 = Seq("AACGTC")
g = Gene("ACCTGA")

print(f"sequence 1: {s1}")
print(f"sequence 2: {g}")

l1 = s1.len()
print(f"The len of the S1 is: {l1}")
print(f"The len of the S2 is: {g.len()}")
print("Testing obj")

