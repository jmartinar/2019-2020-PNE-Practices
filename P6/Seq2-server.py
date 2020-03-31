from Seq1 import Seq
import socket
import termcolor

# Configure the Server's IP and PORT
PORT = 8080
IP = "127.0.0.1"

#create some random chains to use the program
seq_list = ["TGTGAACATTCTGCACAGGTCTCTGGCTGCGCCTGGGCGGGTTTCTT", "CAGGAGGGGACTGTCTGTGTTCTCCCTCCCTCCGAGCTCCAGCCTTC",
            "CTCCCAGCTCCCTGGAGTCTCTCACGTAGAATGTCCTCTCCACCCC", "GAACTCCTGCAGGTTCTGCAGGCCACGGCTGGCCCCCCTCGAAAGT",
            "CTGCAGGGGGACGCTTGAAAGTTGCTGGAGGAGCCGGGGGGAA"]

#------------------------------------CREATING THE SERVER------------------------------------
# -- Step 1: create the socket
ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# -- Optional: This is for avoiding the problem of Port already in use
ls.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# -- Step 2: Bind the socket to server's IP and PORT
ls.bind((IP, PORT))

# -- Step 3: Configure the socket for listening
ls.listen()

while True:
    # -- Waits for a client to connect
    print("Waiting for Clients to connect")

    try:
        (cs, client_ip_port) = ls.accept()

    # -- Server stopped manually
    except KeyboardInterrupt:
        print("Server stopped by the user")

        # -- Close the listenning socket
        ls.close()

        # -- Exit!
        exit()

    else:

        # -- Read the message from the client
        # -- The received message is in raw bytes
        msg_raw = cs.recv(2048)

        # -- We decode it for converting it
        # -- into a human-redeable string
        msg = msg_raw.decode()

        argument_command = msg[msg.find(" ") + 1:] #para sacar la cadena que se solicita
        response = "ERROR"

    #ping
    if "PING" in msg:
        response = "OK!\n"   #just prints a message to check its connected

    #get
    elif "GET" in msg:
        response = seq_list[int(argument_command)]  #the get prints the chain located with the argument command chosen

    #info
    elif "INFO" in msg:
        seq_info = Seq(argument_command) #gets the seq chosen
        count_bases_string = "" #starts the count of bases in a new variable

        for base, count in seq_info.count().items():    #loop to count the base and the times it appears on the chain
            s_base = str(base) + ": " + str(count) + " (" + str(
                round(count / seq_info.len() * 100, 2)) + "%)" + "\n"   #calculates the percentage of the base in chain
            count_bases_string += s_base

        response = ("Sequence: " + str(seq_info) + "\n" +
                    "Total length: " + str(seq_info.len()) + "\n" +
                    count_bases_string)   #prints the result of the seq with its length and bases counted

    #complement
    elif "COMP" in msg:
        seq_comp = Seq(argument_command)    #takes the composite function with the method in Seq
        response = seq_comp.complement() + "\n" #prints the complement

    #reverse
    elif "REV" in msg:
        seq_rev = Seq(argument_command) #takes the reverse function with the method in Seq
        response = seq_rev.reverse() + "\n" #prints it

    #gene
    elif "GENE" in msg:
        gene = argument_command #takes the gene chosen in the argument
        s = Seq()
        s.read_fasta("../Session-04/" + gene + ".txt")
        response = str(s) + "\n"

        # -- The message has to be encoded into bytes
        # Server Console

    termcolor.cprint(msg[:msg.find(" ")], "green")
    print(response)

    # Client console
    cs.send(response.encode())
    # -- Close the data socket
    cs.close()