from Seq1 import *

def print_seqs(seq_list):       #exercise 2: function to print the seq, its position and its length
    for i in range(len(seq_list)):
        print("Sequence", i + 1, ": (Length:",  seq_list[i].len(), ")",  seq_list[i])

#--Main prog
print("-----|Exercise 1|-----")

s1 = Seq("ACTGA")
seq_list = []
seq_list.append(s1)

print_seqs(seq_list)

