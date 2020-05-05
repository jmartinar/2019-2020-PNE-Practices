import http.client
import json

SERVER = 'rest.ensembl.org'
ENDPOINT = '/info/ping'
PARAMS ='?content-type=application/json'
URL = SERVER + ENDPOINT + PARAMS

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

PING = api_info['ping']

if PING == 1:
    print("PING OK! The data base is running")