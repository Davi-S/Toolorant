import asyncio
import logging

import aiohttp
import requests

import game_resources as gr
from client import CustomClient
from settings import user_settings

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
        self.platforms = {'twitch': platforms.Twitch}
        self._seen_matches = {}

    async def get_enemies(self, match_info: dict) -> list[Player]:
        for player in match_info['Players']:
            if player['Subject'] == self.client.puuid:
                ally_team = player['TeamID']
                break
        enemies = [player for player in match_info['Players'] if player['TeamID'] != ally_team]
        
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(self.client.a_get_player_full_name(session, enemy['Subject']))
                for enemy in enemies
            ]
            results = await asyncio.gather(*tasks)
        
        return  [Player(full_name, gr.Agent(enemy['CharacterID'])) for full_name, enemy in zip(results, enemies)]

    async def get_player_streams(self, player: Player) -> list[str]:
        logger.debug(f'Getting streams of player {player.full_name}')
        streams = []
        async with aiohttp.ClientSession() as session:
            for platform_name, platform_cls in self.platforms.items():
                platform = platform_cls(session, **user_settings.stream_hunter[platform_name])
                await platform.initialize()
                tasks = [
                    asyncio.create_task(platform.get_response(name))
                    for name in player.name_variations
                ]
                responses = await asyncio.gather(*tasks)
                for response in responses:
                    if live := platform.get_live(response):
                        streams.extend(live)
        return set(streams)

    def hunt(self) -> dict[tuple[str, str], list[str]]:
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as e:
            logger.error(f'Match information could not be fetched due to error: {e}')
            return {}

        # Check seen matches (cache)
        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]
        
        logger.info('Getting players streams')
        enemies = asyncio.run(self.get_enemies(match_info))
        result = {
            (player.name, player.agent.name): asyncio.run(self.get_player_streams(player))
            for player in enemies
        }
        # Save result on cache and return
        self._seen_matches[match_info['MatchID']] = result
        return result
