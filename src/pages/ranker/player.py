import logging

import aiohttp
import game_resources as gr
from client import CustomClient

logger = logging.getLogger(__name__)

class Player:
    # TODO: getter methods for attributes to get the formatted values
    # TODO: do not use __slots__
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
        'kills_per_death',  # Match Details
        'kills_per_match',  # Match Details
        'head_shot',        # Match Details
        'account_level',    # Current Game Match
        'team',             # Current Game Match
        'party',            # Party Player
        '_player_mmr',
        '_player_competitive_update'
    )

    _client = None
    _session = None

    # Every player is on the same match, so one object is enough for all player instances
    _current_game_match = None

    @classmethod
    def init_cls(cls, client: CustomClient, session: aiohttp.ClientSession) -> None:
        logger.debug('Initializing class')
        cls._client = client
        cls._session = session
        cls._current_game_match = cls._client.coregame_fetch_match()

    def __init__(self, puuid: str) -> None:
        self.puuid = puuid
        self._player_mmr = None
        self._player_competitive_update = None

    async def get_player_mmr(self) -> dict:
        """Fetch the player mmr or get the one from the cache"""
        if not self._player_mmr:
            data = await self._client.a_fetch_mmr(self._session, self.puuid)
            self._player_mmr = data
        return self._player_mmr

    async def get_player_competitive_update(self) -> dict:
        """Fetch the player competitive updates (history) or get the one from the cache"""
        if not self._player_competitive_update:
            data = await self._client.a_fetch_competitive_updates(self._session, self.puuid)
            if not data:
                logger.warning(f'No data retrieved for player {self.puuid}')
            self._player_competitive_update = data
        return self._player_competitive_update

    async def build(self) -> None:
        """Call the set method for each attribute in the slots"""
        logger.debug(f'Building player {self.puuid=}')
        for attr in self.__slots__:
            if not attr.startswith('_'):
                method = getattr(self, f'set_{attr}', None)
                if method is not None:
                    await method()
                    
    ####################################
    ########## SETTER METHODS ##########    
    ####################################
    async def set_full_name(self):
        """Set the player's full name (name + tag)"""
        self.full_name = await self._client.a_get_player_full_name(self._session, self.puuid)

    async def set_name(self):
        """Set the player's name"""
        self.name = self.full_name.split('#')[0]

    async def set_tag(self):
        """Set the player's tag"""
        self.tag = self.full_name.split('#')[1]

    async def set_agent(self):
        """Set the match's player's agent"""
        player = next((player for player in self._current_game_match['Players'] if player['Subject'] == self.puuid), None)
        self.agent = gr.Agent(player['CharacterID'])

    async def set_current_rank(self):
        """Set the player's current rank. Default's set to Unranked"""
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            latest_season_comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            self.current_rank = gr.Rank(latest_season_comp['CompetitiveTier'])
        except (KeyError, TypeError):
            self.current_rank = gr.Rank(0)

    async def set_rank_rating(self):
        """Set the player's rank rating. Default's set to 0"""
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            last_season_comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            self.rank_rating = last_season_comp['RankedRating']
        except (KeyError, TypeError):
            self.rank_rating = 0

    async def set_peak_rank(self):
        """Set the player's peak rank of all seasons. Default's set to 0"""
        try:
            data = await self.get_player_mmr()
            seasons = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID']
            peak = max(
                (season_info['Rank'] for season_info in seasons.values()), default=0
            )
            self.peak_rank = gr.Rank(peak)
        except AttributeError:
            self.peak_rank = gr.Rank(0)

    async def set_win_rate(self):
        """Set the player's win rate percent of current season. Default's set to 0"""
        try:
            data = await self.get_player_mmr()
            latest_season_id = await self._client.a_get_latest_season_id(self._session)
            last_season_comp = data['QueueSkills']['competitive']['SeasonalInfoBySeasonID'][latest_season_id]
            total_games = last_season_comp['NumberOfGames']
            won_games = last_season_comp['NumberOfWins']
            self.win_rate = round(won_games / total_games * 100, 1) if total_games else 0
        except (KeyError, TypeError):
            self.win_rate = 0
    
    # TODO: set_kills_per_death, set_kills_per_match, and set_head_shot can use the same a_fetch_competitive_updates response and get all info in one single loop
    async def set_kills_per_death(self):
        """Set the player's kills per death (K/D). Based on a maximum of 20 last matches. Default's set to 0"""
        comp_updates = (await self.get_player_competitive_update()).get('Matches', [])
        kills, deaths = 0, 0
        for match in comp_updates:
            try:
                match_detail = await self._client.a_fetch_match_details(self._session, match['MatchID'])
                if player := next((player for player in match_detail['players'] if player['subject'] == self.puuid), None):
                    kills += player['stats']['kills']
                    deaths += player['stats']['deaths']
            except TypeError:
                continue
        self.kills_per_death = round(kills / deaths, 1) if deaths else kills
        
    async def set_kills_per_match(self):
        """Set the player's kills per match (K/M). Based on a maximum of 20 last matches. Default's set to 0"""
        comp_updates = (await self.get_player_competitive_update()).get('Matches', [])
        kills, matches = 0, 0
        for match in comp_updates:
            try:
                match_detail = await self._client.a_fetch_match_details(self._session, match['MatchID'])
                if player := next((player for player in match_detail['players'] if player['subject'] == self.puuid), None):
                    kills += player['stats']['kills']
                    matches += 1
            except TypeError:
                continue
        self.kills_per_match = round(kills / matches, 1) if matches else 0

    async def set_head_shot(self):
        """Set the player's head shot percent of last 20 matches. Default's set to 0"""
        comp_updates = (await self.get_player_competitive_update()).get('Matches', [])
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
            except TypeError:
                continue
        self.head_shot = round(head_shots / total_shots * 100, 1) if total_shots else 0

    async def set_account_level(self):
        """Set the player's account level"""
        if player := next((player for player in self._current_game_match['Players'] if player['Subject'] == self.puuid), None):
            self.account_level = player['PlayerIdentity']['AccountLevel']
            
    async def set_team(self):
        """Set the player's team. "Blue" or "Red"."""
        player = next((player for player in self._current_game_match['Players'] if player['Subject'] == self.puuid), None)
        self.team = player['TeamID']
        
    async def set_party(self):
        # TODO: Fix this. This is not working as expected. The party ID is always the same for all players
        party = await self._client.a_party_fetch_player(self._session, self.puuid)
        self.party = party['CurrentPartyID']
    ######################################
    ######### END SETTER METHODS #########
    ######################################
