import json

class AppConfig:
    __default = {
                "output": "results.csv",
                "delimiter": "|",
            }
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.data = {}
        if self.config_path:
            self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as config_file:
            self.data = json.load(config_file)

    def get_files(self):
        return self.data.get("files", [])

    def get_output(self):
        return self.data.get("output", self.__default.get("output"))

    def get_delimiter(self):
        return self.data.get("delimiter", self.__default.get("delimiter"))
