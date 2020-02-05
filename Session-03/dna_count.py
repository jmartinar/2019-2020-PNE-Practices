#Session 3 - Exercise 2

dna_seq = input("Introduce the sequence: ")

def total_lenght(dna_seq):
    counter = 0
    for letter in dna_seq:
        counter += 1
    return counter

def letter_counter(dna_seq):
    a = 0
    g = 0
    t = 0
    c = 0
    for letter in dna_seq:
        if letter == "A":
            a += 1
        elif letter == "G":
            g += 1
        elif letter == "T":
            t += 1
        elif letter == "C":
            c += 1
    return ("A: ", a, "C: ", c, "T:", t, "G: ", g)

print("Total length is: ", total_lenght(dna_seq))
print(letter_counter(dna_seq))
