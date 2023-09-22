import dataclasses
import json
import os
from pathlib import Path

import game_resources as gr


PROFILES_PATH = Path(__file__).parent.joinpath('profiles/')
if not PROFILES_PATH.exists():
    os.makedirs(PROFILES_PATH)


@dataclasses.dataclass
class Profile:
    name: str
    game_mode: gr.GameMode
    map_agent: dict[gr.Map, gr.Agent | None]

    @classmethod
    def load(cls, profile_name: str):
        """Create a profile class from a profile file"""
        with open(PROFILES_PATH.joinpath(f'{profile_name}.json'), 'r') as f:
            data = json.load(f)

        game_mode = gr.GameMode[data['game_mode'].upper()]
        map_agent = {gr.Map[map.upper()]: (gr.Agent[agent.upper()] if agent is not None else None)
                     for map, agent
                     in data['map_agent'].items()}
        return cls(profile_name, game_mode, map_agent)

    @classmethod
    def delete(cls, profile_name: str) -> None:
        """Deletes the profile file with the given name"""
        os.remove(PROFILES_PATH.joinpath(f'{profile_name}.json'))
        
    def delete(self) -> None:
        """Deletes the profile file relative to the class"""
        os.remove(PROFILES_PATH.joinpath(f'{self.name}.json'))

    def add(self) -> None:
        """Creates a profile file with the class information"""
        game_data_dict = {
            'game_mode': self.game_mode.name,
            'map_agent': {map.name: (agent.name if agent is not None else None)
                          for map, agent in self.map_agent.items()}
        }
        with open(PROFILES_PATH.joinpath(f'{self.name}.json'), 'w') as f:
            json.dump(game_data_dict, f, indent=4)


def get_all_profiles():
    profiles_name = [file[:-5]
                     for file
                     in os.listdir(PROFILES_PATH)]
    return [Profile.load(profile_name) for profile_name in profiles_name]
