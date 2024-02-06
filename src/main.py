import argparse
import pdfplumber
import json
from config import AppConfig


class Peap:
    def __init__(self, app_config):
        self.app_config = app_config

    def _is_known_pdf(self, pdf_text):
        rules = self.app_config.get_rules()
        print(f"rules: {rules}")
        for item in rules:
            if item.get("pattern", "") in pdf_text:
                return True, item.get("label", "")

        return False, None

    def run(self):
        files = self.app_config.get_files()
        for file in files:
            self._process_pdf(file.get("pdf_file"), file.get("pdf_password"))

    def _process_pdf(self, pdf_file, pdf_password=None):
        response = ""
        with pdfplumber.open(pdf_file, password=pdf_password) as pdf:
            first_page = (
                pdf.pages[0].extract_text_simple(x_tolerance=3, y_tolerance=3)
                if pdf.pages
                else None
            )
            is_known, label = self._is_known_pdf(first_page)
            if is_known:
                print(f"{pdf_file} is a known pdf {label}")
                for page in pdf.pages:
                    page_text = page.extract_text_simple(x_tolerance=3, y_tolerance=3)
                    response += page_text

            else:
                print(f"{pdf_file} is an unknown pdf")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()

    app = Peap(AppConfig(args.config))
    app.run()
