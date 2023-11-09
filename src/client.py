import logging
import os

import valclient
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

    def get_player_full_name(self, puuid):
        playerData = self.put(
            endpoint="/name-service/v2/players",
            json_data=[puuid]
        )[0]
        return f"{playerData['GameName']}#{playerData['TagLine']}"