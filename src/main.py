import argparse
import csv
import os

from config import AppConfig
from data_store import DataStore
from pypdf import PdfReader
from td import TD


class Peap:
    def __init__(self, ds: DataStore):
        self.ds = ds
        self.dlq = {}
        self.td = TD()

    def process_pdf(self, pdf_file, pdf_password=None):
        reader = PdfReader(pdf_file, password=pdf_password)

        page1 = reader.pages[0]
        if self.td.is_match(page1.extract_text()):
            self.td.process(pdf_file, reader, self.ds.write, self._dlq)
        else:
            self._dlq(pdf_file, "Unknown pdf type")    
            
        return self.ds.read()

    def _dlq(self, pdf_file, issue="unknown"):
        self.dlq[pdf_file] = {"issue": issue}
        return input_string[:5]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()
    config = AppConfig(args.config)
    app = Peap()
    files = config.get_files()

    for file in files:
        app.process_pdf(file.get("pdf_file"), file.get("pdf_password"))
