from pathlib import Path

# -- Constant with the new of the file to open
FILENAME = "ADA.txt"

# -- Open and read the file
file_contents = Path(FILENAME).read_text().split("\n")[1:]

# -- Print the contents on the console
file_contents_final = "".join(file_contents)

print(len(file_contents_final))