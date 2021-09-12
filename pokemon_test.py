import unittest

from ex_1 import heaviest_pokemon
from ex_2 import find_by_type
from ex_3 import find_owners
from ex_4 import find_roster
from ex_5 import finds_most_owned


class MyTestCase(unittest.TestCase):
    def test_query1(self):
        self.assertEqual("snorlax", heaviest_pokemon())

    def test_query2(self):
        self.assertListEqual(
            ["bulbasaur", "ivysaur", "venusaur", "oddish", "gloom", "vileplume", "bellsprout", "weepinbell",
             "victreebel", "exeggcute", "exeggutor", "tangela"], find_by_type("grass"))

    def test_query3(self):
        self.assertListEqual(["Misty", "Wallace", "Gary", "Plumeria"], find_owners("gengar"))

    def test_query4(self):
        self.assertListEqual(
            ["metapod", "raticate", "spearow", "pikachu", "machoke", "machamp", "weepinbell", "cloyster", "kabuto"],
            find_roster("Loga"))

    def test_query5(self):
        self.assertListEqual(["venusaur", "raticate"], finds_most_owned())


if __name__ == '__main__':
    unittest.main()
