import valclient
import os


class RegionError(Exception):
    '''
      Raised whenever there's a problem while attempting to fetch the region.
    '''
    pass


class CustomClient(valclient.Client):
    """Is a valclient that don't need a region"""

    def __init__(self, region=None, auth=None):
        if not region and (region := self.get_region()) or region:
            super().__init__(region, auth)
            return
        else:
            raise RegionError('Unable to get region')

    def get_region(self):
        try:
            with open(os.path.join(os.getenv('LOCALAPPDATA'), R'VALORANT\Saved\Logs\ShooterGame.log'), 'rb') as f:
                lines = f.readlines()
            for line in lines:
                if b'regions' in line:
                    region = line.split(b'regions/')[1].split(b']')[0]
                    return region.decode()
        except Exception:
            return ''

    