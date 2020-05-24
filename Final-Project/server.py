import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq
import json

# Define the Server's port, IP and bases
PORT = 8080
IP = "127.0.0.1"
bases = ['A', 'C', 'T', 'G']

server = 'rest.ensembl.org'   #sever used
parameters = '?content-type=application/json'  #json parameters
conn = http.client.HTTPConnection(server)  #http connection to the server

# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True


# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
class TestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        """This method is called whenever the client invokes the GET method
        in the HTTP protocol request"""

        # Print the request line
        termcolor.cprint(self.requestline, 'green') #green request line

        req_line = self.requestline.split(' ') #splits the request line (by the spaces)

        arguments = (req_line[1]).split("?")  #We get the first request line and then the path, goes after /. We get the arguments that go after the ?

        first_argument = arguments[0] #sets the first argument

        contents = Path('Error.html').read_text() #no argument --> error form
        self.send_response(404)

        #--------------------------------------------MAIN PROGRAM--------------------------------------------
        try:

            # --------------------------------------------only / --------------------------------------------
            if first_argument == "/":  #return an HTML page with the forms for accessing to all the previous services

                contents = Path('index.html').read_text()   #contents displayed in index.html
                self.send_response(200)


            #--------------------------------------------listSpecies--------------------------------------------

            elif first_argument == '/listSpecies':     #part 2, list species --> html form list the names of all the species available in the database
                contents = f"""<!DOCTYPE html> 
                                    <html lang = "en">
                                    <head>
                                     <meta charset = "utf-8" >
                                     <title>List of species in the browser</title >
                                    </head >
                                    <body  style="background-color:rgb(255,255,182)">
                                     <h1 style="color:rgb(21,105,150);"> List of species in the genome database</h1>
                                     <p style="color:rgb(21,105,150);"><b>The total number of species in ensembl is: 286</b></p>
                                      """


                #Get the arguments after the ?
                get_value = arguments[1]

                #We need the value of the index --> position of the sequence
                seq_n = get_value.split('?')  #splits the argument by the ?
                seq_name, index = seq_n[0].split("=")  #splits by the =


                # menu of iteration to chose the path to act when the limit is inputed
                if index == "":  #no index is inputed --> all list must be printed
                    index = "286"
                if index == str: #this module works as an exception for when a string is inputed
                    contents = """<!DOCTYPE html> 
                                                        <html lang="en"> 
                                                            <head>
                                                                <meta charset="UTF-8">
                                                                <title>Error</title>
                                                            </head>
                                                            <body style="background-color:rgb(255,255,182)">
                                                                <h1>ERROR</h1>
                                                                <p> Selected specie's karyotype information is not available </p>
                                                                <p> Introduce a specie in the database to find its karyotype </p>
                                                                <a href="/"> Main page </a> </p>
                                                                </body>
                                                                </html>"""
                index = int(index)
                if index <= 0: #index less or equal to 0 --> error
                    contents = """<!DOCTYPE html>
                                <html lang="en" dir="ltr">
                                  <head>
                                    <meta charset="utf-8">
                                    <title>ERROR</title>
                                  </head>
                                  <body style="background-color: red;">
                                    <h1>ERROR</h1>
                                    <p>Resource not available</p>
                                    <p>Your search's limit is equal or less than 0</p>
                                  </body>
                                </html>"""
                if index > 0: #index more than 0
                    #html to print the total numbers of species selected
                    contents += f"""<p>The number of species you selected are: {index} </p>"""

                    #now program starts, gets the requested limit and ...

                    endpoint = 'info/species'  #stablishes the endpoint and its parameters for the request
                    parameters = '?content-type=application/json'
                    request = endpoint + parameters


                    try:
                        conn.request("GET", request)   #connection request

                    except ConnectionRefusedError:   #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()


                    #----------------------Main program of listSpecies------------------------

                    # -- Read the response message from the server
                    response = conn.getresponse()

                    # -- Read the response's body
                    body = response.read().decode('utf_8') #utf_8 to admit all characters in the response

                    limit_list = [] #list to save all species within the limit
                    body = json.loads(body) #loads is a json method to read json response
                    limit = body["species"] #json.loads(species)

                    if index > len(limit):   #if there are more species than the limit
                        contents = f"""<!DOCTYPE html>
                                                    <html lang = "en">
                                                    <head>
                                                     <meta charset = "utf-8" >
                                                     <title>ERROR</title >
                                                    </head>
                                                    <body  style="background-color:rgb(255,255,182)">
                                                    <p>ERROR LIMIT OUT OF RANGE</p>
                                                    <p> Introduce a valid limit</p>
                                                    <a href="/">Main page</a></body></html>"""
                    else:
                        for element in limit:  #iteration to get all the species within the limit
                            limit_list.append(element["display_name"])   #appends each element to the list

                            if len(limit_list) == index:
                                contents += f"""<p>The species are: </p>"""
                                for specie in limit_list:   #iteration to print all the species in the limit list
                                    contents += f"""<p> - {specie} </p>"""
                        contents += f"""<a href="/">Main page</a></body></html>""" #link to return to main page




            # --------------------------------------------karyotype--------------------------------------------

            elif first_argument == '/karyotype': #part3, returns the names of the cromosomes of the chosen species

                contents = f"""<!DOCTYPE html>
                                <html lang = "en">
                                <head>
                                    <meta charset = "utf-8">
                                     <title> Karyotype </title >
                                </head >
                                <body  style="background-color:rgb(255,255,182)">
                                <h2 style="color:rgb(21,105,150);"> The names of the chromosomes are:</h2>"""

                try:
                    # Get the arguments after the ?
                    get_value = arguments[1]

                    # We get the seq index and name
                    specie = get_value.split('?')  # splits by the ?
                    specie_method, name_sp = specie[0].split("=")  # splits by the =

                    full_name = "" #we initialize the variable to keep doble or more word names
                    for n in range(0, len(name_sp)): #we iterate to inlude all the characters of the entire name (all words combined with +)
                            if name_sp[n] == "+": #when we get a + we create a space with "%20" in the url to be able to search it in the database as a 2 (or more) word species
                                full_name += "%20"
                            else:
                                full_name += name_sp[n] #in case its a one word species


                    endpoint = 'info/assembly/'  #stablishes the endpoint and its parameters for the request
                    parameters = '?content-type=application/json'
                    request = endpoint + full_name + parameters

                    try:
                        conn.request("GET", request) #connection request

                    except ConnectionRefusedError: #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()

                    # ----------------------Main program of karyotype------------------------
                    # -- Read the response message from the server
                    response = conn.getresponse()

                    # -- Read the response's body
                    body = response.read().decode("utf-8") #utf_8 to admit all characters in the response
                    body = json.loads(body) #loads is a json method to read json response
                    karyotype_data = body["karyotype"] #list to save all the names


                    for chromosome in karyotype_data: #iteration to print all the chromosomes names
                        contents += f"""<p> - {chromosome} </p>"""

                    contents += f"""<a href="/">Main page </a></body></html>"""  # link to return to main page

                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = f"""<!DOCTYPE html> 
                                    <html lang="en"> 
                                        <head>
                                            <meta charset="UTF-8">
                                            <title>Error</title>
                                        </head>
                                        <body style="background-color:rgb(255,255,182)">
                                            <h1>ERROR</h1>
                                            <p> Selected specie's karyotype information is not available </p>
                                            <p><a href="/Karyotype?Specie={full_name}">Check if your specie is in our database</a><br><br>
                                            <p> Introduce a specie in the database to find its karyotype </p>
                                            <a href="/"> Main page </a> </p>
                                            </body>
                                            </html>"""

            # --------------------------------------------Cromosome length--------------------------------------------

            elif first_argument == "/chromosomeLength": #part4, Return the Length of the chromosome named "chromo" of the given specie

                try:
                    # We get the arguments that go after the ?, it will get us the SPECIE&CHROMOSOME
                    pair = arguments[1]

                    # We have to separate both the species name and the chromo index inputed
                    pairs = pair.split('&')  #splits by the &
                    specie_name, specie = pairs[0].split("=") #having pair[0] as the species name

                    chromosome_index, chromosome = pairs[1].split("=") #having pair[1] as the species name

                    #html form for when no chromosome index is inputed
                    contents = f"""<!DOCTYPE html>
                                <html lang = "en">
                                <head>
                                 <meta charset = "utf-8" >
                                 <title>ERROR</title >
                                </head>
                                <body  style="background-color:rgb(255,255,182)">
                                <p>ERROR INVALID VALUE</p>
                                <p> Introduce a valid integer value for chromosome of this species</p>
                                <a href="/">Main page</a></body></html>"""

                    full_name = ""  # we initialize the variable to keep doble or more word names
                    for n in range(0, len(specie)):  # we iterate to inlude all the characters of the entire name (all words combined with +)
                        if specie[n] == "+":  # when we get a + we create a space with "%20" in the url to be able to search it in the database as a 2 (or more) word species
                            full_name += "%20"
                        else:
                            full_name += specie[n]  # in case its a one word species

                    endpoint = 'info/assembly/'  # stablishes the endpoint and its parameters for the request
                    parameters = '?content-type=application/json'
                    request = endpoint + full_name + parameters

                    try:
                        conn.request("GET", request)  #connection request
                    except ConnectionRefusedError: #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()

                    # ----------------------Main program of chromosome length------------------------
                    # -- Read the response message from the server
                    response = conn.getresponse()

                    # -- Read the response's body
                    body = response.read().decode('utf-8')#utf_8 to admit all characters in the response
                    body = json.loads(body) #loads is a json method to read json response

                    chromosome_data = body["top_level_region"] #list to save all the chromosomes
                    specie = specie.replace("+", " ") #to print it with a space between both words (in double word species)
                    for chromo in chromosome_data: #iteration to get all the chromosomes within the list of data

                        if chromo["name"] == str(chromosome):
                            length = chromo["length"]
                            contents = f"""<!DOCTYPE html><html lang = "en"><head><meta charset = "utf-8" ><title> Length Chromosome</title >
                                            </head ><body  style="background-color:rgb(255,255,182)"><h2 style="color:rgb(21,105,150);"> The length of the '{chromosome}' {specie} chromosome is: {length}</h2><a href="/"> Main page</a"""
                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = f"""<!DOCTYPE html> 
                                                    <html lang="en"> 
                                                        <head>
                                                            <meta charset="UTF-8">
                                                            <title>Error</title>
                                                        </head>
                                                        <body style="background-color:rgb(255,255,182)">
                                                            <h1>ERROR</h1>
                                                            <p> Selected specie's cromosome length information is not available </p>
                                                            <p> Introduce a specie in the database (with a proper chromosome) to find its length information </p>
                                                            <p><a href="/Karyotype?Specie={full_name}">Check if your specie is in our database</a><br><br>
                                                            <a href="/"> Main page </a> </p>
                                                            </body>
                                                            </html>"""

            # --------------------------------------------gene Seq--------------------------------------------

            elif first_argument == "/geneSeq": #Return the sequence of a given human gene

                contents = f"""<!DOCTYPE html>
                            <html lang = "en">            
                            <head>  
                            <meta charset = "utf-8">
                            <title> Gene Sequence </title>
                            </head>
                            <body  style="background-color:rgb(255,255,182)">
                                <h1 style="color:rgb(225, 141, 27)"> Gene Sequence</h1>"""

                try:
                    # We get the arguments that go after the ?
                    get_value = arguments[1]

                    # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                    # position of the sequence
                    seq_n = get_value.split('?') #splits the argument by the ?
                    seq_name, name_seq = seq_n[0].split("=")   # #splits by the = --> name of the gene inputed

                    contents += f"""<p style="color:rgb(225, 141, 27)"> The sequence of gene {name_seq} is:  </p>""" #html to print the gene name

                    first_endpoint = "xrefs/symbol/homo_sapiens/"   #first endpoint = homosapiens --> human gene
                    parameters = '?content-type=application/json'
                    first_request = first_endpoint + name_seq + parameters

                    try:
                        conn.request("GET", first_request) #connection request

                    except ConnectionRefusedError: #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()

                    # ----------------------Main program of geneSeq------------------------

                    # -- Read the response message from the server
                    response = conn.getresponse()
                    # -- Read the response's body
                    body = response.read().decode()
                    body = json.loads(body) #loads is a json method to read json response

                    id_gene = body[0] #to get the id of the gene (first column of body) #json.loads(id)
                    id_gene = id_gene["id"]

                    second_endpoint = "sequence/id/" #to get specifically the sequence of the gene we id'd
                    second_request = second_endpoint + id_gene + parameters

                    try:
                        conn.request("GET", second_request)#connection request

                    except ConnectionRefusedError: #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()

                    # -- Read the second response message from the server
                    second_response = conn.getresponse()

                    # -- Read the second response's body
                    second_body = second_response.read().decode("utf-8")
                    second_body = json.loads(second_body) #loads is a json method to read json response

                    sequence = second_body["seq"] #gene sequence asked
                    contents += f"""<p>{sequence}</p><a href="/">Main page</a></body></html>"""  #print the sequence on screen

                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = """<!DOCTYPE html> 
                                      <html lang="en"> 
                                            <head>
                                                <meta charset="UTF-8">
                                                <title>Error</title>
                                            </head>
                                            <body style="background-color:rgb(255,255,182)">
                                                <h1>ERROR</h1>
                                                <p> Selected specie's gene sequence information is not available </p>
                                                <p> Introduce a valid human gene to find its sequence information </p>
                                                <a href="/"> Main page </a> </p>
                                                </body>
                                      </html>"""

            # --------------------------------------------gene Info-------------------------------------------

            elif first_argument == "/geneInfo": #Return information about a human gene: start, end, Length, id and Chromose

                contents = f"""<!DOCTYPE html>
                                <html lang = "en">     
                                <head>
                                    <meta charset = "utf-8" >
                                    <title>Gene Information</title>
                                </head>
                                 <body  style="background-color:rgb(255,255,182)">"""

                try:
                    # We get the arguments that go after the ?
                    get_value = arguments[1]

                    # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                    # position of the sequence
                    seq_n = get_value.split('?') #splits the argument by the ?
                    seq_name, name_seq = seq_n[0].split("=") # #splits by the = --> name of the gene inputed

                    contents += f"""<p style="color:rgb(225, 141, 27)"> Information of gene {name_seq} is:  </p>"""  #html to print the gene name

                    first_endpoint = "xrefs/symbol/homo_sapiens/" #first endpoint = homosapiens --> human gene
                    parameters = '?content-type=application/json'
                    first_request = first_endpoint + name_seq + parameters

                    try:
                        conn.request("GET", first_request) #connection request
                    except ConnectionRefusedError:
                        print("ERROR! Cannot connect to the Server") #exception for connection error
                        exit()

                    # ----------------------Main program of geneInfo------------------------

                    # -- Read the response message from the server
                    response = conn.getresponse()

                    # -- Read the response's body
                    body = response.read().decode()
                    body = json.loads(body) #loads is a json method to read json response

                    id_gene = body[0] #to get the id of the gene (first column of body) #json.loads(id)
                    id_gene = id_gene["id"]

                    second_endpoint = "lookup/id/" #to get specifically the info of the sequence of the gene we id'd
                    second_request = second_endpoint + id_gene + parameters

                    try:
                        conn.request("GET", second_request) #connection request

                    except ConnectionRefusedError: #exception for connection error
                        print("ERROR! Cannot connect to the Server")
                        exit()

                    # -- Read the second response message from the server
                    second_response = conn.getresponse()
                    # -- Read the response's body
                    second_body = second_response.read().decode()
                    second_body = json.loads(second_body ) #loads is a json method to read json response

                    length = int(second_body ["end"]) - int(second_body ["start"]) #measure the length of the gene

                    #prints the data of the starting point, end, length, region name and gene id
                    contents += f"""<p> -Starts at: {second_body ["start"]} </p><p> -Ends at: {second_body ["end"]} </p>
                                <p> -Length is: {length}</p>
                                <p> -ID is at: {id_gene} </p> <p> Located in chromosome: {second_body ["seq_region_name"]} </p>
                                <a href="/">Main page</a></body></html>"""

                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = """<!DOCTYPE html> 
                                                <html lang="en"> 
                                                      <head>
                                                          <meta charset="UTF-8">
                                                          <title>Error</title>
                                                      </head>
                                                      <body style="background-color:rgb(255,255,182)">
                                                          <h1>ERROR</h1>
                                                          <p> Selected specie's gene information is not available </p>
                                                          <p> Introduce a valid human gene to find its information </p>
                                                          <a href="/"> Main page </a> </p>
                                                          </body>
                                                </html>"""

            # --------------------------------------------gene Calc--------------------------------------------

            elif first_argument == "/geneCalc": #Return the names of the genes located in the chromosome "chromo" from the start to end positions

                contents = f"""<!DOCTYPE html>
                                    <html lang = "en">            
                                    <head>  
                                    <meta charset = "utf-8">
                                    <title> Gene Calculations</title>
                                    </head>
                                        <body  style="background-color:rgb(255,255,182)">
                                        <h1 style="color:rgb(225, 141, 27)">Gene calculations</h1>"""
                try:
                    # We get the arguments that go after the ?
                    get_value = arguments[1]

                    # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                    # position of the sequence
                    seq_n = get_value.split('?') #splits the argument by the ?
                    seq_name, name_seq = seq_n[0].split("=") #splits by the = --> name of the gene inputed

                    first_endpoint = "xrefs/symbol/homo_sapiens/"  #first endpoint = homosapiens --> human gene
                    parameters = '?content-type=application/json'
                    first_request = first_endpoint + name_seq + parameters

                    try:
                        conn.request("GET", first_request) #connection request

                    except ConnectionRefusedError:
                        print("ERROR! Cannot connect to the Server") #exception for connection error
                        exit()

                    # ----------------------Main program of geneCalc------------------------

                    # -- Read the response message from the server
                    response = conn.getresponse()

                    # -- Read the response's body
                    body = response.read().decode('utf-8')
                    body = json.loads(body) #loads is a json method to read json response


                    id_gene = body[0] #to get the id of the gene (first column of body) #json.loads(id)
                    id_gene = id_gene["id"]

                    second_endpoint = "sequence/id/" #to get specifically the info of the sequence of the gene we id'd
                    second_request = second_endpoint + id_gene + parameters

                    try:
                        conn.request("GET", second_request) #connection request

                    except ConnectionRefusedError:
                        print("ERROR! Cannot connect to the Server") #exception for connection error
                        exit()

                    # -- Read the second response message from the server
                    second_response = conn.getresponse()

                    # -- Read the second response's body
                    second_body = second_response.read().decode()
                    second_body = json.loads(second_body)

                    sequence = Seq(second_body["seq"]) #gets the sequence of the gene

                    contents += f"""<p> The length of gene {name_seq} is: {sequence.len()} </p>"""

                    list_of_bases = ["A", "C", "G", "T"]

                    for base in list_of_bases:
                        perc_base = round(sequence.count_base(base) * 100 / sequence.len(), 2)
                        contents += f"""<p> {base} : {sequence.count_base(base)} ({perc_base}%) </p>"""
                    contents += f"""<a href="/">Main page</a></body></html>"""

                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = """<!DOCTYPE html> 
                                                <html lang="en"> 
                                                      <head>
                                                          <meta charset="UTF-8">
                                                          <title>Error</title>
                                                      </head>
                                                      <body style="background-color:rgb(255,255,182)">
                                                          <h1>ERROR</h1>
                                                          <p> Selected specie's gene calculations information is not available </p>
                                                          <p> Introduce a valid human gene to find its calculations information </p>
                                                          <a href="/"> Main page </a> </p>
                                                          </body>
                                                </html>"""


            # --------------------------------------------gene geneList--------------------------------------------

            elif first_argument == "/geneList": #Return the names of the genes located in the chromosome "chromo" from the start to end positions

                contents = f"""<!DOCTYPE html>
                              <html lang = "en">            
                              <head>  
                              <meta charset = "utf-8">
                              <title> Gene List</title>
                              </head>
                              <body  style="background-color:rgb(255,255,182)">
                              <h1 style="color:rgb(225, 141, 27)">Gene List</h1>"""

                try:
                    # We get the arguments that go after the ?
                    get_value = arguments[1]

                    # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                    # position of the sequence
                    pairs = get_value.split('&') #splits by the &
                    chromo_value, chromo = pairs[0].split("=")  #having pair[0] as the species name
                    chromosome_start, start = pairs[1].split("=") #chromosome start (pair[1] column)
                    chromosome_end, end = pairs[2].split("=")  #chromosome end (pair[2] column)

                    contents += f"""<p style="color:rgb(225, 141, 27)"> List of genes of the chromosome {chromo}, which goes from {start} to {end}: </p>"""

                    endpoint = "overlap/region/human/"  # first endpoint --> human
                    parameters = '?feature=gene;content-type=application/json'
                    request = endpoint + chromo + ":" + start + "-" + end + parameters #request line

                    try:
                        conn.request("GET", request)#connection request

                    except ConnectionRefusedError:
                        print("ERROR! Cannot connect to the Server") #exception for connection error
                        exit()

                    # ----------------------Main program of geneList------------------------
                    # -- Read the response message from the server
                    response = conn.getresponse()
                    # -- Read the response's body
                    body = response.read().decode("utf-8") #utf_8 to admit all characters in the response
                    body = json.loads(body)

                    for element in body: #iteration to print all the elements of the chromosome within the chosen limits
                        print(element["external_name"])
                        contents += f"""<p>{element["external_name"]}</p>"""
                    contents += f"""<a href="/">Main page</a></body></html>"""

                except KeyError: #exception in case no value or an incorrect format value is inputed
                    contents = """<!DOCTYPE html> 
                                                    <html lang="en"> 
                                                          <head>
                                                              <meta charset="UTF-8">
                                                              <title>Error</title>
                                                          </head>
                                                          <body style="background-color:rgb(255,255,182)">
                                                              <h1>ERROR</h1>
                                                              <p> Selected specie's gene interval sequence information is not available </p>
                                                              <p> Introduce a valid human gene to find its interval sequence information </p>
                                                              <a href="/"> Main page </a> </p>
                                                              </body>
                                                    </html>"""



     # Open the form1.html file
            # Read the index from th

            # Define the content-type header:
            if 'json=1' in req_line:
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(str.encode(contents)))

            else:
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', len(str.encode(contents)))

            # The header is finished
            self.end_headers()

            # Send the response message
            self.wfile.write(str.encode(contents))

            return


        except (KeyError, ValueError, IndexError, TypeError):
            contents = Path('error.html').read_text()


# ------------------------
# - Server MAIN program (taken from previous practices)
# ------------------------
# -- Set the new handler
Handler = TestHandler

# -- Open the socket server
with socketserver.TCPServer(("", PORT), Handler) as httpd:

    print("Serving at PORT", PORT)

    # -- Main loop: Attend the client. Whenever there is a new
    # -- clint, the handler is called
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("")
        print("Stoped by the user")
        httpd.server_close()