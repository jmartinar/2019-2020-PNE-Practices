from Client0 import Client

PRACTICE = 2
EXERCISE = 4

print(f"-----| Practice {PRACTICE}, Exercise {EXERCISE} |------")

IP = "192.168.1.40"
PORT = 8080
c = Client(IP, PORT) #merges ip and port as c

# --  message to and from the server
c.debug_talk("Message 1---")
c.debug_talk("Message 2: Testing !!!")