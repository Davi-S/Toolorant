import aiohttp

from settings import user_settings


class Twitch:
    base_url = 'https://www.twitch.tv'
    valorant_game_id = '516575'

    def __init__(self, session: aiohttp.ClientSession, *, client_id: str, client_secret: str, access_token: str) -> None:
        self.session = session
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token

        self.use_api = False
    
    async def initialize(self):
        # Does not has any of the auth methods. Will use the web scrap method.
        if (not self.client_id) and (not self.client_secret) and (not self.access_token):
            return
        
        # Valid access token and client id. Will use the API method.
        if self.access_token and self.client_id and await self.validate_access_token(self.access_token, self.client_id):
            self.use_api = True
            return

        # Not a valid access token, but has the client id and client secret, so try to get the access token
        if self.client_id and self.client_secret:
            token = await self.get_access_token(self.client_id, self.client_secret)
            if token:
                # Update with valid access token. Else, the auth methods are invalid and will use the web scrap method
                self.access_token = token
                user_settings.stream_hunter.twitch.access_token = self.access_token
                user_settings.persist()
                self.use_api = True

    async def validate_access_token(self, access_token: str, client_id: str) -> bool:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Client-ID": client_id,
        }
        async with self.session.get('https://id.twitch.tv/oauth2/validate', headers=headers) as response:
            return response.status == 200

    async def get_access_token(self, client_id: str, client_secret: str) -> str:
        async with self.session.post(f'https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials') as response:
            if response.status != 200:
                return ''
            response = await response.json()
            return response['access_token']

    async def get_response(self, query: str) -> list | str:
        if self.use_api:
            return await self._get_response_with_api(query)
        else:
            return await self._get_response_without_api(query)

    async def _get_response_with_api(self, query: str) -> list:
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Client-ID': f'{self.client_id}',
        }
        params = {
            'query': query,
            'live_only': 'true',
        }
        async with self.session.get('https://api.twitch.tv/helix/search/channels', headers=headers, params=params) as response:
            if response.status != 200:
                return None
            response = await response.json()
            return response['data']

    async def _get_response_without_api(self, query: str) -> str:
        async with self.session.get(url=f'{self.base_url}/{query}') as response:
            return await response.text()

    def get_live(self, response: str | list) -> list:
        if self.use_api:
            return self._get_live_with_api(response)
        else:
            return self._get_live_without_api(response)

    def _get_live_with_api(self, response: list) -> list:
        streams = []
        for channel in response:
            if channel['game_id'] == self.valorant_game_id:
                streams.append(f'twitch.tv/{channel["broadcaster_login"]}')
        return streams

    def _get_live_without_api(self, response: str) -> list:
        start = response.find('href="https://www.twitch.tv/')
        end = response.find('"', start + 6)
        channel = response[start + 18:end]
        return [channel] if 'isLiveBroadcast' in response else []
