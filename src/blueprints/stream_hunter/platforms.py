import requests

from abstracts import LivePlatform


class Twitch(LivePlatform):
    BASE_URL = 'https://www.twitch.tv'

    @classmethod
    def live(cls, channel):
        response = requests.get(f'{cls.BASE_URL}/{channel}')
        return f'{cls.BASE_URL}/{channel}' if 'isLiveBroadcast' in response.text else ''
