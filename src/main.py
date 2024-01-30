import pdfplumber
import json

with open('../config.json', 'r') as config_file:
    config = json.load(config_file)

with pdfplumber.open("./test/resources/test.pdf", password=config.get("pdf_password")) as pdf:
    first_page = pdf.pages[0]
    # print(first_page.chars[0])
    print(first_page.extract_text_simple(x_tolerance=3, y_tolerance=3))
