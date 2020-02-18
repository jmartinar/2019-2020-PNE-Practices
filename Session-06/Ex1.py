class Seq:
    "A class for representing sequence objects"
    def __init__(self, strbases):

        bases = ["A","T","C","G"]
        if self.strbases in bases:
            self.strbases = strbases
            print("New seq created!")
        else:


    def __str__(self):
        return self.strbases

    pass

# -- Main prog
s1 = Seq("AACGTC")
s2 = Seq("werwetr")

print(f"sequence 1: {s1}")
print(f"sequence 2: {s2}")