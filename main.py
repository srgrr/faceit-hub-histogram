"""
	Author: SergioRG
"""
from collections import Counter
import numpy as np
import argparse
import logging
import requests
import uuid
import time
import ast
import os

FACEIT_GET_LIMIT = 20

FACEIT_GET_PLAYER_DETAILS_ENDPOINT = 'https://open.faceit.com/data/v4/players?nickname=%s'
FACEIT_GET_MATCH_HISTORY_ENDPOINT = \
f'https://open.faceit.com/data/v4/players/%s/history?game=csgo&offset=%s&limit={FACEIT_GET_LIMIT}&from=0&to=2047483647'


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


def _get_player_id_and_num_matches(nickname, api_key):
	final_url = FACEIT_GET_PLAYER_DETAILS_ENDPOINT % nickname
	headers = _get_basic_headers(api_key)
	response = requests.get(final_url, headers=headers)
	resp_dict = eval(str(response.json()))
	return resp_dict['player_id']


def _get_competition_names_from_match_history(player_id, api_key):
	competition_names = []
	last_match = None

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

		if not matches:
			logging.debug('Reached end of match history')
			break

		last_match = matches[-1]
		competition_names += [x['competition_name'] for x in matches]

	logging.debug(f'Processed {len(competition_names)}')

	return competition_names


def main(player_name, faceit_api_key, debug):
	if debug:
		logging.basicConfig(filename=f'{player_name}-{uuid.uuid4()}.log', level=logging.DEBUG)

	logging.debug(f'Processing player {player_name} ...')

	player_id = _get_player_id_and_num_matches(player_name, faceit_api_key)
	competition_names = _get_competition_names_from_match_history(player_id, faceit_api_key)

	cnt = Counter(competition_names)

	for (k, v) in cnt.items():
		print(f'{k}: {v}')


if __name__ == '__main__':
	opts = parse_options()
	main(**vars(opts))
