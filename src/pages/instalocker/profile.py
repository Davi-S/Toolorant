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
    map_agent: dict[gr.Map, gr.Agent | str]

    @classmethod
    def load(cls, profile_name: str):
        # Check for "None" to avoid raising errors
        if profile_name is None:
            return None
        with open(PROFILES_PATH.joinpath(f'{profile_name}.json'), 'r') as f:
            data: dict = json.load(f)
        map_agent = {gr.Map[map.upper()]: (gr.Agent[agent.upper()] 
                                           if agent not in ['NONE', 'DODGE']
                                           else agent)
                     for map, agent
                     in data.items()}
        return cls(profile_name, map_agent)

    def delete(self) -> None:
        os.remove(PROFILES_PATH.joinpath(f'{self.name}.json'))

    def save(self) -> None:
        data = {map.name: (agent.name
                           if agent not in ['NONE', 'DODGE']
                           else agent)
                for map, agent in self.map_agent.items()}

        with open(PROFILES_PATH.joinpath(f'{self.name}.json'), 'w') as f:
            json.dump(data, f, indent=4)


def get_all_profiles():
    profiles_name = get_all_profiles_name()
    return [Profile.load(profile_name) for profile_name in profiles_name]

def get_all_profiles_name():
    return [file[:-5] for file in os.listdir(PROFILES_PATH)]
     
def delete(profile_name: str) -> None:
    os.remove(PROFILES_PATH.joinpath(f'{profile_name}.json'))
