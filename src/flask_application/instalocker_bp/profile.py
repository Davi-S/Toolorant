import dataclasses
import json
import os

from .. import game_resources as gr

BASE_PROFILES_PATH = 'src\\flask_application\\instalocker_bp\\profiles\\'


@dataclasses.dataclass
class Profile:
    name: str
    game_mode: gr.GameMode
    map_agent: dict[gr.Map, gr.Agent | None]

    @classmethod
    def load(cls, profile_name: str):
        # Load JSON data from file
        with open(BASE_PROFILES_PATH + profile_name + '.json', 'r') as f:
            json_data = json.load(f)

        # Create instances of dataclasses using JSON data
        # Use Enum to get enum member
        game_mode = gr.GameMode[json_data['game_mode'].upper()]
        map_agent = {gr.Map[k.upper()]: (gr.Agent[v.upper()] if v is not None else None)
                     for k, v in json_data['map_agent'].items()}
        return cls(profile_name, game_mode, map_agent)

    @classmethod
    def delete(cls, profile_name: str) -> None:
        os.remove(f'{BASE_PROFILES_PATH}\\{profile_name}.json')

    def dump(self) -> None:
        # Dump dataclass instances to JSON
        game_data_dict = {
            'game_mode': self.game_mode.name.title(),
            'map_agent': {k.name.title(): (v.name.title() if v is not None else None)
                          for k, v in self.map_agent.items()}
        }
        with open(BASE_PROFILES_PATH + self.name + '.json', 'w') as f:
            json.dump(game_data_dict, f, indent=4)


def get_all_profiles():
    profiles_name = [file[:-5] for file in os.listdir(f'{os.getcwd()}\\{BASE_PROFILES_PATH}')]
    return [Profile.load(profile_name) for profile_name in profiles_name]
