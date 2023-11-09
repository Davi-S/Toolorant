import asyncio
import logging

import aiohttp
import requests

import game_resources as gr
from client import CustomClient

from . import platforms
from .player import Player

logger = logging.getLogger(__name__)


# TODO: use proxies to make requests so the IP is not blocked
def get_proxies():
    proxies_response = requests.get(
        'https://api.proxyscrape.com/v2/?request=displayproxies&protocol=socks4&timeout=5000&country=all&simplified=true',
        stream=True
    )
    return [f"socks4://{proxy.decode().strip()}" for proxy in proxies_response.iter_lines() if proxy]


class StreamHunter:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self.platforms = [platforms.Twitch()]
        self._seen_matches = {}

    def get_enemies(self, match_info: dict) -> list[Player]:
        # TODO: Implement asyncio for this function
        for player in match_info['Players']:
            if player['Subject'] == self.client.puuid:
                ally_team = player['TeamID']
                break

        return [Player(self.client.get_player_full_name(player['Subject']), gr.Agent(player['CharacterID']))
                for player in match_info['Players']
                if player['TeamID'] != ally_team]

    async def get_player_streams(self, player: Player) -> list[str]:
        streams = []
        async with aiohttp.ClientSession() as session:
            for platform in self.platforms:
                tasks = [asyncio.create_task(platform.get_page(session, name))
                         for name in player.name_variations]
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    if live := platform.is_live(response):
                        streams.append(live)
        return streams

    def hunt(self) -> dict[tuple[str, str], list[str]]:
        # TODO optimize this function. Actual average time to run is 6 seconds
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as e:
            logger.error(f'Match information could not be fetched due to error: {e}')
            return {}
        # 1.5 seconds to execute from start to here

        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]
        enemies = self.get_enemies(match_info)
        # 3.8 seconds to execute from last timed to here

        return {
            (player.name, player.agent.name): asyncio.run(self.get_player_streams(player))
            for player in enemies
        }
        # 0.8 seconds to execute from last timed to here
