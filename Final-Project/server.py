import http.server
import socketserver
import termcolor
from pathlib import Path
from Seq1 import Seq
import json

# Define the Server's port
PORT = 8080
IP = "127.0.0.1"
bases = ['A', 'C', 'T', 'G']

SERVER_EN = 'rest.ensembl.org'
ALWAYS_PARAMS = '?content-type=application/json'
conn = http.client.HTTPConnection(SERVER_EN)

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

        req_line = self.requestline.split(' ') #splits it by the spaces

        arguments = (req_line[1]).split("?") #sWe get the first request line and then the path, goes after /. We get the arguments that go after the ?
        first_argument = arguments[0] #sets the first argument
        contents = Path('Error.html').read_text()
        self.send_response(404)

        try:
            if first_argument == "/":  #return an HTML page with the forms for accessing to all the previous services

                contents = Path('index.html').read_text()
                self.send_response(200)

            elif first_argument == '/listSpecies':
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