import pytest
from Joueur import Joueur

def test_joueur_initialization():
    j = Joueur("X")
    assert j.symbol == "X"
