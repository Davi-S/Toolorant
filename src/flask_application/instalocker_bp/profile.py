import dataclasses
import json
import os
from .. import game_resources as ge

BASE_PROFILES_PATH = 'src/profiles/'  # os.path.join(os.getcwd(), 'profiles/')

# TODO: use toml instead of json


@dataclasses.dataclass
class Profile:
    name: str
    game_mode: ge.GameMode
    map_agent: dict[ge.Map, ge.Agent | None]

    @classmethod
    def load_profile(cls, profile_name: str):
        # Load JSON data from file
        with open(BASE_PROFILES_PATH + profile_name + '.json', 'r') as f:
            json_data = json.load(f)

        # Create instances of dataclasses using JSON data
        # Use Enum to get enum member
        game_mode = ge.GameMode[json_data['game_mode'].upper()]
        map_agent = {ge.Map[k.upper()]: (ge.Agent[v.upper()] if v is not None else None)
                     for k, v in json_data['map_agent'].items()}
        return cls(profile_name, game_mode, map_agent)

    def dump_profile(self) -> None:
        # Dump dataclass instances to JSON
        game_data_dict = {
            'game_mode': self.game_mode.name.title(),
            'map_agent': {k.name.title(): (v.name.title() if v is not None else None)
                          for k, v in self.map_agent.items()}
        }
        with open(BASE_PROFILES_PATH + self.name + '.json', 'w') as f:
            json.dump(game_data_dict, f, indent=4)

    def delete_profile(self) -> None:
        os.remove(f'{BASE_PROFILES_PATH}\\{self.name}.json')
