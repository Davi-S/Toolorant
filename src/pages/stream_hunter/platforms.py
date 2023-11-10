import aiohttp
from settings import user_settings

class Twitch:
    base_url = 'https://www.twitch.tv'
    valorant_game_id = '516575'

    async def validate_access_token(self, session: aiohttp.ClientSession, access_token: str, client_id: str):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": client_id,
        }
        async with session.get('https://api.twitch.tv/helix/validate', headers=headers) as response:
            return response.status == 200

    async def get_access_token(self, session: aiohttp.ClientSession, client_id: str, client_secret: str):
        async with session.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials') as response:
            token = await response.json()
            token = token['access_token']
            user_settings.stream_hunter.twitch.access_token = token
            user_settings.persist()
            return token

    async def get_page(self, session: aiohttp.ClientSession, channel: str, *, client_id, client_secret, access_token) -> str:
        if (not client_id) and (not client_secret) and (not access_token):
            return await self._get_page_without_api(session, channel)

        elif access_token and client_id and await self.validate_access_token(session, access_token, client_id):
            return await self._get_page_with_api(session, access_token, client_id, channel)
            
        elif client_id and client_secret:
            access_token = await self.get_access_token(session, client_id, client_secret)
            return await self._get_page_with_api(session, access_token, client_id, channel)
                
    async def _get_page_with_api(self, session: aiohttp.ClientSession, app_access_token: str, client_id: str, query: str):
        headers = {
            'Authorization': f'Bearer {app_access_token}',
            'Client-ID': f'{client_id}',
        }
        params = {
            'query': query,
            'live_only': 'true',
        }
        async with session.get('https://api.twitch.tv/helix/search/channels', headers=headers, params=params) as response:
            data = await response.json()
            data = data['data']
            return data if response.status == 200 else None

    async def _get_page_without_api(self, session: aiohttp.ClientSession, channel: str):
        async with session.get(url=f'{self.base_url}/{channel}') as resp:
            return await resp.text()

    def get_live(self, response: str | list[dict]) -> str:
        if type(response) == str:
            return self._get_live_without_api(response)
        else:
            return self._get_live_with_api(response)

    def _get_live_without_api(self, response: str) -> str:
        start = response.find('href="https://www.twitch.tv/')
        end = response.find('"', start + 6)
        channel = response[start + 18:end]
        return channel if 'isLiveBroadcast' in response else ''
    
    def _get_live_with_api(self, response: list[dict]) -> list[str]:
        streams = []
        for channel in response:
            if channel['game_id'] == self.valorant_game_id:
                streams.append(f'twitch.tv/{channel["display_name"]}')
        return streams