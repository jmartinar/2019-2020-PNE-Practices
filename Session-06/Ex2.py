class Seq:
    "A class for representing sequence objects"
<<<<<<< HEAD


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

#--Main program

def print_seqs(seq_list):       #exercise 2: function to print the seq, its position and its length
    for i in range(len(seq_list)):
        print("Sequence", i, ": (Length:",  seq_list[i].len(), ")",  seq_list[i])

print_seqs([Seq("ACT"), Seq("GATA"), Seq("CAGATA")])
>>>>>>> origin/master
