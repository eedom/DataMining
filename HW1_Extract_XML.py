'''Instructions
In this assignment you are NOT allowed to use any external library to read the given XLSX file directly.
Instead, you should unzip the XLSX file and extract the following XML files: sharedStrings.xml and athletes.xml.
The shared strings file should be read first and be used to create a list of all strings referenced in the document.
You should then read athletes.xml and extract all of its rows. Note that the content of each cell maps to the index
in the shared string list. Finally, your parser should then saved the extracted information in json, using the format below:

[
    {"name": "AALERUD Katrine", "noc": "Norway", "discipline": "Cycling Road"},
    {"name": "ABAD Nestor", "noc": "Spain", "discipline": "Artistic Gymnastics"},
    {"name": "ABAGNALE Giovanni", "noc": "Italy", "discipline": "Rowing"},
    ...
]
Hint: use the "xml" parser from beautiful soup.'''

from bs4 import BeautifulSoup as bs
import lxml


def parse(filename):
    with open(filename, "r") as file:
        return bs(file.read(), "lxml")


strings = parse("sharedStrings.xml").find_all("t")

table = parse("sheet1.xml").find_all("row")


def lookup(what, string_table):
    index = int(what)
    if index < len(string_table):
        return string_table[index].text
    return "<not found>"


headers = []

output = "["

k = 1

for row in table:

    columns = row.find_all("v")

    if len(headers) == 0:

        for col in columns:
            headers.append(lookup(col.text, strings).lower())
    else:

        line = "\n\t{"

        i = 0

        for col in columns:

            header = headers[i]

            value = lookup(col.text, strings)

            line += ('"' + header + '": "' + value + '"')

            i += 1

            if i < len(columns):
                line += ", "

        line += "}"

        k += 1

        if k < len(table):
            line += ","

        output += line

output += "\n]"

with open("output.txt", "w") as file:
    file.write(output)
