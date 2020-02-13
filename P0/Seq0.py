def seq_ping():
    print("OK")

seq_ping()


from pathlib import Path

FILENAME = input("introduce a filename")
def seq_read_fasta(filename):
    file_contents = Path(FILENAME).read_text().split("\n")[1:]
    file_contents_final = "".join(file_contents)
    print(file_contents_final)

seq_read_fasta(FILENAME)

