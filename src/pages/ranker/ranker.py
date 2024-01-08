import asyncio
import logging
# import random
# import time
# import uuid

import aiohttp

# import game_resources as gr
from client import CustomClient

from .player import Player

logger = logging.getLogger(__name__)


class Ranker:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self._seen_matches = {}

    def get_players_puuid(self, match_info: dict) -> list[str]:
        return [player['Subject'] for player in match_info['Players']]

    async def get_players(self, puuids: list[str]) -> list[Player]:
        players = [Player(puuid) for puuid in puuids]
        async with aiohttp.ClientSession() as session:
            Player.init_cls(self.client, session)
            tasks = [asyncio.create_task(player.build()) for player in players]
            await asyncio.gather(*tasks)
        return players

    def rank(self) -> list[Player]:
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as error:
            logger.error(f'Match information could not be fetched due to error: {error}')
            return {}

        # TODO: uncomment the cache check
        # if match_info['MatchID'] in self._seen_matches:
        #     logger.warn('Repeated match ID')
        #     return self._seen_matches[match_info['MatchID']]

        players_puuid = self.get_players_puuid(match_info)
        logger.info('Getting players')
        try:
            players = asyncio.run(self.get_players(players_puuid))
            logger.info('Got players')
        except Exception as error:
            players = {}
            logger.error(f'Error getting players: {error}')
        # Save the match result on the cache
        self._seen_matches[match_info['MatchID']] = players
        return players
        
        # #### TEST DATA ####
        # players = []
        # prefixes = ['Mystic', 'Solar', 'Galactic', 'Ethereal', 'Quantum', 'Thunder', 'Aqua', 'Inferno', 'Celestial', 'Neon']
        # suffixes = ['Phoenix', 'Spectre', 'Nebula', 'Cipher', 'Zenith', 'Vortex', 'Chronicle', 'Pinnacle', 'Radiance', 'Oracle']
        # base_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack']
        # names = []
        # for name in base_names:
        #     prefix = random.choice(prefixes)
        #     suffix = random.choice(suffixes)
        #     names.append(prefix + name + suffix)
        # teams = ['Blue', 'Blue', 'Blue', 'Blue', 'Blue', 'Red', 'Red', 'Red', 'Red', 'Red']
        # parties = ['0', '1', '1', '2', '3', '4', '4', '7', '6', '5']
        # for i in range(10):
        #     player = Player(str(uuid.uuid4()))
        #     player.full_name = f"{names[i]}#{random.randint(1000, 9999)}"
        #     player.name = player.full_name.split('#')[0]
        #     player.tag = player.full_name.split('#')[1]
        #     player.agent = gr.Agent[agents[i]]
        #     player.current_rank = gr.Rank(random.randint(10, 15))
        #     player.rank_rating = random.randint(30, 80)
        #     player.peak_rank = gr.Rank(random.randint(10, 25))
        #     player.win_rate = round(random.random() * 100, 1)
        #     player.kills_per_death = random.randint(1, 5)
        #     player.kills_per_match = random.randint(15, 20)
        #     player.head_shot = round(random.random() * 100, 1)
        #     player.account_level = random.randint(100, 300)
        #     player.party = parties[i]
        #     player.team = teams[i]
        #     players.append(player)
        # # time.sleep(5)
        # return players
