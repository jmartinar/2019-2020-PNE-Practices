import http.client
import json
from termcolor import *

list_genes = ['FRAT1', 'ADA', 'FXN', 'RNU6_269P', 'MIR633', 'TTTY4C', 'RBMY2YP', 'FGFR3', 'KDR', 'ANK2']
list_identifiers = ['ENSG00000165879', 'ENSG00000196839', 'ENSG00000165060', 'ENSG00000212379', 'ENSG00000207552', 'ENSG00000228296', 'ENSG00000227633', 'ENSG00000068078', 'ENSG00000128052', 'ENSG00000145362']
dict_genes = dict(zip(list_genes, list_identifiers))

SERVER = 'rest.ensembl.org'
ENDPOINT = '/sequence/id/'
PARAMS ='ENSG00000207552?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS
IDENTIFIER = "ENSG00000207552"

print()
print(f"Server: {SERVER}")
print(f"URL: {URL}")

conn = http.client.HTTPConnection(SERVER)

try:
    conn.request("GET", ENDPOINT + PARAMS)

except ConnectionRefusedError:
    print("ERROR!!! We weren't able to conncet to the server :(")

resp1 = conn.getresponse()

print(f"Response received!: {resp1.status} {resp1.reason}")

data_ = resp1.read().decode("utf-8")

api_info = json.loads(data_)
colored_gene = colored("Gene", 'green')

for i,e in dict_genes.items():
    if e == IDENTIFIER:
        print(f"{colored_gene}: {i}")

colored_desc = colored("Description", 'green')
print(f"{colored_desc}: {api_info['desc']}")

colored_seq = colored("Bases", "green")
print(f"{colored_seq}: {api_info['seq']}")