import os
import json
import requests
from pprint import pprint

to_keep_card_info = {
	'card_info': ['name', 'oracle_id'],
	'pricing_info': ['type_line', 'legalities', 'reserved','cmc', 'released_at'],
	'printing_info': ['booster', 'full_art', 'prices', 'rarity', 'promo', 'reprint', 'set', 'set_type'],
	'extra_info': ['oracle_text', 'mana_cost', 'edhrec_rank', 'colors', 'card_faces']
}


def get_card_name_list():
	url = 'https://api.scryfall.com/catalog/card-names'
	card_name_file = 'MTG_Card_Names.txt'
	if not os.path.exists(card_name_file) or os.path.getsize(card_name_file) < 64:
		print('Downloading card list...')
		url = 'https://api.scryfall.com/catalog/card-names'
		response = requests.get(url)
		print(f'Card names response code: {response.status_code}')
		if response.status_code != 200:
			print('Card list download ({url}) failed, exiting.')
			exit()
		card_names = json.loads(response.text)['data']
		with open(card_name_file, 'w', encoding="utf-8") as file:
			file.write('\n'.join(card_names))
	else:
		with open(card_name_file, 'r', encoding="utf-8") as file:
			card_names = [card_name for card_name in file]#.splitlines()
	return card_names


def get_card_data():
	# TO-DO: Gather more information for better analysis
	bulk_save_location = 'MTG_Cards_bulk_data.json'
	card_info_file = 'MTG_Card_info.json'
	if not os.path.exists(card_info_file) or os.path.getsize(card_info_file) < 64:
		if not os.path.exists(bulk_save_location) or os.path.getsize(bulk_save_location) < 64:
			print('MTG Card data doesn\'t exist, downloading...')
			url = 'https://c2.scryfall.com/file/scryfall-bulk/oracle-cards/oracle-cards-20210309220412.json'
			response = requests.get(url)
			print(f'Bulk download response code: {response.status_code}')
			bulk_data = response.text
			with open(bulk_save_location, 'w', encoding="utf-8") as file:
				file.write(bulk_data)
		else:
			print('MTG Card data exist, loading...')
			with open(bulk_save_location, 'r', encoding="utf-8") as file:
				bulk_data = json.load(file)
		filtered_data = extract_data(bulk_data)
		with open(card_info_file, 'w', encoding="utf-8") as file:
			json.dump(filtered_data, file)
	else:
		with open(card_info_file, 'r', encoding="utf-8") as file:
			filtered_data = json.load(file)
	return filtered_data


def extract_data(raw_data):
	extracted_data = {}
		
	for card_data in raw_data:
		try:
			if card_data['lang'] != 'en':
				print(f'Non-English card: {card_data["name"]} {card_data["lang"]} {card_data["uri"]}')
				continue
			oracle_card = extracted_data.get(card_data['name'].lower(), {})
			# empty dict evaluate to False
			if oracle_card:
				for info_type in to_keep_card_info.keys():
					for useful_data in to_keep_card_info[info_type]:
						if info_type == 'printing_info':
							oracle_card[info_type][useful_data] = [card_data[useful_data]]
						else:
							oracle_card[info_type][useful_data] = card_data[useful_data]
			else:
				oracle_card = {'card_info': {},	'pricing_info': {}, 'printing_info': {}, 'extra_info': {}}
				for useful_data in to_keep_card_info['printing_info']:
					oracle_card['printing_info'][useful_data] = [card_data[useful_data]]
			extracted_data[card_data['name'].lower()] = oracle_card

		except KeyError as e:
			print(card_data['name'], card_data['object'], e)
	return extracted_data
			# exit()


if __name__ == "__main__":
	get_card_name_list()
	get_card_data()