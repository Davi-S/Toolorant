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
    map_agent: dict[gr.Map, gr.Agent | None]

    @classmethod
    def load(cls, profile_name: str):
        with open(PROFILES_PATH.joinpath(f'{profile_name}.json'), 'r') as f:
            data = json.load(f)
        map_agent = {gr.Map[map.upper()]: (gr.Agent[agent.upper()] if agent is not None else None)
                     for map, agent
                     in data.items()}
        return cls(profile_name, map_agent)

    @classmethod
    def delete(cls, profile_name: str) -> None:
        os.remove(PROFILES_PATH.joinpath(f'{profile_name}.json'))

    def delete(self) -> None:
        os.remove(PROFILES_PATH.joinpath(f'{self.name}.json'))

    def add(self) -> None:
        data = {map.name: (agent.name if agent is not None else None)
                for map, agent in self.map_agent.items()}

        with open(PROFILES_PATH.joinpath(f'{self.name}.json'), 'w') as f:
            json.dump(data, f, indent=4)


def get_all_profiles():
    profiles_name = [file[:-5]
                     for file
                     in os.listdir(PROFILES_PATH)]
    return [Profile.load(profile_name) for profile_name in profiles_name]
