import argparse
import calendar
import datetime
import json
import re
from pypdf import PdfReader
import pdfplumber
from config import AppConfig


class Peap:
    def __init__(self, app_config):
        self.app_config = app_config
        self.dlq = {}

    def run(self):
        files = self.app_config.get_files()
        for file in files:
            self._process_pdf(file.get("pdf_file"), file.get("pdf_password"))

        print(f"{self.dlq}")

    def _process_pdf(self, pdf_file, pdf_password=None):
        reader = PdfReader(pdf_file)
        if reader.is_encrypted:
            reader.decrypt(pdf_password)
            
        page1 = reader.pages[0]
        is_known, label = self._is_known_pdf(page1.extract_text())
        if is_known and label == "TD Aeroplan Visa":
            print(f"{pdf_file} is a TD Aeroplan Visa document")
            for page in reader.pages:
                extracted_text = page.extract_text()
                print(extracted_text)
                match = re.search(
                    r"STATEMENT PERIOD: ([a-zA-Z]+) (\d+),(\d+)to([a-zA-Z]+)(\d+),(\d+)", 
                    extracted_text,
                )
                if match is not None:
                    is_roll_over = match[3] != match[6]
                    first_year = match[3]
                    last_year = match[6] if is_roll_over else match[3]
                    print(f"{extracted_text}")
                    rows = self._extract_standardised_rows(extracted_text, first_year, last_year)
                    self._appendToResults(rows)
                else:
                    self._dlq(pdf_file, "no statement period")
                
        elif is_known and label == "Pass The Keys":
            print(f"{pdf_file} is a PTK document")
        else:
            self._dlq(pdf_file)

    def _is_known_pdf(self, pdf_text):
        rules = self.app_config.get_rules()
        for rule in rules:
            pattern = rule.get("pattern", "")
            if pattern in pdf_text:
                return True, rule.get("label", "")

        return False, None

    def _dlq(self, pdf_file, issue="unknown"):
        print(f"{pdf_file} is in the DLQ")
        self.dlq[pdf_file] = {"issue": issue}

    def _extract_standardised_rows(self, raw_extracted_txt, first_year, last_year):
        pattern = r'^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC).*'
        transaction_rows = [line for line in raw_extracted_txt.splitlines() if re.match(pattern, line)]
        
        return [self._standardise(row, first_year, last_year) for row in transaction_rows]
    
    def _standardise(self, line, first_year, last_year):
        pattern = r'^(JAN).*'
        if re.match(pattern, line) is not None:
            items = line.split(" ")
            return self._format_line_with_date(items, last_year)
        else:
            items = line.split(" ")
            return self._format_line_with_date(items, first_year)
        
    def _format_line_with_date(self, items, year):
        return f"{self._format_date(items[0], year)} {self._format_date(items[1], year)} {items[2]} {items[3]}"
    
    def _format_date(self, date, year):
        index = list(calendar.month_abbr).index(date[:3].title())
        specific_date = datetime.date(int(year), index, int(date[3:]))
        return specific_date.strftime("%Y-%b-%d")

    def _appendToResults(self, rows):
        for row in rows:
            print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()

    app = Peap(AppConfig(args.config))
    app.run()


