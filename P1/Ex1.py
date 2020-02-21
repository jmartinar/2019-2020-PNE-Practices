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

def print_seqs(seq_list):       #exercise 2: function to print the seq, its position and its length
    for i in range(len(seq_list)):
        print("Sequence", i + 1, ": (Length:",  seq_list[i].len(), ")",  seq_list[i])

#--Main prog
print("-----|Exercise 1|-----")

s1 = Seq("ACTGA")
seq_list = []
seq_list.append(s1)

print_seqs(seq_list)

