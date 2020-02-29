import pathlib

class Client:
    """"A class for representing sequence objects"""
    def __init__(IP, PORT):
        IP = input("Introduce the ip adress: ")
        PORT = int(input("Introduce the port to connect: "))
        return IP, PORT

    def ping(self):
        print("OK")
