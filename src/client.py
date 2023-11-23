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

    async def a_put(self, session:  aiohttp.ClientSession, endpoint="/", endpoint_type="pd", json_data=None, exceptions=None) -> dict:
        if json_data is None:
            json_data = {}
        if exceptions is None:
            exceptions = {}
        async with session.put(f'{self.base_url_glz if endpoint_type == "glz" else self.base_url}{endpoint}', headers=self.headers, json=json_data) as response:
            data = await response.text()
            return json.loads(data)[0]

    async def a_get_player_full_name(self, session: aiohttp.ClientSession, puuid: str):
        response = await self.a_put(session, endpoint="/name-service/v2/players", json_data=[puuid])
        playerData = response
        return f"{playerData['GameName']}#{playerData['TagLine']}"

    def fetch_player_settings(self) -> dict:
        return self.fetch('/player-preferences/v1/data-json/Ares.PlayerSettings', 'local')

    def put_player_settings(self, settings_data) -> dict:
        return self.put('/player-preferences/v1/data-json/Ares.PlayerSettings', 'local', settings_data)
