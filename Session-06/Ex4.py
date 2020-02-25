import termcolor

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

#--Main program

def print_seqs_colour(seq_list,colour):       #exercise 2: function to print the seq, its position and its length and added in exercise 4 a parameter to print coloured seq
    for i in range(len(seq_list)):
        termcolor.cprint(f"Sequence {i} : (Length: {seq_list[i].len()} ) {seq_list[i]}", colour)


def generate_seqs(pattern, number):    #exercise 3: function to generate a list with bases that repeats number times
    my_base = []   #create the list
    base = ""      #create the base
    for i in range(1, number+1):   #for from 1 to the number of repetitions chosen
        base = i * pattern        #the pattern is repeated i times in the list and also in the base creating a pyramid
        base = Seq(base)          #we apply Seq class properties
        my_base.append(base)      #append it to the main list
        base = ""                 #restart the base
    return(my_base)



seq_list1 = generate_seqs("A", 3)
seq_list2 = generate_seqs("AC", 5)

print("List 1:")
print_seqs_colour(seq_list1, "blue" )

print()
print("List 2:")
print_seqs_colour(seq_list2, "green")