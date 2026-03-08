import pytest
from GameState import NormalState, DrawState, VictoryState
from Jeu import Jeu
from PionFactory import PionFactory

def test_normal_state_play_turn_illegal():
    jeu = Jeu()
    state = NormalState(jeu)
    jeu.set_state(state)
    
    # Coup illégal (ex: milieu du plateau)
    res = state.play_turn("up", 2, 2)
    assert res is False

def test_normal_state_play_turn_legal_continue():
    jeu = Jeu()
    state = NormalState(jeu)
    jeu.set_state(state)
    
    # Coup légal: 0, 0 avec X (Joueur 1 = indice 0)
    assert jeu.current_turn == 0
    res = state.play_turn("right", 0, 0)
    assert res is None # Le jeu continue
    assert jeu.current_turn == 1 # Au tour de O

def test_normal_state_play_turn_victory():
    jeu = Jeu()
    
    # On simule un plateau presque gagnant pour X sur la première ligne
    for j in range(1, 5):
        jeu.plateau.place_pion(0, j, PionFactory.create_pion("X"))
        
    state = NormalState(jeu)
    jeu.set_state(state)
    
    # X (tour 0) joue ("right", 0, 0). Ça pousse la ligne et ça gagne.
    res = state.play_turn("right", 0, 0)
    assert res is not None # Un vainqueur !
    assert res.symbol() == "X"
    # L'état change en VictoryState
    assert isinstance(jeu.game_state, VictoryState)
    assert jeu.game_state.play_turn("up", 0, 0) == res # VictoryState retourne tjs le vainqueur

def test_normal_state_play_turn_draw():
    jeu = Jeu()
    # On remplit le plateau sans que personne ne gagne
    # Pattern: X O X O X sur les lignes paires, O X O X O sur les impaires
    # Sauf qu'une telle grille forme des diagonales X ou O !
    # Essayons:
    # X O X O X
    # X O X O X
    # O X O X O
    # O X O X O
    # X O O X X -> Pour casser les colonnes et les diagonales
    
    grid_patterns = [
        ["X", "O", "O", "X", "O"],
        ["O", "X", "X", "O", "X"],
        ["X", "O", "O", "X", "O"],
        ["O", "X", "X", "O", "X"],
        ["X", "O", "X", "O", "O"], # Casse tout
    ]
    
    for i in range(5):
        for j in range(5):
            jeu.plateau.place_pion(i, j, PionFactory.create_pion(grid_patterns[i][j]))
            
    # Le plateau est plein. On libère (0, 0)
    jeu.plateau.place_pion(0, 0, PionFactory.create_pion(" ")) 
    state = NormalState(jeu)
    jeu.set_state(state)
    
    # Ca va faire Draw !
    res = state.play_turn("right", 0, 0)
    assert res is True # Indique Draw
    assert isinstance(jeu.game_state, DrawState)
    assert jeu.game_state.play_turn("up", 0, 0) is False # DrawState retourne False

def test_victory_state():
    jeu = Jeu()
    state = VictoryState(jeu)
    winner_mock = PionFactory.create_pion("X")
    state.set_winner(winner_mock)
    
    assert state.play_turn("up", 0, 0) == winner_mock

def test_draw_state():
    jeu = Jeu()
    state = DrawState(jeu)
    assert state.play_turn("up", 0, 0) is False

def test_gamestate_base_pass():
    from GameState import GameState
    jeu = Jeu()
    state = GameState(jeu)
    # Ligne 10 contient juste "pass"
    state.play_turn("up", 0, 0)
