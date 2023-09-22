import logging
import os

import valclient


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
        if file_region := self.get_region():
            logger.debug(f'Starting valclient.Client with ShooterGame.log region: {file_region}')
            super().__init__(file_region, auth)
            return
        if region:
            logger.debug(f'Starting valclient.Client with region argument: {region}')
            super().__init__(region, auth)
            return
        logger.error('Unable to start client due to no region found')
        raise RegionError('Unable to get region')

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
