import concurrent.futures
import logging

import game_resources as gr
from client import CustomClient

from . import platforms
from .player import Player

logger = logging.getLogger(__name__)


class StreamHunter:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self.platforms = [platforms.twitch, platforms.youtube]
        self._seen_matches = {}

    def get_enemies(self, match_info):
        for player in match_info['Players']:
            if player['Subject'] == self.client.puuid:
                ally_team = player['TeamID']
                break

        return [Player(self.client.get_player_full_name(player['Subject']), gr.Agent(player['CharacterID']))
                for player in match_info['Players']
                if player['TeamID'] != ally_team]

    def get_player_streams(self, player):
        logger.debug(f'Getting streams for player: {player}')
        streams = []
        for name in player.name_variations:
            for platform in self.platforms:
                if live := platform.live(name):
                    streams.append(live)
        return streams

    def hunt(self):
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as e:
            logger.error(f'Match information could not be fetched due to error: {e}')
            return {}

        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]

        enemies = self.get_enemies(match_info)

        streams = {}
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_player = {
                executor.submit(self.get_player_streams, player): player
                for player in enemies
            }
            for future in concurrent.futures.as_completed(future_to_player):
                player = future_to_player[future]
                result = future.result()
                streams[(player.full_name, player.agent.name)] = result

        self._seen_matches[match_info['MatchID']] = streams
        return streams
