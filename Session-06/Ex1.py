class Seq:
    "A class for representing sequence objects"
    def __init__(self, strbases): #define in this function all our object1 properties

        for x in strbases:
            if (x != "A") and (x != "T") and (x != "G") and (x !="C"):  #checks if its a vaid seq
                print("Invalid seq detcted")
                self.strbases = "ERROR"
                return
        print("New sequence created!")
        self.strbases = strbases

    def __str__(self):   #return the string of characters of the object
        return self.strbases

    def len(self):    #return the lentgh of characters of the object
        return len(self.strbases)

    pass

# -- Main prog
s1 = Seq("AACGTC")
s2 = Seq("werwetr")

print(f"sequence 1: {s1}")
print(f"sequence 2: {s2}")