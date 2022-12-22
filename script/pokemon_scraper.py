import pandas as pd
import argparse
import pokebase as pb
import requests
import json


def get_all_pokemon(generation):
    """
    Args:
        generation (int): pokemon generation

    Returns:
        list of pokemons belonging to specified generation
    """
    all_pokemon = pb.generation(generation)
    list_of_pokemon = []
    for pokemon in all_pokemon.pokemon_species:
        list_of_pokemon.append(pokemon.name)
    return list_of_pokemon

class Pokemon:
    def __init__(self, name, json_data):
        self.name = name
        self.json_data = json_data

    def get_stats(self):
        stat_dict = {}
        all_stats = self.json_data['stats']
        for stats in all_stats:
            stat_name = stats['stat']['name']
            stat_value = stats['base_stat']
            stat_dict.update({stat_name: stat_value})
        return stat_dict

    def get_types(self):
        types_list = []
        types = self.json_data['types']
        for type in types:
            types_list.append(type['type']['name'])
        return types_list

    def get_base_exp(self):
        base_exp = self.json_data['base_experience']
        return base_exp

    def get_height(self):
        height = self.json_data['height']
        return height
    
    def get_weight(self):
        weight = self.json_data['weight']
        return weight

    def get_image_url(self):
        image_url = self.json_data['sprites']['front_default']
        return image_url
    
    def get_base_happiness(self):
        url_2 = self.json_data['species']['url']
        json_data_2 = requests.get(url_2).json()
        base_happiness = json_data_2['base_happiness']
        return base_happiness

    def get_capture_rate(self):
        url_2 = self.json_data['species']['url']
        json_data_2 = requests.get(url_2).json()
        capture_rate = json_data_2['capture_rate']
        return capture_rate

def get_data(generation):
    """
    Calls get_all_pokemon function to get list of all pokemon belonging to specified generation.
    Loops through each pokemon to obtain the stats from PokeAPI
    """
    list_of_pokemon = get_all_pokemon(generation)

    # initialise empty lists
    all_name = []
    all_hp = []
    all_attack = []
    all_defense= []
    all_special_attack = []
    all_special_defense = []
    all_speed = []
    all_types = []
    all_base_exp = []
    all_height = []
    all_weight = []
    all_image_url = []
    all_base_happiness = []
    all_capture_rate = []

    # loop through each pokemon and store information in dataframe
    for pokemon in list_of_pokemon:
        url = "https://pokeapi.co/api/v2/pokemon/" + pokemon
        try:
            r = requests.get(url)
            json_data = r.json()
        except:
            print(f'Unable to fetch data for {pokemon}')
            continue

        pok = Pokemon(pokemon, json_data)
        stats = pok.get_stats()
        types = pok.get_types()
        base_exp = pok.get_base_exp()
        height = pok.get_height()
        weight = pok.get_weight()
        image_url = pok.get_image_url()
        base_happiness = pok.get_base_happiness()
        capture_rate = pok.get_capture_rate()

        all_name.append(pokemon)
        all_hp.append(stats['hp'])
        all_attack.append(stats['attack'])
        all_defense.append(stats['defense'])
        all_special_attack.append(stats['special-attack'])
        all_special_defense.append(stats['special-defense'])
        all_speed.append(stats['speed'])
        all_types.append(types)
        all_base_exp.append(base_exp)
        all_height.append(height)
        all_weight.append(weight)
        all_image_url.append(image_url)
        all_base_happiness.append(base_happiness)
        all_capture_rate.append(capture_rate)

    # write to dataframe
    df_pokemon = pd.DataFrame()
    df_pokemon['name'] = all_name
    df_pokemon['hp'] = all_hp
    df_pokemon['attack'] = all_attack
    df_pokemon['defense'] = all_defense
    df_pokemon['special_attack'] = all_special_attack
    df_pokemon['special_defense'] = all_special_defense
    df_pokemon['speed'] = all_speed
    df_pokemon['types'] = all_types
    df_pokemon['base_experience'] = all_base_exp
    df_pokemon['base_happiness'] = all_base_happiness
    df_pokemon['capture_rate'] = all_capture_rate
    df_pokemon['height'] = all_height
    df_pokemon['weight'] = all_weight
    df_pokemon['image_url'] = all_image_url

    return df_pokemon



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generation", 
        type=int, 
        help="Pokemon generation")
    args = parser.parse_args()

    df_pokemon = get_data(args.generation)

      # unlist "types" column
    df_pokemon = df_pokemon.assign(types=lambda df_: [', '.join(lst) for lst in df_.types])

    # filename
    filename = f"../data/df_pokemon_gen_{args.generation}.csv"
    # save to file
    df_pokemon.to_csv(filename, index=0)

    