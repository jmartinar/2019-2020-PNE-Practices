from Client0 import Client
from Seq1 import Seq

PRACTICE = 2
EXERCISE = 5

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.40"
PORT = 8080
c = Client(IP, PORT) #merges ip and port as c

# --  message to and from the server
c.debug_talk("Sending U5 Gene to the server...") #send first message

FOLDER = "../Session-04/"
file_name = FOLDER + "FRAT1.txt"
s = Seq("")
s = s.read_fasta(file_name)
s = str(s)

#fragment divider
n = 10
for i in range(0, len(s), n):


c.debug_talk(f"Gene FRAT1: {s} \nFragment 1: ") #send the gene to the server