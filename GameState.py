from PionFactory import PionFactory


class GameState:
    def __init__(self, jeu):
        self.jeu = jeu
        self.winner = None

    def play_turn(self, direction, x, y):
        pass

    def set_winner(self, winner):
        self.winner = winner


class DrawState(GameState):
    def play_turn(self, direction, x, y):
        return False


class NormalState(GameState):
    def play_turn(self, direction, x, y):
        current_player = self.jeu.joueurs[self.jeu.current_turn]
        pion = PionFactory.create_pion(current_player.symbol)

        # print(self.jeu.check_legal(direction, x, y, pion))
        if not self.jeu.check_legal(direction, x, y, pion):
            return False

        self.jeu.plateau.shift_insert(direction, x, y, pion)

        winner = self.jeu.check_victory()

        if winner is not None:
            victory_state = VictoryState(self.jeu)
            victory_state.set_winner(winner)
            self.jeu.set_state(victory_state)
            return winner

        if self.jeu.check_draw():
            self.jeu.set_state(DrawState(self.jeu))
            return True

        self.jeu.current_turn = 1 - self.jeu.current_turn
        return None


class VictoryState(GameState):
    def play_turn(self, direction, x, y):
        return self.winner
