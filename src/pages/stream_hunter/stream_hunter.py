import asyncio
import logging
import time
import aiohttp

import game_resources as gr
from client import CustomClient

from . import platforms
from .player import Player

logger = logging.getLogger(__name__)


class StreamHunter:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self.platforms = [platforms.Twitch()]
        self._seen_matches = {}

    def get_enemies(self, match_info: dict):
        for player in match_info['Players']:
            if player['Subject'] == self.client.puuid:
                ally_team = player['TeamID']
                break

        return [Player(self.client.get_player_full_name(player['Subject']), gr.Agent(player['CharacterID']))
                for player in match_info['Players']
                if player['TeamID'] != ally_team]

    async def get_players_streams(self, players: list[Player]):
        streams_dict = {}
        async with aiohttp.ClientSession() as session:
            for platform in self.platforms:
                tasks = []
                for player in players:
                    tasks = [platform.get_task(session, name) for name in player.name_variations]
                    responses = await asyncio.gather(*tasks)
                    streams_list = []
                    for response in responses:
                        if live := platform.is_live(await response.text()):
                            streams_list.append(live)
                    streams_dict[(player.full_name, player.agent)] = streams_list                  

        return streams_dict

    def hunt(self) -> dict[tuple[str, gr.Agent], list[str]]:
        # try:
        #     match_info = self.client.coregame_fetch_match()
        # except Exception as e:
        #     logger.error(f'Match information could not be fetched due to error: {e}')
        #     return {}

        # if match_info['MatchID'] in self._seen_matches:
        #     logger.warn('Repeated match ID')
        #     return self._seen_matches[match_info['MatchID']]

        # enemies = self.get_enemies(match_info)
        
        # Create Player objects with random values
        full_names = ["Gaules#123", "alanzoka#456", "Mike Johnson#789", "Sarah Davis#012", "Chris Wilson#345"]
        agents = [gr.Agent['ASTRA'] for _ in range(5)]
        enemies = []
        for full_name, agent in zip(full_names, agents):
            player = Player(full_name=full_name, agent=agent)
            enemies.append(player)
        
        start = time.time()
        
        
        streams = asyncio.run(self.get_players_streams(enemies))
        
        
        print(time.time() - start)  # 1.5
        return streams
