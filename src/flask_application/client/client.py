import logging
import os

import valclient

from logging_configuration import create_file_handler

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))


class RegionError(Exception):
    '''
      Raised whenever there's a problem while attempting to fetch the region.
    '''
    pass


class CustomClient(valclient.Client):
    """Is a valclient that don't need a region"""

    def __init__(self, region=None, auth=None):
        if file_region := self.get_region():
            log.debug(f'Starting valclient with ShooterGame.log region: {file_region}')
            super().__init__(file_region, auth)
            return
        if region:
            log.debug(f'Starting valclient with region argument: {region}')
            super().__init__(region, auth)
            return
        log.error('Unable to start client due to no region found')
        raise RegionError('Unable to get region')

    def get_region(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log'), 'rb') as f:
                lines = f.readlines()
            for line in lines:
                if b'regions' in line:
                    region = line.split(b'regions/')[1].split(b']')[0]
                    region = region.decode()
                    log.debug(f'Region {region} found on "ShooterGame.log" file')
                    return region
        except Exception:
            log.debug('No region on "ShooterGame.log" file found')
            return ''
