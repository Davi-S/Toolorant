import flask
from ...observer_pattern_abstract import Listener
import valclient
import valclient.resources
from ..websocket.websocket import Event
from .. import game_resources as ge
from ..profile import Profile

instalocker_bp = flask.Blueprint('instalocker_bp', __name__,
                                 template_folder='templates')


def init_app(app: flask.Flask):
    app.register_blueprint(instalocker_bp)


class CustomClient(valclient.Client):
    """Is a valclient that don't need a region and don't need to be initialized."""

    def __init__(self):
        super().__init__()  # passing 'na' region by default (it will be override)
        super().activate()

        region = self.fetch_region()['region'].lower()

        # The same code form the valclient.Client
        self.region = region
        self.shard = region

        if self.region in valclient.resources.region_shard_override.keys():
            self.shard = valclient.resources.region_shard_override[self.region]
        if self.shard in valclient.resources.shard_region_override.keys():
            self.region = valclient.resources.shard_region_override[self.shard]

    def fetch_region(self) -> dict:
        """Gets info about the region and from the Riot client"""
        return self.fetch(endpoint="/riotclient/region-locale", endpoint_type="local")


class Instalocker(Listener):
    def __init__(self) -> None:
        super().__init__()
        # self._client = CustomClient()
        self.profile = None

    def update(self, event):
        print('update called')
        if event != Event.PREGAME_STARTED:
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


instalocker = Instalocker()


@instalocker_bp.route('/start', methods=['POST'])
def start():
    instalocker.profile = 'some_profile'
    flask.current_app.config.websocket.add_listener(instalocker)
    print('instalocker subscribed')
    return ''


@instalocker_bp.route('/stop', methods=['POST'])
def stop():
    flask.current_app.config.websocket.remove_listener(instalocker)
    print('instalocker unsubscribed')
    return ''
