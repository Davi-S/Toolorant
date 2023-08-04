from .. import game_resources as gr
from ..abstracts import Listener
from ..websocket.websocket import Event


class Instalocker(Listener):
    def __init__(self, client) -> None:
        super().__init__()
        self._client = client
        self.profile = None
        self._seen_matches = set()

    def on_event(self, event):
        if self.profile and event == Event.PREGAME:
            self.lock()
        return

    def lock(self):
        try:
            match_info = self._client.pregame_fetch_match()
        except Exception:  # TODO: add exception "You are not in a pre-game error" to be more specific about the exception
            return

        # Check if the function is being called multiple times for the same match
        # This is needed because the WS can notify the same event multiple times
        if match_info['ID'] in self._seen_matches:
            return
        self._seen_matches.add(match_info['ID'])

        # Check the game mode
        if self.get_match_game_mode(match_info) != self.profile.game_mode:
            return

        # Get the agent for the map
        agent = self.profile.map_agent[self.get_match_map(match_info)]

        # check if the user wants to instalock in this map
        if agent is None:
            return

        # Try to instalock the character
        try:
            lock_info = self._client.pregame_lock_character(agent.value)
        # TODO: treat errors that can happen when locking the character
        except Exception:
            return

    def get_match_game_mode(self, match_info: dict):
        game_mode = match_info['Mode'].split('/')[-2]
        # "QueueID" tells if the game is competitive.
        # If the game is NOT competitive, "QueueID" will be a empty string. Tus, not affecting "game_mode"
        # If the game IS competitive, "QueueID" will be "Competitive".
        game_mode = game_mode + match_info['QueueID'].title()
        return gr.GameMode(game_mode)

    def get_match_map(self, match_info: dict):
        game_map = match_info['MapID'].split('/')[-2]
        return gr.Map(game_map)
