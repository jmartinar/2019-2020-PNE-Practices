import http.server
import http.client
import socketserver
from pathlib import Path
import json
from Seq1 import Seq
# Port
PORT = 8080
# -- This is for preventing the error: "Port already in use"
socketserver.TCPServer.allow_reuse_address = True
# Class with our Handler. It is a called derived from BaseHTTPRequestHandler
# It means that our class inheritates all his methods and properties
server = 'rest.ensembl.org'
parameters = '?content-type=application/json'


class TestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """This method
        is called whenever the client invokes the GET method
        in the HTTP protocol request"""
        print(self.requestline)
        # We get the first request line and then the path, goes after /. We get the arguments that go after the ? symbol
        req_line = self.requestline.split(' ')
        path = req_line[1]
        arguments = path.split('?')
        # Action is the first argument
        action = arguments[0]
        contents = Path('error.html').read_text()
        code = 200
        # First we open index.html if we don´t specify any action, this is the Index menu
        try:
            if action == "/":
                contents = Path('index.html').read_text()

            elif action == "/listSpecies":
                contents = f"""<!DOCTYPE html>
                <html lang = "en">
                <head>
                 <meta charset = "utf-8" >
                 <title>List of species in the browser</title >
                </head >
                <body>
                <p>The total number of species in ensembl is: 267</p>"""
                # We get the arguments that go after the ? symbol
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, index = seq_n[0].split("=")
                index = int(index)
                contents += f"""<p>The number of species you selected are: {index} </p>"""
                server = 'rest.ensembl.org'
                endpoint = 'info/species'
                parameters = '?content-type=application/json'
                conn = http.client.HTTPConnection(server)
                request = endpoint + parameters
                try:
                    conn.request("GET", request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                # -- Read the response message from the server
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode()
                limit_list = []
                body = json.loads(body)
                limit = body["species"]
                if index > len(limit):
                    contents = f"""<!DOCTYPE html>
                            <html lang = "en">
                            <head>
                             <meta charset = "utf-8" >
                             <title>ERROR</title >
                            </head>
                            <body>
                            <p>ERROR LIMIT OUT OF RANGE. Introduce a valid limit value</p>
                            <a href="/">Main page</a></body></html>"""
                else:
                    for element in limit:
                        limit_list.append(element["display_name"])
                        if len(limit_list) == index:
                            contents += f"""<p>The species are: </p>"""
                            for specie in limit_list:
                                contents += f"""<p> - {specie} </p>"""
                    contents += f"""<a href="/">Main page</a></body></html>"""

            elif action == "/karyotype":
                contents = f"""<!DOCTYPE html>
                <html lang = "en">
                <head>
                    <meta charset = "utf-8">
                     <title> Karyotype </title >
                </head >
                <body>
                <h2> The names of the chromosomes are:</h2>"""
                # We get the arguments that go after the ? symbol
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, name_sp = seq_n[0].split("=")
                server = 'rest.ensembl.org'
                endpoint = 'info/assembly/'
                parameters = '?content-type=application/json'
                conn = http.client.HTTPConnection(server)
                request = endpoint + name_sp + parameters
                try:
                    conn.request("GET", request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                # -- Read the response message from the server
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode("utf-8")
                karyotype_data = body["karyotype"]
                for chromosome in karyotype_data:
                    contents += f"""<p> - {chromosome} </p>"""
                    contents += f"""<a href="/">Main page </a></body></html>"""


            elif action == "/chromosomeLength":
                # We get the arguments that go after the ? symbol
                pair = arguments[1]
                # We have a couple of elements, we need the sequence that we previously wrote and the operation to perform
                # that we previously selected
                pairs = pair.split('&')
                specie_name, specie = pairs[0].split("=")
                chromosome_index, chromosome = pairs[1].split("=")
                specie = specie
                contents = f"""<!DOCTYPE html>
                <html lang = "en">
                <head>
                 <meta charset = "utf-8" >
                 <title>ERROR</title >
                </head>
                <body>
                <p>ERROR INVALID VALUE. Introduce an integer value for chromosome</p>
                <a href="/">Main page</a></body></html>"""
                server = 'rest.ensembl.org'
                endpoint = 'info/assembly/'
                parameters = '?content-type=application/json'
                conn = http.client.HTTPConnection(server)
                request = endpoint + specie + parameters
                try:
                    conn.request("GET", request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                # -- Read the response message from the server
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode()
                body = json.loads(body)
                chromosome_data = body["top_level_region"]
                for chromo in chromosome_data:
                    if chromo["name"] == str(chromosome):
                        length = chromo["length"]
                        contents = f"""<!DOCTYPE html><html lang = "en"><head><meta charset = "utf-8" ><title> Length Chromosome</title >
                            </head ><body><h2> The length of the chromosome is: {length}</h2><a href="/"> Main page</a"""
            elif action == "/geneSeq":
                contents= f"""<!DOCTYPE html>
                <html lang = "en">            
                <head>  
                <meta charset = "utf-8"
                <title> Gene Sequence </title>
                </head>"""
                # We get the arguments that go after the ? symbol
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, name_seq = seq_n[0].split("=")
                contents += f"""<p> The sequence of gene {name_seq} is:  </p>"""
                server = 'rest.ensembl.org'
                first_endpoint = "xrefs/symbol/homo_sapiens/"
                parameters = '?content-type=application/json'
                first_request = first_endpoint + name_seq + parameters
                conn = http.client.HTTPConnection(server)
                try:
                    conn.request("GET", first_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode()
                body = json.loads(body)
                id_gene = body[0]
                id_gene = id_gene["id"]

                second_endpoint = "sequence/id/"
                second_request = second_endpoint + id_gene + parameters
                try:
                    conn.request("GET", second_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response2 = conn.getresponse()
                # -- Read the response's body
                body2 = response2.read().decode()
                body2 = json.loads(body2)
                sequence = body2["seq"]
                contents += f"""<p>{sequence}</p><a href="/">Main page</a></body></html>"""
            elif action == "/geneInfo":
                contents = f"""<!DOCTYPE html>
                    <html lang = "en">            
                    <head>  
                    <meta charset = "utf-8"
                    <title> Gene Information</title>
                    </head>"""
                # We get the arguments that go after the ? symbol
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, name_seq = seq_n[0].split("=")
                contents += f"""<p> The information of gene {name_seq} is:  </p>"""
                server = 'rest.ensembl.org'
                first_endpoint = "xrefs/symbol/homo_sapiens/"
                parameters = '?content-type=application/json'
                first_request = first_endpoint + name_seq + parameters
                conn = http.client.HTTPConnection(server)
                try:
                    conn.request("GET", first_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode()
                body = json.loads(body)
                id_gene = body[0]
                id_gene = id_gene["id"]
                second_endpoint = "lookup/id/"
                second_request = second_endpoint + id_gene + parameters
                try:
                    conn.request("GET", second_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response2 = conn.getresponse()
                # -- Read the response's body
                body2 = response2.read().decode()
                body2 = json.loads(body2)
                length = int(body2["end"]) - int(body2["start"])
                contents += f"""<p> The gene starts at: {body2["start"]} </p><p> The gene ends at: {body2["end"]} </p>
                <p> The gene length is: {length}</p>
                <p> The gene id is at: {id_gene} </p> <p> The gene is on chromosome: {body2["seq_region_name"]} </p>
                <a href="/">Main page</a></body></html>"""
            elif action == "/geneCalc":
                contents = f"""<!DOCTYPE html>
                        <html lang = "en">            
                        <head>  
                        <meta charset = "utf-8"
                        <title> Gene Calculations</title>
                        </head>"""
                # We get the arguments that go after the ? symbol
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                seq_n = get_value.split('?')
                seq_name, name_seq = seq_n[0].split("=")
                server = 'rest.ensembl.org'
                first_endpoint = "xrefs/symbol/homo_sapiens/"
                parameters = '?content-type=application/json'
                first_request = first_endpoint + name_seq + parameters
                conn = http.client.HTTPConnection(server)
                try:
                    conn.request("GET", first_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode()
                body = json.loads(body)
                id_gene = body[0]
                id_gene = id_gene["id"]
                second_endpoint = "sequence/id/"
                second_request = second_endpoint + id_gene + parameters
                try:
                    conn.request("GET", second_request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response2 = conn.getresponse()
                # -- Read the response's body
                body2 = response2.read().decode()
                body2 = json.loads(body2)
                sequence = Seq(body2["seq"])
                contents += f"""<p> The length of gene {name_seq} is: {sequence.len()} </p>"""
                list_of_bases = ["A", "C", "G", "T"]
                for base in list_of_bases:
                    perc_base = round(sequence.count_base(base) * 100 / sequence.len(),2)
                    contents += f"""<p> {base} : {sequence.count_base(base)} ({perc_base}%) </p>"""
                contents += f"""<a href="/">Main page</a></body></html>"""

            elif action == "/geneList":
                contents = f"""<!DOCTYPE html>
                  <html lang = "en">            
                  <head>  
                  <meta charset = "utf-8"
                  <title> Gene List</title>
                  </head>"""
                endpoint = "overlap/region/human/"
                get_value = arguments[1]
                # We get the seq index, after we have a couple of elements, the one which we need is the value of the index
                # position of the sequence
                pairs = get_value.split('&')
                chromo_value, chromo = pairs[0].split("=")
                chromosome_start, start = pairs[1].split("=")
                chromosome_end, end = pairs[2].split("=")
                contents += f"""<p> List of genes of the chromosome {chromo}, which goes from {start} to {end} </p>"""
                server = 'rest.ensembl.org'
                parameters = '?feature=gene;content-type=application/json'
                request = endpoint + chromo + ":" + start + "-" + end + parameters

                conn = http.client.HTTPConnection(server)
                try:
                    conn.request("GET", request)
                except ConnectionRefusedError:
                    print("ERROR! Cannot connect to the Server")
                    exit()
                response = conn.getresponse()
                # -- Read the response's body
                body = response.read().decode("utf-8")
                body = json.loads(body)
                for element in body:
                    print(element["external_name"])
                    contents += f"""<p>{element["external_name"]}</p>"""
                contents += f"""<a href="/">Main page</a></body></html>"""





#97321915  97319271

        except (KeyError,ValueError,IndexError,TypeError):
            contents = Path('error.html').read_text()


        # Generating the response message
        self.send_response(code)  # -- Status line: OK!

        # Define the content-type header:
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', len(str.encode(contents)))

        # The header is finished
        self.end_headers()

        # Send the response message
        self.wfile.write(str.encode(contents))

        return


# ------------------------
# - Server MAIN program
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