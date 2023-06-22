from ..abstracts import Listener

class Instalocker(Listener):
    def __init__(self) -> None:
        super().__init__()
        # self._client = CustomClient()
        self.profile = None

    def on_event(self, event):
        print('update called')
        if event != 'pregame_started':
            return

        if not self.profile:
            return

        self.lock()

    def lock(self):
        print('lock called')
    #     match_info = self._client.pregame_fetch_match()

    #     # Check the game mode
    #     if self.get_match_game_mode(match_info) != profile.game_mode:
    #         return

    #     # Get the agent for the map
    #     agent = profile.map_agent[self.get_match_map(match_info)]

    #     # check if the user does not wants to instalock in this map
    #     if agent is None:
    #         return

    #     # Try to instalock the character
    #     # TODO: treat errors that can happen when locking the character
    #     lock_info = self._client.pregame_lock_character(agent.value)

    # def get_match_game_mode(self, match_info: dict):
    #     game_mode = match_info['Mode'].split('/')[-2]
    #     # "QueueID" tells if the game is competitive.
    #     # If the game is NOT competitive, "QueueID" will be a empty string. Tus, not affecting "game_mode"
    #     # If the game IS competitive, "QueueID" will be "Competitive".
    #     game_mode = game_mode + match_info['QueueID'].title()
    #     return ge.GameMode(game_mode)

    # def get_match_map(self, match_info: dict):
    #     game_map = match_info['MapID'].split('/')[-2]
    #     return ge.Map(game_map)
