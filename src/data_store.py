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


class FileSystemDataStore(DataStore):
    
    def __init__(self, app_config: AppConfig):
        self.store = []

    def write(self, date, amount, description, category="uncategorised"):
        self.store.append([date, amount, description, category])

    def read(self):
        return self.store
