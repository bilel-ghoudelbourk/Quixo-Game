import pytest
from PionFactory import PionFactory
from Pion import PionO, PionX, PionVide

def test_create_pion_o():
    p = PionFactory.create_pion("O")
    assert isinstance(p, PionO)

def test_create_pion_x():
    p = PionFactory.create_pion("X")
    assert isinstance(p, PionX)

def test_create_pion_vide():
    p = PionFactory.create_pion(" ")
    assert isinstance(p, PionVide)
    
    # Test d'un cas par défaut
    p_defaut = PionFactory.create_pion("N'importe quoi")
    assert isinstance(p_defaut, PionVide)
