import asyncio
import logging
import time
import aiohttp
import requests

import game_resources as gr
from client import CustomClient

from . import platforms
from .player import Player

logger = logging.getLogger(__name__)


def get_proxies():
    proxies_response = requests.get(
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&simplified=true', stream=True)
    return [f"socks4://{proxy.decode().strip()}" for proxy in proxies_response.iter_lines() if proxy]


class StreamHunter:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self.platforms = [platforms.Twitch()]
        self._seen_matches = {}
        self._proxies = get_proxies()

    def get_enemies(self, match_info: dict):
        for player in match_info['Players']:
            if player['Subject'] == self.client.puuid:
                ally_team = player['TeamID']
                break

        return [Player(self.client.get_player_full_name(player['Subject']), gr.Agent(player['CharacterID']))
                for player in match_info['Players']
                if player['TeamID'] != ally_team]

    async def get_player_streams(self, player: Player):
        streams = []
        async with aiohttp.ClientSession() as session:
            for platform in self.platforms:
                tasks = [platform.get_task(session, name)
                         for name in player.name_variations]
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    if live := platform.is_live(await response.text()):
                        streams.append(live)
        return streams

    def hunt(self) -> dict[tuple[str, str], list[str]]:
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
        full_names = ["Gaules#123", "alanzoka#456",
                      "cellbit#789", "Sarah Davis#012", "Chris Wilson#345"]
        agents = [gr.Agent['ASTRA'] for _ in range(5)]
        enemies: list[Player] = []
        for full_name, agent in zip(full_names, agents):
            player = Player(full_name=full_name, agent=agent)
            enemies.append(player)

        start = time.time()
        streams = {}
        for player in enemies:
            streams[(player.full_name, player.agent.name)] = asyncio.run(self.get_player_streams(player))
        print(time.time() - start)  # 1
        return streams
