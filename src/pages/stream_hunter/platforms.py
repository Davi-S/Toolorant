import aiohttp


class Twitch:
    # TODO: Add twitch api key and user id supports
    BASE_URL = 'https://www.twitch.tv'

    async def get_page(self, session: aiohttp.ClientSession, channel: str) -> str:
        async with session.get(url=f'{self.BASE_URL}/{channel}') as resp:
            return await resp.text()

    def is_live(self, response: str) -> str:
        start = response.find('href="https://www.twitch.tv/')
        end = response.find('"', start + 6)
        channel = response[start + 18:end]
        return channel if 'isLiveBroadcast' in response else ''

# TODO: Add Youtube support