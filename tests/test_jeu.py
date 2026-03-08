import pytest
from Jeu import Jeu
from PionFactory import PionFactory
from Pion import PionO, PionX

def test_initialisation_jeu():
    jeu = Jeu()
    assert jeu.current_turn == 0
    assert jeu.game_over is False
    assert len(jeu.joueurs) == 2
    assert jeu.joueurs[0].symbol == "X"
    assert jeu.joueurs[1].symbol == "O"

def test_check_legal_milieu_plateau():
    jeu = Jeu()
    pion = PionFactory.create_pion("X")
    # Tenter de jouer au milieu du plateau (interdit dans Quixo, on ne prend que sur les bords)
    assert not jeu.check_legal("up", 2, 2, pion)
    assert not jeu.check_legal("down", 1, 1, pion)

def test_check_legal_bord_plateau():
    jeu = Jeu()
    pion = PionFactory.create_pion("X")
    
    # Prendre sur un bord avec un pion vide est légal (si on remplace par notre pion)
    assert jeu.check_legal("right", 0, 0, pion)
    assert jeu.check_legal("left", 4, 4, pion)
    
    # Prendre un pion adverse n'est pas permis (si (0,0) est O, on ne peut pas le prendre avec X)
    pion_adverse = PionFactory.create_pion("O")
    jeu.plateau.place_pion(0, 0, pion_adverse)
    assert not jeu.check_legal("right", 0, 0, pion)

def test_check_victory_horizontal():
    jeu = Jeu()
    pion_x = PionFactory.create_pion("X")
    
    # Ligne 2 pleine de X
    for j in range(5):
        jeu.plateau.place_pion(2, j, pion_x)
        
    vainqueur = jeu.check_victory()
    assert vainqueur is not None
    assert vainqueur.symbol() == "X"

def test_check_victory_vertical():
    jeu = Jeu()
    pion_o = PionFactory.create_pion("O")
    
    # Colonne 3 pleine de O
    for i in range(5):
        jeu.plateau.place_pion(i, 3, pion_o)
        
    vainqueur = jeu.check_victory()
    assert vainqueur is not None
    assert vainqueur.symbol() == "O"

def test_check_victory_diagonal():
    jeu = Jeu()
    pion_x = PionFactory.create_pion("X")
    
    # Diagonale principale pleine de X
    for i in range(5):
        jeu.plateau.place_pion(i, i, pion_x)
        
    vainqueur = jeu.check_victory()
    assert vainqueur is not None
    assert vainqueur.symbol() == "X"

def test_check_draw():
    jeu = Jeu()
    pion_x = PionFactory.create_pion("X")
    
    # Remplir le plateau avec des X pour simuler un plateau plein
    for i in range(5):
        for j in range(5):
            jeu.plateau.place_pion(i, j, pion_x)
            
    assert jeu.check_draw() is True
    
    # Vider une case
    pion_vide = PionFactory.create_pion(" ")
    jeu.plateau.place_pion(0, 0, pion_vide)
    assert jeu.check_draw() is False

def test_jeu_clone():
    jeu = Jeu()
    jeu.plateau.place_pion(0, 0, PionFactory.create_pion("X"))
    jeu.current_turn = 1
    
    clone_jeu = jeu.clone()
    assert clone_jeu is not jeu
    assert clone_jeu.plateau is not jeu.plateau
    assert clone_jeu.current_turn == 1
    assert clone_jeu.plateau.get_pion(0, 0).symbol() == "X"

def test_jeu_play_turn_direct():
    jeu = Jeu()
    res = jeu.play_turn("right", 0, 0)
    assert res is None

def test_get_legal_moves():
    jeu = Jeu()
    moves = jeu.get_legal_moves(jeu.joueurs[0])
    # Total de cases bordures = 16. Chaque case a 3 directions valides d'insertion, 
    # Moins les combinaisons impossibles (ex: right depuis j=0 est invalide ? Non left depuis 0 est invalide)
    assert len(moves) > 0
    # Le coin 0,0 
    assert ("down", 0, 0) not in moves  # Pousser vers le bas modifie bien, oui, mais c'est "up" qui est ignoré
    
    # Ex: on ne peut pas push down depuis la ligne 0 car "down" signifie insérer par le haut et sortir par le bas, 
    # la règle dit que (i == 0 and d == "down") est ignoré dans check_legal logic loop de l'application
    pass

def test_reset_game():
    jeu = Jeu()
    jeu.plateau.place_pion(0, 0, PionFactory.create_pion("X"))
    jeu.current_turn = 1
    jeu.game_over = True
    
    jeu.reset_game()
    assert jeu.current_turn == 0
    assert jeu.game_over is False
    assert jeu.plateau.get_pion(0, 0).symbol() == " "
