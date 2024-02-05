import argparse
import pdfplumber
import json


class AppConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as config_file:
            self.data = json.load(config_file)

    def get_files(self):
        return self.data.get("files", [])

    def get_rules(self):
        return self.data.get("rules", [])

    def __str__(self):
        return f"AppConfig(config_path={self.config_path}) \nFiles: {self.get_files()}\nRules: {self.get_rules()}"


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

    def _get_pdf_files(self):
        return self.app_config.get("files", [])

    def run(self):
        files = self._get_pdf_files()
        for file in files:
            self._process_pdf(file.get("pdf_file"), file.get("pdf_password"))

    def _process_pdf(self, pdf_file, pdf_password=None):
        with pdfplumber.open(pdf_file, password=pdf_password) as pdf:
            first_page = (
                pdf.pages[0].extract_text_simple(x_tolerance=3, y_tolerance=3)
                if pdf.pages
                else None
            )
            is_known, label = self._is_known_pdf(first_page)
            if is_known:
                print(f"{pdf_file} is a known pdf {label}")
            else:
                print(f"{pdf_file} is an unknown pdf")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()

    app = Peap(AppConfig(args.config))
    app.run()
