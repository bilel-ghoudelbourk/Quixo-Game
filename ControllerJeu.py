from GameState import VictoryState, DrawState
from Joueur import Joueur
from Pion import PionX, PionO


class ControllerJeu:
    def __init__(self, jeu, vue):
        self.jeu = jeu
        self.vue = vue
        self.vue.set_controller(self)

    def play_turn(self, direction, x, y):
        res = self.jeu.play_turn(direction, x, y)
        self.vue.update_view()

        if type(res) is PionX or type(res) is PionO:
            self.vue.announce_winner(res.symbol())
        elif res is True:
            self.vue.announce_draw()

    def check_legal(self, direction, x, y):
        return self.jeu.check_legal(direction, x, y, None)
