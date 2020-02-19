class Seq:
    "A class for representing sequence objects"
    def __init__(self, strbases):

        for x in strbases:
            if (x != "A") and (x != "T") and (x != "G") and (x !="C"):
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

class Gene(Seq):
    pass


# -- Main prog
s1 = Seq("AACGTC")
s2 = Seq("werwetr")

print(f"sequence 1: {s1}")
print(f"sequence 2: {s2}")
