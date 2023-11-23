import json
import os
from pathlib import Path

PROFILES_PATH = Path(__file__).parent.joinpath('s_profiles/')
if not PROFILES_PATH.exists():
    os.makedirs(PROFILES_PATH)


def get_all_s_profiles_name() -> list[str]:
    return [file[:-5] for file in os.listdir(PROFILES_PATH)]


def delete(s_profile_name: str) -> None:
    os.remove(PROFILES_PATH.joinpath(f'{s_profile_name}.json'))


def save(s_profile_name: str, s_profile_data: dict) -> None:
    with open(PROFILES_PATH.joinpath(f'{s_profile_name}.json'), 'w') as f:
        json.dump(s_profile_data, f, indent=4)


def load(s_profile_name: str) -> dict:
    with open(PROFILES_PATH.joinpath(f'{s_profile_name}.json'), 'r') as f:
        data = json.load(f)
    return data
