"""
    Author: SergioRG
"""
from collections import Counter
import numpy as np
import argparse
import logging
import requests
import itertools
import uuid
import time
import ast
import os

FACEIT_GET_LIMIT = 20

FACEIT_GET_PLAYER_DETAILS_ENDPOINT = 'https://open.faceit.com/data/v4/players?nickname=%s'
FACEIT_GET_MATCH_HISTORY_ENDPOINT = \
f'https://open.faceit.com/data/v4/players/%s/history?game=csgo&offset=%s&limit={FACEIT_GET_LIMIT}&from=0'


def parse_options():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--player-name',
        help='Nickname of the player in faceit'
    )

    parser.add_argument(
        '--faceit-api-key',
        type=str,
        help='Faceit API key'
    
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug messages'
        )

    return parser.parse_args()


def _get_basic_headers(api_key):
    return {'Authorization': f'Bearer {api_key}'}


def _hub_honesty_factor(play_count, honest_hubs=['CS:GO 5v5', 'CS:GO 5v5 PREMIUM']):
    return 1.0 * sum(play_count[x] for x in honest_hubs) / sum(y for y in play_count.values())


def _team_dishonesty_factor(player_team, match):
    levels = [x['skill_level'] for x in match['teams'][player_team]['players']]
    return sum([(l1 - l2) ** 2 for (l1, l2) in itertools.combinations(levels, 2)])


def _get_team_name(player_id, match):
    return 'faction1' if player_id in \
    [x['player_id'] for x in match['teams']['faction1']['players']] \
    else 'faction2'


def _get_player_id(nickname, api_key):
    final_url = FACEIT_GET_PLAYER_DETAILS_ENDPOINT % nickname
    headers = _get_basic_headers(api_key)
    response = requests.get(final_url, headers=headers)
    resp_dict = eval(str(response.json()))
    return resp_dict['player_id']


def _get_match_history(player_id, api_key):
    for offset in range(0, 2 ** 15 - 1, FACEIT_GET_LIMIT):
        logging.debug(f'Processing offset {offset}')
        final_url = FACEIT_GET_MATCH_HISTORY_ENDPOINT % (player_id, str(offset))
        headers = _get_basic_headers(api_key)
        response = requests.get(final_url, headers=headers)
        resp_dict = eval(str(response.json()))

        if not 'items' in resp_dict:
            logging.debug('REST API returned something unexpected')
            logging.debug(resp_dict)
            break

        matches = resp_dict['items']

        for match in matches:
            yield match

        if not matches:
            logging.debug('Reached end of match history')
            break


def main(player_name, faceit_api_key, debug):

    output_base = f'{player_name}-{uuid.uuid4()}'

    if debug:
        logging.basicConfig(filename=f'{output_base}.log', level=logging.DEBUG)

    logging.debug(f'Processing player {player_name} ...')

    player_id = _get_player_id(player_name, faceit_api_key)

    report_d = {}

    for match in _get_match_history(player_id, faceit_api_key):
        logging.debug(f'Processing match {match["match_id"]}')
        player_team = _get_team_name(player_id, match)
        logging.debug(f'Target player played in {player_team}')
        hub_name = match['competition_name']
        logging.debug(f'Match was played in {hub_name}')
        player_won = player_team == match['results']['winner']
        logging.debug(f'Target player won the game: {player_won}')
        dishonesty_factor = _team_dishonesty_factor(player_team, match)
        logging.debug(f'Team dishonesty factor: {dishonesty_factor}')
        match_date = match['started_at']
        logging.debug(f'Match started at {match_date}')
        logging.debug('-' * 20)

        report_d.setdefault(hub_name, []).append(
            {
                'player_won': int(player_won),
                'dishonesty_factor': dishonesty_factor,
                'match_date': match_date
            }
        )

    print(report_d)


if __name__ == '__main__':
    opts = parse_options()
    main(**vars(opts))
