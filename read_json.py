import json

import pymysql

from DB import insert, select


def read_json(path='file.json'):
    with open(path, 'r') as file:
        data = json.load(file)
        for pokemon in data:
            query = 'insert into {} values({},"{}",{},{})'.format('pokemon', pokemon["id"], pokemon["name"],
                                                                  pokemon["height"], pokemon["weight"])
            try:
                insert(query)
            except pymysql.err.IntegrityError:
                continue
            query = 'insert into types values({},"{}")'.format(pokemon["id"], pokemon["type"])
            try:
                insert(query)
            except pymysql.err.IntegrityError:
                pass
            for trainer in pokemon['ownedBy']:
                trainer_id = select(
                    "select id from trainer where name='{}' and town='{}'".format(trainer['name'], trainer['town']))
                if len(trainer_id) == 0:
                    query = 'insert into trainer(name,town) values("{}","{}")'.format(trainer['name'], trainer['town'])
                    insert(query)
                    trainer_id = select(
                        "select id from trainer where name='{}' and town='{}'".format(trainer['name'], trainer['town']))
                query = f'insert into owned_by values({pokemon["id"]},{trainer_id[0]["id"]})'
                insert(query)


if __name__ == "__main__":
    read_json()
