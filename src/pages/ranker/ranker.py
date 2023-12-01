import asyncio
import logging

import aiohttp

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

    def rank(self) -> dict[tuple[str, str], list[str]]:
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as error:
            logger.error(f'Match information could not be fetched due to error: {error}')
            return {}

        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]

        players_puuid = self.get_players_puuid(match_info)
        players = asyncio.run(self.get_players(players_puuid))

        result = players  # TODO

        # Save the match result on the cache
        self._seen_matches[match_info['MatchID']] = result
        return result
