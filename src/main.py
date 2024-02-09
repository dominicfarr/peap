import argparse

from config import AppConfig
from pypdf import PdfReader
from td import TD


class Peap:
    def __init__(self, app_config):
        self.app_config = app_config
        self.dlq = {}
        self.results = []
        self.processor_map = {"TD": TD()}

    def run(self):
        files = self.app_config.get_files()

        for file in files:
            self._process_pdf(file.get("pdf_file"), file.get("pdf_password"))

        self._write_results()

        print(f"Process complete.\n\nResults appended to {self.app_config.get_output()}\n\nErrors: \n{self.dlq}")

    def _process_pdf(self, pdf_file, pdf_password=None):
        reader = PdfReader(pdf_file)

        if reader.is_encrypted:
            reader.decrypt(pdf_password)

        page1 = reader.pages[0]
        if class_name := self._is_known_pdf(page1.extract_text()):
            processor = self.processor_map.get(class_name)
            if processor is None:
                self._dlq(pdf_file, "unknown processor")
                return

            processor.process(pdf_file, reader, self.results.extend, self._dlq)
        else:
            self._dlq(pdf_file)

    def _is_known_pdf(self, pdf_text):
        rules = self.app_config.get_rules()
        for rule in rules:
            pattern = rule.get("pattern", "")
            if pattern in pdf_text:
                return rule.get("class", None)

        return None

    def _dlq(self, pdf_file, issue="unknown"):
        self.dlq[pdf_file] = {"issue": issue}

    def _write_results(self):
        with open(self.app_config.get_output(), "a") as file:
            for line in self.results:
                file.write(line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()

    app = Peap(AppConfig(args.config))
    app.run()
