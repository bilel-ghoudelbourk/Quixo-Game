import pytest
from Jeu import Jeu
from ControllerJeu import ControllerJeu
from Pion import PionX, PionO

class MockVue:
    def __init__(self):
        self.controller = None
        self.updated = False
        self.winner = None
        self.drawn = False
        
    def set_controller(self, controller):
        self.controller = controller
        
    def update_view(self):
        self.updated = True
        
    def announce_winner(self, winner_symbol):
        self.winner = winner_symbol
        
    def announce_draw(self):
        self.drawn = True

def test_controller_initialization():
    jeu = Jeu()
    vue = MockVue()
    ctrl = ControllerJeu(jeu, vue)
    assert ctrl.jeu is jeu
    assert ctrl.vue is vue
    assert vue.controller is ctrl

def test_controller_check_legal():
    jeu = Jeu()
    vue = MockVue()
    ctrl = ControllerJeu(jeu, vue)
    
    # Coup légal aux bords avec pion vide
    assert ctrl.check_legal("right", 0, 0) is True
    # Coup illégal (milieu)
    assert ctrl.check_legal("up", 2, 2) is False

def test_controller_play_turn():
    jeu = Jeu()
    vue = MockVue()
    ctrl = ControllerJeu(jeu, vue)
    
    ctrl.play_turn("right", 0, 0)
    assert vue.updated is True
    assert vue.winner is None
    assert vue.drawn is False

def test_controller_play_turn_winner():
    jeu = Jeu()
    vue = MockVue()
    ctrl = ControllerJeu(jeu, vue)
    
    for j in range(1, 5):
        jeu.plateau.place_pion(0, j, PionX())
        
    ctrl.play_turn("right", 0, 0)
    assert vue.updated is True
    assert vue.winner == "X"
    assert vue.drawn is False

def test_controller_play_turn_draw():
    jeu = Jeu()
    vue = MockVue()
    ctrl = ControllerJeu(jeu, vue)
    
    grid_patterns = [
        ["X", "O", "O", "X", "O"],
        ["O", "X", "X", "O", "X"],
        ["X", "O", "O", "X", "O"],
        ["O", "X", "X", "O", "X"],
        ["X", "O", "X", "O", "O"], 
    ]
    for i in range(5):
        for j in range(5):
            jeu.plateau.place_pion(i, j, PionX() if grid_patterns[i][j] == "X" else PionO())
            
    jeu.plateau.place_pion(0, 0, PionX().__class__.__bases__[0]()) # PionVide n'est pas importable dans ControllerJeu tel quel mais on peut vider la case via la propriété de base ou un autre biais. 
    # Mieux : on réimporte l'usine pour vider
    
    from PionFactory import PionFactory
    jeu.plateau.place_pion(0, 0, PionFactory.create_pion(" ")) 
    
    ctrl.play_turn("right", 0, 0)
    assert vue.updated is True
    assert vue.drawn is True
