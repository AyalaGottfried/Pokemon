from DB import select


def find_by_type(pokemon_type):
    query = 'select distinct pokemon.name from pokemon join types on pokemon_id = id where types.name="{}"'.format(pokemon_type)
    result = select(query)
    return [pokemon['name'] for pokemon in result]
