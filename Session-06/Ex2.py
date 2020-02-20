


def print_seqs(seq_list):
    for e in range(len(seq_list)):
        print("Sequence", e, ": (Length:",  seq_list[e].len(), ")",  seq_list[e])


print_seqs([Seq("ACT"), Seq("GATA"), Seq("CAGATA")])
