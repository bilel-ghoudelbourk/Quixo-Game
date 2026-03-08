from Jeu import Jeu
from VueJeu import VueJeu
from ControllerJeu import ControllerJeu

if __name__ == "__main__":
    jeu = Jeu(is_ai=True, ai_symbol="O")
    vue = VueJeu(jeu)
    controller = ControllerJeu(jeu, vue)
    vue.start()
