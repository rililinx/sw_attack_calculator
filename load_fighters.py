import json
import os
from typing import List

class Character:
    def __init__(self, name, parry, toughness, attacks=None, fight=None, shooting=None):
        self.name = name
        self.parry = parry
        self.toughness = toughness
        self.attacks = attacks if attacks else {}
        self.Fight = fight
        self.Shooting = shooting

    @classmethod
    def from_json(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            return cls(data['name'], data['Parry'], data['Toughness'], data.get('Attacks'), data.get('Fight'), data.get('Shooting'))


def load_characters_from_folder(folder_path: str) -> List[Character]:
    characters = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            characters.append(Character.from_json(file_path))
    return characters