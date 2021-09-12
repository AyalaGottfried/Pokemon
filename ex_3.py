from DB import select


def find_owners(pokemon_name):
    query = 'select name from trainer join owned_by on id_trainer=id where id_pokemon=(select id from pokemon where ' \
            'name="{}") '.format(pokemon_name)
    result = select(query)
    return [pokemon['name'] for pokemon in result]
