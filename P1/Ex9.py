from Seq1 import Seq

#--Main prog
print("-----|Practice 1, Exercise 9|-----")

FOLDER = "../Session-04/"
file_name = FOLDER + "U5.txt"

s = Seq("")
s = s.read_fasta(file_name)

print("Sequence", 1, ": (Length:",  s.len(), ")",  s)
print(f"Bases: {s.count()}")
print(f"Reverse: {s.reverse()}")
print(f"Comp: {s.complement()}")