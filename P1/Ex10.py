from Seq1 import Seq

bases = ["A", "C", "T", "G"]
list_of_genes = ["U5", "ADA", "FRAT1", "FXN", "RNU6_269P" ]
txt = ".txt"
FOLDER = "../Session-04/"
s0 = Seq('')


for e in list_of_genes:
    val = 0
    base = ''
    s0 = s0.read_fasta(FOLDER+e+txt)
    for i, t in (s0.count()).items():
        while t > val:
            val = t
            base = i
    print("Gene ", e, " : Most frequent base: ", base)