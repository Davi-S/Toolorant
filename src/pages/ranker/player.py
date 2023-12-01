import dataclasses

import game_resources as gr

# puuid          Current Game Match
# name           Current Game Match
# agent          Current Game Match
# current rank   Current Game Match
# rank rating    Player MMR
# peak rank      Player MMR
# win rate (%)   Player MMR
# KD (%)         Match Details
# headshot (%)   Match Details
# account level  Current Game Match

@dataclasses.dataclass
class Player:
    puuid: str
    full_name: str
    name: str = dataclasses.field(init=False)
    tag: str = dataclasses.field(init=False)
    agent: gr.Agent
    current_rank: str
    rank_rating: str
    peak_rank: str
    win_rate: str
    kills_per_deaths: str
    head_shot: str
    account_level: str

    def __post_init__(self):
        self.name = self.full_name.split('#')[0]
        self.tag = self.full_name.split('#')[1]
