import calendar
import re


class TD:
    def __init__(self):
        super(TD, self).__init__()
        self.statement_period = TD_Statement_Period()
        self.td_row_extractor = TD_Row_Extractor()

    def process(self, pdf_file, reader, results_hof, dlq_hof):
        # print(f"{pdf_file} is a TD Aeroplan Visa document")

        statement_period = self.statement_period.get_statement_period(
            reader.pages[0].extract_text()
        )

        if statement_period is not None:
            for page in reader.pages:
                extracted_text = page.extract_text()
                rows = self.td_row_extractor.extract(extracted_text, statement_period)
                results_hof(rows)
        else:
            dlq_hof(pdf_file, "no statement period")


class TD_Statement_Period:
    __statement_pattern = r"STATEMENT PERIOD: (.*)"
    __data_pattern = r"([A-Z][a-z]+)(\d{2}),(\d{4})to([A-Z][a-z]+)(\d{2}),(\d{4})"

    def __init__(self, *args, **kwargs):
        super(TD_Statement_Period, self).__init__(*args, **kwargs)

    def get_statement_period(self, lines):
        match = re.search(self.__statement_pattern, lines)

        if match is None:
            return None

        extract = match[1].strip().replace(" ", "")

        date_match = re.search(self.__data_pattern, extract)
        if date_match is None:
            return None

        start_date = f"{date_match[3]}-{date_match[1]}-{date_match[2]}"
        end_date = f"{date_match[6]}-{date_match[4]}-{date_match[5]}"

        return {
            "start": start_date,
            "end": end_date,
            "is_rollover": lambda: start_date[:4] != end_date[:4],
        }


class TD_Row_Extractor:
    __pattern = r"^(JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC).*"

    def __init__(self, *args, **kwargs):
        super(TD_Row_Extractor, self).__init__(*args, **kwargs)

    def extract(self, raw_extracted_txt, statement_period):
        transaction_rows = [
            line
            for line in raw_extracted_txt.splitlines()
            if re.match(self.__pattern, line)
        ]

        return [self._standardise(row, statement_period) for row in transaction_rows]

    def _standardise(self, line, statement_period):
        pattern = r"^(JAN).*"
        year = (
            statement_period.get("end")[:4]
            if statement_period["is_rollover"]() and re.match(pattern, line)
            else statement_period.get("start")[:4]
        )

        items = line.split(" ")
        if re.match(r"([A-Z]{3}\d+[A-Z]{3}\d+)", line) is not None:
            amount = line.split(' ')[1]
            desc = ' '.join(items[2:])
        else:
            amount = line.split(' ')[2]
            desc = ' '.join(items[3:])
            
        date = self._format_date(items[0], year)
        
        return " | ".join([date, amount, desc])             


    def _format_line_with_date(self, items, year, amount, desc):
        return f"{self._format_date(items[0], year)} | {amount} | {desc}"

    def _format_date(self, date, year):
        pattern = r"([a-zA-Z]+)(\d+)"

        match = re.search(pattern, date)
        index = str(list(calendar.month_abbr).index(match[1].title()))

        return f"{year}-{index.zfill(2)}-{match[2].zfill(2)}"
