import logging
import time

import valclient.exceptions

import game_resources as gr
import websocket
from abstracts import Listener
from client import CustomClient

from . import profile as prof

logger = logging.getLogger(__name__)

class Instalocker(Listener):
    def __init__(self, client: CustomClient, profile: prof.Profile | None, select_delay: int, lock_delay: int) -> None:
        super().__init__()
        self.client = client
        self.profile = profile
        self.select_delay = select_delay
        self.lock_delay = lock_delay
        
        self._seen_matches = set()

    def on_event(self, event):
        if self.profile and event == websocket.Event.PREGAME:
            logger.info(f'Received event {event}')
            self.lock()
        return

    def lock(self):
        # sourcery skip: extract-method
        try:
            match_info = self.client.pregame_fetch_match()
        except valclient.exceptions.PhaseError:
            logger.error('Will not lock because the match information could not be fetched')
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
        if agent == 'NONE':
            logger.info('Will not lock because profile agent is None')
            return False
        
        if agent == 'DODGE':
            logger.info('Will dodge queue')
            self.client.pregame_quit_match()
            return False

        # Try to lock the character
        logger.debug('Ready to try to lock')
        try:
            time.sleep(self.select_delay)
            self.client.pregame_select_character(agent.value)
            logger.debug('Agent selected successfully')
            time.sleep(self.lock_delay)
            self.client.pregame_lock_character(agent.value)
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
        game_mode = gr.GameMode(game_mode)
        logger.debug(f'Match game mode: {game_mode.name}')
        return game_mode
    
    def get_match_map(self, match_info: dict):
        game_map = match_info['MapID'].split('/')[-2]
        game_map = gr.Map(game_map)
        logger.debug(f'Match map: {game_map.name}')
        return game_map