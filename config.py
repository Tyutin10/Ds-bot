import json

class Config:
    def __init__(self):
        self._data = {}
    
    def get_config(self, config_path: str) -> None:
        with open(config_path, 'r', encoding='utf-8') as file:
            self._data = json.load(file)
            for key, value in self._data.items():
                setattr(self, key, value)
    