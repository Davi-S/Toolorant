import logging

from client import CustomClient

logger = logging.getLogger(__name__)


class Ranker:
    def __init__(self, client: CustomClient) -> None:
        super().__init__()
        self.client = client
        self._seen_matches = {}

    async def get_players_puuid(self, match_info: dict) -> list[str]:
        return list(match_info['Players']['Subject'])

    def rank(self) -> dict[tuple[str, str], list[str]]:
        try:
            match_info = self.client.coregame_fetch_match()
        except Exception as error:
            logger.error(f'Match information could not be fetched due to error: {error}')
            return {}

        if match_info['MatchID'] in self._seen_matches:
            logger.warn('Repeated match ID')
            return self._seen_matches[match_info['MatchID']]

        # TODO
        result = ...

        # Save the match result on the cache
        self._seen_matches[match_info['MatchID']] = result
        return result
