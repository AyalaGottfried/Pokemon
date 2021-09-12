import unittest

import requests


class PokemonTest(unittest.TestCase):
    def test_get_pokemons_by_type(self):
        url = "http://127.0.0.1:3000/pokemons"
        data = {
            "id": 563,
            "name": "eevee",
            "types": ["big", "normal"],
            "weight": 80,
            "height": 80
        }
        requests.post(url, json=data)
        url = "http://127.0.0.1:3000/pokemons/get_by_type/normal"
        res = requests.get(url).json()
        self.assertIn("eevee", res)
        url = "http://127.0.0.1:3000/pokemons/types/563"
        res = requests.put(url)
        self.assertEqual(200, res.status_code)

    def test_add_pokemon(self):
        url = 'http://127.0.0.1:3000/pokemons'
        data = {
            "id": 193,
            "name": 'yanma',
            "types": ['bug', 'flying'],
            "weight": 380,
            "height": 12
        }

        requests.post(url=url, json=data)

        url = 'http://127.0.0.1:3000/pokemons/get_by_type/bug'
        res = requests.get(url=url).json()
        self.assertIn('yanma', res)
        url = 'http://127.0.0.1:3000/pokemons/get_by_type/flying'
        res = requests.get(url=url).json()
        self.assertIn('yanma', res)

    def test_get_pokemons_by_owner(self):
        url = 'http://127.0.0.1:3000/pokemons/Drasna'
        res = requests.get(url=url).json()
        correct = ["wartortle", "caterpie", "beedrill", "arbok", "clefairy", "wigglytuff", "persian", "growlithe",
                   "machamp", "golem", "dodrio", "hypno", "cubone", "eevee", "kabutops"]
        self.assertListEqual(res, correct)

    def test_update_pokemon_types(self):
        url = "http://127.0.0.1:3000/pokemons"
        data = {"id": 3, "name": "venusaur", "height": 20, "weight": 1000, "types": []}
        requests.post(url, json=data)
        url = "http://127.0.0.1:3000/pokemons/types/venusaur"
        requests.put(url)
        url = "http://127.0.0.1:3000/pokemons/get_by_type/poison"
        res = requests.get(url).json()
        self.assertIn("venusaur", res)
        url = "http://127.0.0.1:3000/pokemons/get_by_type/grass"
        res = requests.get(url).json()
        self.assertIn("venusaur", res)

    def test_get_owners_of_a_pokemon(self):
        url = "http://127.0.0.1:3000/trainers/charmander"
        res = requests.get(url).json()
        for i in ["Giovanni", "Jasmine", "Whitney"]:
            self.assertIn(i, res)

    def test_evolve(self):
        url = 'http://127.0.0.1:3000/evolve?pokemon=pinsir&trainer=Whitney'
        res = requests.put(url=url)
        self.assertEqual(b"this pokemon can't evolve", res.content)
        url = 'http://127.0.0.1:3000/evolve?pokemon=spearow&trainer=Archie'
        res = requests.put(url=url)
        self.assertEqual(b"this pokemon is not owned by this trainer", res.content)
        url = 'http://127.0.0.1:3000/evolve?pokemon=oddish&trainer=Whitney'
        res = requests.put(url=url)
        self.assertEqual(200, res.status_code)
        res = requests.put(url=url)
        self.assertEqual(400, res.status_code)
        url = 'http://127.0.0.1:3000/pokemons/Whitney'
        res = requests.get(url=url).json()
        self.assertIn('gloom', res)
        self.assertIn('pikachu', res)
        self.assertIn('raichu', res)
        url = 'http://127.0.0.1:3000/evolve?pokemon=pikachu&trainer=Whitney'
        res = requests.put(url=url)
        self.assertEqual(200, res.status_code)

