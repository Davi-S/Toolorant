import logging
import time

import valclient.exceptions

import game_resources as gr
from abstracts import Listener
from extensions.websocket.websocket import Event


logger = logging.getLogger(__name__)


class Instalocker(Listener):
    def __init__(self, client, select_delay, lock_delay) -> None:
        super().__init__()
        self._client = client
        self._seen_matches = set()
        self.profile = None
        self.select_delay = select_delay
        self.lock_delay = lock_delay

    def on_event(self, event):
        if self.profile and event == Event.PREGAME:
            logger.info(f'Received event {event}')
            self.lock()
        return

        
    def lock(self):
        try:
            match_info = self._client.pregame_fetch_match()
        except valclient.exceptions.PhaseError as e:
            logger.error(f'Will not lock because the match information could not be fetched due to error: {e}.')
            return False

        # Check if the function is being called multiple times for the same match
        # This is needed because the WS can notify the same event multiple times.
        if match_info['ID'] in self._seen_matches:
            logger.warn('Will not lock because of repeated match ID')
            return False
        self._seen_matches.add(match_info['ID'])

        # Get the agent for the map
        agent = self.profile.map_agent[self.get_match_map(match_info)]

        # check if the user wants to instalock in this map
        if agent is None:
            logger.info('Will not lock because profile agent is None')
            return False

        # Try to instalock the character
        logger.debug('Ready to try to lock')
        try:
            time.sleep(self.select_delay)
            self._client.pregame_select_character(agent.value)
            logger.debug('Agent selected successfully')
            time.sleep(self.lock_delay)
            self._client.pregame_lock_character(agent.value)
            logger.info('Agent locked successfully')
            return True
        except Exception as e:
            logger.error(f'Could not lock the agent due to error: {e}')
            return False

    def get_match_game_mode(self, match_info: dict):
        game_mode = match_info['Mode'].split('/')[-2]
        # "QueueID" tells if the game is competitive or unrated.
        queue_id = match_info['QueueID'].title()
        game_mode = game_mode + (queue_id if queue_id == 'Competitive' else '')
        logger.debug(f'Match game mode: {game_mode}')
        return gr.GameMode(game_mode)

    def get_match_map(self, match_info: dict):
        game_map = match_info['MapID'].split('/')[-2]
        logger.debug(f'Match map: {game_map}')
        return gr.Map(game_map)
