from DB import select


def finds_most_owned():
    query = 'select name from pokemon join owned_by on id_pokemon = id group by id_pokemon having count(id_trainer)  \
            >= all (select count(id_trainer) from owned_by group by id_pokemon) '
    result = select(query)
    return [pokemon["name"] for pokemon in result]
