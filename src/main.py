import argparse
import csv
import os

from config import AppConfig
from pypdf import PdfReader
from td import TD


class Peap:
    
    def __init__(self, app_config):
        self.app_config = app_config
        self.delimiter = self.app_config.get_delimiter()
        csv_path = self.app_config.get_output()
        self.dlq = {}
        self.results = []
        self.processor_map = {"TD": TD()}

        # Check if the file exists
        file_exists = os.path.isfile(csv_path)

        # If the file doesn't exist or is empty, add the header row
        if not file_exists or os.path.getsize(csv_path) == 0:
            with open(csv_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=self.delimiter)
                writer.writerow(["Date", "Amount", "Description", "Category"])


    def run(self):
        files = self.app_config.get_files()

        for file in files:
            self._process_pdf(file.get("pdf_file"), file.get("pdf_password"))

        print(
            f"Process complete.\n\nResults appended to {self.app_config.get_output()}\n\nErrors: \n{self.dlq}"
        )

    

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

            processor.process(self.delimiter, pdf_file, reader, self._write_row, self._dlq)
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

    def _write_row(self, date, amount, description, category = "Uncategorised"):
        with open(self.app_config.get_output(), "a", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delimiter)
            writer.writerow(
                [
                    date,
                    amount,
                    description,
                    category,
                ]
            )
                
    def _write_results(self):
        with open(self.app_config.get_output(), "a") as file:
            for line in self.results:
                file.write(line + "\n")

    def _categories(self, *args):
        # Read the existing CSV file into a list of dictionaries
        with open(self.app_config.get_output(), "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file,fieldnames=["Date", "Amount", "Description"], delimiter=self.delimiter)
            existing_data = [row for row in reader]
            
        # Define the header row
        header = ["Date", "Amount", "Description", "Category"]

        # Add the header row to the existing data
        # existing_data.insert(0, dict(zip(header, header)))

        # Write the updated data (including the header) back to the CSV file
        with open(self.app_config.get_output(), "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=self.delimiter)
            writer.writeheader()
            writer.writerows(existing_data)

        # Read the CSV file with extracted transactions
        with open(self.app_config.get_output(), "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.delimiter)
            transactions = [row for row in reader]
            
        # collect known transaction description
        known_transactions = {
            self.extract_first_part(transaction["Description"].strip()): ('UNCATEGORISED' if transaction["Category"] == '' else '')
            for transaction in transactions
        }
        
        for transaction in transactions:
            # Check if the current transaction description is known
            description = self.extract_first_part(transaction["Description"].strip())
            print(f"Transaction: {transaction['Description']} key: {description}")
            if description in known_transactions:
                known_category = known_transactions[description]
                
                user_input = input(f"This transaction is already categorized as '{known_category}'. Do you want to associate it with this category? (y/n): ")
                if user_input.lower() == 'n':
                    # Prompt the user to enter a different category
                    category = input("Enter a different category (press Enter to skip): ")
                    known_transactions[description] = category
                else:
                    # Use the known category for the current transaction
                    print(f"Associating transaction with category '{known_category}'")
                    transaction["Category"] = known_category
                    continue
            else:
                # Prompt the user to enter a new category
                category = input("Enter a category (press Enter to skip): ")

            if category:
                # Write the category to the CSV file
                with open(self.app_config.get_output(), "a", newline="") as csv_file:
                    writer = csv.writer(csv_file, delimiter=self.delimiter)
                    writer.writerow(
                        [
                            transaction["Date"],
                            transaction["Amount"],
                            transaction["Description"],
                            category,
                        ]
                    )

        print("Categorization completed.")
        
    def extract_first_part(self, input_string):
        return input_string[:5]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Peap")
    parser.add_argument("--config", required=True, help="Path to configuration file")
    args = parser.parse_args()

    app = Peap(AppConfig(args.config))
    app.run()
