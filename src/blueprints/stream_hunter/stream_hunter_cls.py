import concurrent.futures
import logging

from . import platforms
from .player import Player


logger = logging.getLogger(__name__)


class StreamHunter:
    def __init__(self, client) -> None:
        super().__init__()
        self._client = client
        self._seen_matches = {}
        self._platforms = [platforms.Twitch]

    def get_player_full_name(self, puuid):
        playerData = self._client.put(
            endpoint="/name-service/v2/players",
            json_data=[puuid]
        )[0]
        return f"{playerData['GameName']}#{playerData['TagLine']}"

    def get_enemies(self, match_info):
        for player in match_info['Players']:
            if player['Subject'] == self._client.puuid:
                ally_team = player['TeamID']
                break

        return [Player(self.get_player_full_name(player['Subject']))
                for player in match_info['Players']
                if player['TeamID'] != ally_team]

    def get_player_streams(self, player):
        logger.debug(f'Getting streams for player: {player}')
        streams = []
        for name in player.name_variations:
            for platform in self._platforms:
                if live := platform.live(name):
                    streams.append(live)
        return streams

    def hunt(self):
        try:
            match_info = self._client.coregame_fetch_match()
        except Exception as e:
            logger.error(f'Match information could not be fetched due to error: {e}')
            return {}

        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]
        
        self._seen_matches[match_info['MatchID']] = {}

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
                streams[player.full_name] = result

        self._seen_matches[match_info['MatchID']] = streams
        return streams
