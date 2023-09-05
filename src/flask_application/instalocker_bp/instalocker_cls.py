import logging
import time

from logging_configuration import create_file_handler

from .. import game_resources as gr
from ..abstracts import Listener
from ..websocket.websocket import Event

# Get the file logger and its handler
log = logging.getLogger(__name__)
log.addHandler(create_file_handler(__name__))


class Instalocker(Listener):
    def __init__(self, client, select_delay, lock_delay) -> None:
        super().__init__()
        self._client = client
        self._seen_matches = set()
        self.select_delay = select_delay
        self.lock_delay = lock_delay
        self.profile = None

    def on_event(self, event):
        if self.profile and event == Event.PREGAME:
            log.info(f'Received event {event}')
            self.lock()
        return

    def lock(self):
        try:
            match_info = self._client.pregame_fetch_match()
        except Exception as e:  # TODO: add exception "You are not in a pre-game error" to be more specific about the exception
            log.warning(f'Could not get match information due to: {e}. Will not lock')
            return

        # Check if the function is being called multiple times for the same match
        # This is needed because the WS can notify the same event multiple times.
        # TODO: See the websocket file to fix this
        if match_info['ID'] in self._seen_matches:
            log.warning('Repeated match ID. Will not lock')
            return
        log.debug(f'Match info: {match_info}')
        self._seen_matches.add(match_info['ID'])

        # Check the game mode
        if self.get_match_game_mode(match_info) != self.profile.game_mode:
            log.info('Match and profile game mode does not match. Will not lock')
            return

        # Get the agent for the map
        agent = self.profile.map_agent[self.get_match_map(match_info)]

        # check if the user wants to instalock in this map
        if agent is None:
            log.info('Match and profile agent does not match. Will not lock')
            return

        # Try to instalock the character
        try:
            # Using sleep will only stop the thread. This function is meant to run in a separated thread than the rest of the program
            time.sleep(self.select_delay)
            select_info = self._client.pregame_select_character(agent.value)
            log.debug('Agent selected successfully')
            time.sleep(self.lock_delay)
            lock_info = self._client.pregame_lock_character(agent.value)
            log.info('Agent locked successfully')
        # TODO: treat errors that can happen when locking the character
        except Exception as e:
            log.warning(f'Could not lock the agent due to: {e}')
            return

    def get_match_game_mode(self, match_info: dict):
        game_mode = match_info['Mode'].split('/')[-2]
        # "QueueID" tells if the game is competitive or unrated.
        # Only add the suffix for unrated or competitive game mode 
        queue_id = match_info['QueueID'].title()
        game_mode = game_mode + (queue_id if queue_id in ['Unrated', 'Competitive'] else '')
        log.debug(f'Match game mode: {game_mode}')
        return gr.GameMode(game_mode)

    def get_match_map(self, match_info: dict):
        game_map = match_info['MapID'].split('/')[-2]
        log.debug(f'Match map: {game_map}')
        return gr.Map(game_map)
