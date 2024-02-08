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

    def get_output(self):
        return self.data.get("output", "")
