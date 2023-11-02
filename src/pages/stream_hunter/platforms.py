import aiohttp
import requests

class Twitch:
    BASE_URL = 'https://www.twitch.tv'

    def get_task(self, session: aiohttp.ClientSession, channel: str):  
        return session.get(f'{self.BASE_URL}/{channel}')

    def is_live(self, response: str):
        start = response.find('href="https://www.twitch.tv/')
        end = response.find('"', start + 6)
        channel = response[start + 18:end]
        return channel if 'isLiveBroadcast' in response else ''
