import pytest
from Plateau import Plateau
from PionFactory import PionFactory

def test_initialisation_plateau():
    plateau = Plateau()
    assert len(plateau.grid) == 5
    assert len(plateau.grid[0]) == 5
    
    # Vérifier que toutes les cases contiennent un pion vide
    for i in range(5):
        for j in range(5):
            assert plateau.get_pion(i, j).symbol() == " "

def test_place_pion_et_get_pion():
    plateau = Plateau()
    pion_x = PionFactory.create_pion("X")
    plateau.place_pion(2, 3, pion_x)
    
    assert plateau.get_pion(2, 3) is pion_x
    assert plateau.get_pion(2, 3).symbol() == "X"

def test_shift_insert_up():
    plateau = Plateau()
    pion_o1 = PionFactory.create_pion("O")
    pion_o2 = PionFactory.create_pion("O")
    plateau.place_pion(0, 0, pion_o1)
    plateau.place_pion(1, 0, pion_o2)
    
    nouveau_pion = PionFactory.create_pion("X")
    # Pousse depuis la position (2, 0) vers le haut
    plateau.shift_insert("up", 2, 0, nouveau_pion)
    
    # La ligne 0 descend à 1, la 1 descend à 2. La 0 reçoit le nouveau.
    assert plateau.get_pion(0, 0) is nouveau_pion
    assert plateau.get_pion(1, 0) is pion_o1
    assert plateau.get_pion(2, 0) is pion_o2

def test_shift_insert_down():
    plateau = Plateau()
    pion_x = PionFactory.create_pion("X")
    plateau.place_pion(4, 1, pion_x)
    
    nouveau_pion = PionFactory.create_pion("O")
    # Pousse depuis (2, 1) vers le bas
    plateau.shift_insert("down", 2, 1, nouveau_pion)
    
    # La ligne 4 remonte à 3, etc. Insertion à 4.
    assert plateau.get_pion(4, 1) is nouveau_pion
    assert plateau.get_pion(3, 1) is pion_x

def test_shift_insert_left():
    plateau = Plateau()
    pion_o = PionFactory.create_pion("O")
    plateau.place_pion(1, 0, pion_o)
    
    nouveau_pion = PionFactory.create_pion("X")
    plateau.shift_insert("left", 1, 2, nouveau_pion)
    
    assert plateau.get_pion(1, 0) is nouveau_pion
    assert plateau.get_pion(1, 1) is pion_o

def test_shift_insert_right():
    plateau = Plateau()
    pion_x = PionFactory.create_pion("X")
    plateau.place_pion(3, 4, pion_x)
    
    nouveau_pion = PionFactory.create_pion("O")
    plateau.shift_insert("right", 3, 2, nouveau_pion)
    
    assert plateau.get_pion(3, 4) is nouveau_pion
    assert plateau.get_pion(3, 3) is pion_x

def test_clone_plateau():
    plateau = Plateau()
    pion_x = PionFactory.create_pion("X")
    plateau.place_pion(2, 2, pion_x)
    
    clone_plateau = plateau.clone()
    
    assert clone_plateau is not plateau
    assert clone_plateau.get_pion(2, 2).symbol() == "X"
    # S'assurer que les pions sont bien des objets différents
    assert clone_plateau.get_pion(2, 2) is not plateau.get_pion(2, 2)
