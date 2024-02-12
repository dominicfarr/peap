import csv
import os
from abc import ABC, abstractmethod
from config import AppConfig


class DataStore(ABC):
    @abstractmethod
    def write(self, date, amount, description, category="Uncategorised"):
        pass

    @abstractmethod
    def read(self):
        pass


# Adapter (concrete implementation)
class FileSystemDataStore(DataStore):
    def __init__(self, app_config:AppConfig):
        self.output = app_config.get_output()
        self.delimiter = app_config.get_delimiter()
        # Check if the file exists
        file_exists = os.path.isfile(self.output)

        # If the file doesn't exist or is empty, add the header row
        if not file_exists or os.path.getsize(self.output) == 0:
            with open(self.output, "w", newline="") as csv_file:
                writer = csv.writer(csv_file, delimiter=self.delimiter)
                writer.writerow(["Date", "Amount", "Description", "Category"])

    def write(self, date, amount, description, category="Uncategorised"):
        with open(self.output, "a", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delimiter)
            writer.writerow(
                [
                    date,
                    amount,
                    description,
                    category,
                ]
            )

    def read(self):
        with open(self.output, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=self.delimiter)
            results = [row for row in csv_reader]
        return results
