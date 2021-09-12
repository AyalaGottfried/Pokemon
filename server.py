import json

import pymysql
import requests
from flask import Flask, Response, request

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

from DB import insert, delete, select, update
from ex_2 import find_by_type
from ex_3 import find_owners
from ex_4 import find_roster

app = Flask(__name__)


@app.route("/pokemons/<trainer>")
def get_pokemon_by_trainer(trainer):
    return Response(json.dumps(find_roster(trainer)), status=200)


@app.route("/trainers/<pokemon>")
def get_trainers_of_a_pokemon(pokemon):
    return Response(json.dumps(find_owners(pokemon)), status=200)


@app.route("/pokemons", methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()
    try:
        insert(
            'insert into pokemon values({},"{}","{}",{})'.format(pokemon["id"], pokemon["name"], pokemon["height"],
                                                                 pokemon["weight"]))
        for type in pokemon["types"]:
            insert('insert into types (pokemon_id, name) values ({},"{}")'.format(pokemon["id"], type))
    except KeyError as e:
        return Response(e.args[0] + " required", status=400)
    except pymysql.err.IntegrityError as e:
        return Response("this pokemon id is exist", status=409)
    return Response(status=200)


@app.route("/pokemons/get_by_type/<pokemon_type>")
def get_pokemons_by_type(pokemon_type):
    return Response(json.dumps(find_by_type(pokemon_type)), status=200)


@app.route("/pokemons/<pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    delete('DELETE FROM pokemon WHERE id={}'.format(pokemon_id))
    return Response(status=200)


@app.route("/pokemons/<trainer>", methods=["DELETE"])
def delete_pokemon_by_trainer(trainer):
    query = f'select id_pokemon from owned_by where id_trainer=(select id from trainer where name="{trainer}") '
    result = select(query)
    for pokemon_id in result:
        insert('DELETE FROM pokemon WHERE id={}'.format(pokemon_id['id_pokemon']))
    return Response(status=200)


@app.route("/pokemons/types/<pokemon_name>", methods=["PUT"])
def update_pokemon_types(pokemon_name):
    url = 'http://pokeapi.co/api/v2/pokemon/{}'.format(pokemon_name)
    res = requests.get(url, verify=False).json()
    for t in res["types"]:
        try:
            insert('insert into types (pokemon_id, name) values ({},"{}")'.format(res["id"], t["type"]["name"]))
        except pymysql.err.IntegrityError:
            continue
    return Response(status=200)


@app.route("/evolve", methods=["PUT"])
def evolve():
    name = request.args.get("pokemon")
    url = 'http://pokeapi.co/api/v2/pokemon/{}'.format(name)
    res = requests.get(url, verify=False).json()
    url = res['species']['url']
    res = requests.get(url, verify=False).json()
    url = res['evolution_chain']['url']
    res = requests.get(url, verify=False).json()
    evolves_to = res['chain']['evolves_to']
    if len(evolves_to)==0:
        return Response("this pokemon can't evolve", status=400)
    new_name = evolves_to[0]['species']['name']

    id_pokemon = select("select id from pokemon where name='{}'".format(name))
    new_id_pokemon = select("select id from pokemon where name='{}'".format(new_name))
    trainer = select("select id from trainer where name='{}'".format(request.args.get("trainer")))
    if len(id_pokemon) == 0 or len(new_id_pokemon) == 0 or len(trainer) == 0:
        return Response("one of the details you pass is wrong", status=400)
    is_owned = select('SELECT * FROM owned_by WHERE id_trainer={} AND id_pokemon={}'.format(trainer[0]['id'], id_pokemon[0]['id']))
    if len(is_owned) == 0:
        return Response("this pokemon is not owned by this trainer", status=400)
    update('UPDATE owned_by SET id_pokemon={} WHERE id_trainer={} AND id_pokemon={}'.format(new_id_pokemon[0]['id'],
                                                                                            trainer[0]['id'],
                                                                                            id_pokemon[0]['id']))
    return Response(status=200)


if __name__ == "__main__":
    app.run(port=3000)
