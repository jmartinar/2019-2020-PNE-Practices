from Client0 import Client

PRACTICE = 2
EXERCISE = 2

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.40"
PORT = 8080
c = Client(IP, PORT) #merges ip and port as c
print(c)
