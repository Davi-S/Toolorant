import aiohttp

import game_resources as gr
from client import CustomClient
import valclient.exceptions


class Player:
    __slots__ = (
        'puuid',
        'full_name',        # Name Service
        'name',             # Name Service
        'tag',              # Name Service
        'agent',            # Current Game Match
        'current_rank',     # Player MMR
        'rank_rating',      # Player MMR
        'peak_rank',        # Player MMR
        'win_rate',         # Player MMR
        'kills_per_deaths', # Match Details
        'head_shot',        # Match Details
        'account_level',    # Current Game Match
        '_player_mmr',
    )

    _client = None
    _session = None

    # Every player is on the same match, so one object is enough for all instances
    _current_game_match = None

    @classmethod
    def init_cls(cls, client: CustomClient, session: aiohttp.ClientSession) -> None:
        cls._client = client
        cls._session = session
        cls._current_game_match = cls._client.coregame_fetch_match()

    def __init__(self, puuid: str) -> None:
        self.puuid = puuid
        self._player_mmr = None

    async def get_player_mmr(self):
        if not self._player_mmr:
            data = await self._client.a_fetch_mmr(self._session, self.puuid)
            self._player_mmr = data
        return self._player_mmr

    async def build(self):
        for attr in self.__slots__:
            if not attr.startswith('_'):
                method = getattr(self, f'set_{attr}', None)
                if method is not None:
                    await method()

    async def set_full_name(self):
        self.full_name = await self._client.a_get_player_full_name(self._session, self.puuid)

    async def set_name(self):
        self.name = self.full_name.split('#')[0]

    async def set_tag(self):
        self.tag = self.full_name.split('#')[1]

    async def set_agent(self):
        if player := next((player for player in self._current_game_match['Players'] if player['Subject'] == self.puuid), None):
            self.agent = gr.Agent(player['CharacterID'])
        else:
            self.agent = gr.Agent(0)

    async def set_current_rank(self):
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            latest_season_info = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            self.current_rank = gr.Rank(latest_season_info['CompetitiveTier'])
        except (KeyError, TypeError):
            self.current_rank = gr.Rank(0)

    async def set_rank_rating(self):
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            last_season_comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            self.rank_rating = last_season_comp['RankedRating']
        except (KeyError, TypeError):
            self.rank_rating = 0

    async def set_peak_rank(self):
        """Peak rank counting all seasons"""
        try:
            data = await self.get_player_mmr()
            comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID']
            peak = max(
                (season_info['Rank'] for season_info in comp.values()),
                default=0
            )
            self.peak_rank = gr.Rank(peak)
        except AttributeError:
            self.peak_rank = gr.Rank(0)

    async def set_win_rate(self):
        """Win rate of current season"""
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            last_season_comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            total_games = last_season_comp['NumberOfGames']
            won_games = last_season_comp['NumberOfWins']
            # Percent
            self.win_rate = round(won_games / total_games * 100, 2) if total_games else 0
        except (KeyError, TypeError):
            self.win_rate = 0

    async def set_kills_per_deaths(self):
        """KD of last 20 matches"""
        comp_updates = (await self._client.a_fetch_competitive_updates(self._session, self.puuid, 0, 20))['Matches']
        kills, deaths = 0, 0
        for match in comp_updates:
            try:
                match_detail = await self._client.a_fetch_match_details(self._session, match['MatchID'])
                if player := next((player for player in match_detail['players'] if player['subject'] == self.puuid), None):
                    kills += player['stats']['kills']
                    deaths += player['stats']['deaths']
            except (TypeError, valclient.exceptions.ResponseError):
                continue
        self.kills_per_deaths = round(kills / deaths, 2) if deaths else kills

    async def set_head_shot(self):
        """HS percent of last 20 matches"""
        comp_updates = (await self._client.a_fetch_competitive_updates(self._session, self.puuid, 0, 20))['Matches']
        total_shots, head_shots = 0, 0
        for match in comp_updates:
            try:
                match_detail = await self._client.a_fetch_match_details(self._session, match['MatchID'])
                for game_round in match_detail['roundResults']:
                    player_stats = next(
                        (player['damage']
                        for player in game_round['playerStats']
                        if player['subject'] == self.puuid),
                        []
                    )
                    for damage in player_stats:
                        total_shots += damage['bodyshots'] + damage['legshots'] + damage['headshots']
                        head_shots += damage['headshots']
            except (TypeError, valclient.exceptions.ResponseError):
                continue
        self.head_shot = round(head_shots / total_shots * 100, 2) if total_shots else 0

    async def set_account_level(self):
        if player := next((player for player in self._current_game_match['Players'] if player['Subject'] == self.puuid), None):
            self.account_level = player['PlayerIdentity']['AccountLevel']
