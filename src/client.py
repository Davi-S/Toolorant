import contextlib
import json
import logging
import os

import aiohttp
import valclient
import valclient.exceptions
import valclient.resources

# Get the file logger and its handler
logger = logging.getLogger(__name__)


class RegionError(Exception):
    """
    Raised whenever there's a problem while attempting to fetch the region.
    """
    pass


class CustomClient(valclient.Client):
    """Is a valclient that can also get the region from Valorant logs"""

    def __init__(self, region=None, auth=None):
        self._latest_season_id = None

        self.is_active = False
        if file_region := self.get_region():
            logger.info(f'Starting valclient.Client with ShooterGame.log region: {file_region}')
            self.is_good_region = True
            super().__init__(file_region, auth)
            return
        if region:
            logger.info(f'Starting valclient.Client with region argument: {region}')
            self.is_good_region = True
            super().__init__(region, auth)
            return
        logger.warn('No region found. Starting client with default region "na"')
        self.is_good_region = False
        super().__init__(region='na', auth=auth)

    def activate(self) -> None:
        super().activate()
        self.is_active = True

    def get_region(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log'), 'rb') as f:
                lines = f.readlines()
            for line in lines:
                if b'regions' in line:
                    region = line.split(b'regions/')[1].split(b']')[0]
                    region = region.decode()
                    logger.debug(f'Region "{region}" found on "ShooterGame.log" file')
                    return region
        except Exception:
            logger.debug('No region on "ShooterGame.log" file found')
            return ''

    def __check_puuid(self, puuid) -> str:
        return self.puuid if puuid is None else puuid

#########################################################################
############################# ASYNC METHODS #############################
#########################################################################

    async def a_put(self, session: aiohttp.ClientSession, endpoint="/", endpoint_type="pd", json_data=None, exceptions=None) -> dict:
        if json_data is None:
            json_data = {}
        if exceptions is None:
            exceptions = {}
        async with session.put(f'{self.base_url_glz if endpoint_type == "glz" else self.base_url}{endpoint}', headers=self.headers, json=json_data) as response:
            data = await response.text()
            return json.loads(data)[0]

    async def a_fetch(self, session: aiohttp.ClientSession, endpoint="/", endpoint_type="pd"):
        base_url = (
            self.base_url_glz
            if endpoint_type == "glz"
            else self.base_url
            if endpoint_type == "pd"
            else self.base_url_shared
            if endpoint_type == "shared"
            else self.base_url
        )

        url = f"{base_url}{endpoint}"

        headers = self.headers

        if endpoint_type == "local":
            url = "https://127.0.0.1:{port}{endpoint}".format(port=self.lockfile["port"], endpoint=endpoint)
            headers = self.local_headers
            
        data = {}
        async with session.get(url, headers=headers) as response:
            with contextlib.suppress(Exception):
                data = json.loads(await response.text())
        return data

    async def __a_coregame_check_match_id(self, session: aiohttp.ClientSession, match_id) -> str:
        player = await self.a_coregame_fetch_player(session=session)
        return player["MatchID"] if match_id is None else match_id

    async def a_get_player_full_name(self, session: aiohttp.ClientSession, puuid: str):
        response = await self.a_put(session, endpoint="/name-service/v2/players", json_data=[puuid])
        playerData = response
        return f"{playerData['GameName']}#{playerData['TagLine']}"

    async def a_coregame_fetch_match(self, session: aiohttp.ClientSession, match_id: str = None) -> dict:
        match_id = await self.__a_coregame_check_match_id(session, match_id)
        return await self.a_fetch(
            session=session,
            endpoint=f"/core-game/v1/matches/{match_id}",
            endpoint_type="glz",
            exceptions={404: [valclient.exceptions.PhaseError, "You are not in a core-game"]}
        )

    async def a_coregame_fetch_player(self, session: aiohttp.ClientSession) -> dict:
        return await self.a_fetch(
            session=session,
            endpoint=f"/core-game/v1/players/{self.puuid}",
            endpoint_type="glz",
            exceptions={404: [valclient.exceptions.PhaseError, "You are not in a core-game"]}
        )

    async def a_fetch_mmr(self, session: aiohttp.ClientSession, puuid: str = None) -> dict:
        puuid = self.__check_puuid(puuid)
        return await self.a_fetch(
            session=session,
            endpoint=f"/mmr/v1/players/{puuid}", endpoint_type="pd"
        )

    async def a_get_latest_season_id(self, session: aiohttp.ClientSession):
        if self._latest_season_id:
            return self._latest_season_id
        content = await self.a_fetch_content(session)
        for season in content["Seasons"]:
            if season["IsActive"]:
                season_id = season["ID"]
                self._latest_season_id = season_id
                return self._latest_season_id

    async def a_fetch_content(self, session: aiohttp.ClientSession) -> dict:
        return await self.a_fetch(
            session=session,
            endpoint="/content-service/v3/content",
            endpoint_type="shared"
        )

    async def a_fetch_competitive_updates(self, session: aiohttp.ClientSession, puuid: str = None, start_index: int = 0, end_index: int = 1, queue_id: str = "competitive") -> dict:
        puuid = self.__check_puuid(puuid)
        return await self.a_fetch(
            session=session,
            endpoint=f"/mmr/v1/players/{puuid}/competitiveupdates?startIndex={start_index}&endIndex={end_index}" + (f"&queue={queue_id}" if queue_id != "" else ""),
            endpoint_type="pd",
        )

    async def a_fetch_match_details(self, session: aiohttp.ClientSession, match_id: str) -> dict:
        return await self.a_fetch(
            session=session,
            endpoint=f"/match-details/v1/matches/{match_id}",
            endpoint_type="pd",
        )

    async def a_party_fetch_player(self, session: aiohttp.ClientSession, puuid: str):
        puuid = self.__check_puuid(puuid)
        return await self.a_fetch(
            session=session,
            endpoint=f"/parties/v1/players/{self.puuid}",
            endpoint_type="glz",
        )