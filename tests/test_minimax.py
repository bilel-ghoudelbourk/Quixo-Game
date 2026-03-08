import pytest
from Minimax import evaluate_board, get_best_move
from Jeu import Jeu
from PionFactory import PionFactory
import math

def test_evaluate_board():
    jeu = Jeu()
    
    assert evaluate_board(jeu, "X") == 0
    
    jeu.plateau.place_pion(0, 0, PionFactory.create_pion("X"))
    score_x = evaluate_board(jeu, "X")
    assert score_x > 0
    score_o = evaluate_board(jeu, "O")
    assert score_o < 0

def test_evaluate_board_victory():
    jeu = Jeu()
    for i in range(5):
        jeu.plateau.place_pion(0, i, PionFactory.create_pion("X"))
        
    score_x = evaluate_board(jeu, "X")
    assert score_x >= 100000

def test_get_best_move_first_turn():
    jeu = Jeu()
    move, eval_val = get_best_move(jeu, 1, -math.inf, math.inf, True, "X")
    assert move is not None
    # Il va trouver un coup légal

def test_get_best_move_victory_state():
    jeu = Jeu()
    for i in range(5):
        jeu.plateau.place_pion(i, i, PionFactory.create_pion("O"))
    
    jeu.check_victory() # Ca ne met pas à jour le state tout seul dans ce test isolé
    # On force la State
    from GameState import VictoryState
    state = VictoryState(jeu)
    state.set_winner(PionFactory.create_pion("O"))
    jeu.set_state(state)
    
    # L'ia joue O, c'est censé retourner grand
    move, eval_val = get_best_move(jeu, 1, -math.inf, math.inf, True, "O")
    assert eval_val >= 1000000
    assert move is None
    
    # L'ia joue X (donc a perdu)
    move, eval_val = get_best_move(jeu, 1, -math.inf, math.inf, True, "X")
    assert eval_val <= -1000000

def test_get_best_move_draw_state():
    jeu = Jeu()
    from GameState import DrawState
    jeu.set_state(DrawState(jeu))
    
    move, eval_val = get_best_move(jeu, 1, -math.inf, math.inf, True, "X")
    assert eval_val == 0
    assert move is None
    
def test_get_best_move_maximizing_minimizing():
    jeu = Jeu()
    # On joue quelques coups pour voir si min/max retourne bien une tuple
    move_max, eval_max = get_best_move(jeu, 2, -math.inf, math.inf, True, "X")
    assert move_max is not None
    
    move_min, eval_min = get_best_move(jeu, 1, -math.inf, math.inf, False, "X")
    assert move_min is not None

def test_evaluate_opp_victory():
    jeu = Jeu()
    for i in range(5):
        jeu.plateau.place_pion(0, i, PionFactory.create_pion("O"))
    
    # En tant que X, voir les 5 de O
    score = evaluate_board(jeu, "X")
    assert score <= -100000

def test_no_legal_moves():
    jeu = Jeu()
    # On simule l'absence de coups (bien que normalement impossible sauf cas pathologiques)
    jeu.get_legal_moves = lambda joueur: [] # Mock très rapide
    
    move, val = get_best_move(jeu, 1, -math.inf, math.inf, True, "X")
    assert move is None

def test_alpha_beta_pruning():
    jeu = Jeu()
    # Forcer l'élagage dans la branche 'Maximizing'
    # En donnant un 'beta' très bas, dès que l'IA trouve un coup avec un score normal (autour de 0), 
    # alpha devient 0, et 0 >= -1000, danc ça coupe (break).
    get_best_move(jeu, 1, -math.inf, -1000, True, "X")
    
    # Forcer l'élagage dans la branche 'Minimizing'
    # En donnant un 'alpha' très haut, dès que l'IA trouve un coup de score normal (0),
    # beta devient 0, et 0 <= 1000, donc ça coupe (break).
    get_best_move(jeu, 1, 1000, math.inf, False, "X")
