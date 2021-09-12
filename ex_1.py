from DB import select


def heaviest_pokemon():
    query = 'select name from pokemon where weight = (select max(weight) from pokemon)'
    result = select(query)
    return result[0]['name']
