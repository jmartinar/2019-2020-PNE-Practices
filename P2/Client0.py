import socket
import termcolor

class Client:
    def __init__(self, ip, port):  #ip changes depending on the pc used
        self.port = int(port)
        self.ip = ip

    def ping(self):
        print("Ok")

    def __str__(self):
        return(f"Connection to SERVER at {self.ip}, PORT: {self.port}")

    def talk(self, msg):
        response = ""
        # -- Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # establish the connection to the Server (IP, PORT)
        s.connect((self.ip, self.port))

        # Send data.
        s.send(str.encode(msg))

        # Receive data
        response = s.recv(2048).decode("utf-8")

        # Close the socket
        s.close()

        # Return the response
        return response

    def debug_talk(self, msg):
        #stores the message and the response
        message = str(msg)
        response = self.talk(msg)
        #prints both answers with different colors
        print("To server:")
        termcolor.cprint(message, 'blue')
        print("From server: ")
        termcolor.cprint(response, 'green')