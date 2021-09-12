from DB import select


def find_roster(trainer_name):
    query = 'select name from pokemon join owned_by on id_pokemon=id where id_trainer=(select id from trainer where ' \
            'name="{}") '.format(trainer_name)
    result = select(query)
    return [pokemon['name'] for pokemon in result]
