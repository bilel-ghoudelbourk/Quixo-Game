from Plateau import Plateau
from Joueur import Joueur
from GameState import NormalState
from Pion import PionVide
from PionFactory import PionFactory
import GameConfig


class Jeu:
    def __init__(self, is_ai=False, ai_symbol="O"):
        self.is_ai = is_ai
        self.ai_symbol = ai_symbol
        self.plateau = Plateau()
        self.joueurs = [Joueur("X"), Joueur("O")]
        self.current_turn = 0
        self.game_over = False
        self.game_state = NormalState(self)

    def set_state(self, state):
        self.game_state = state

    def clone(self):
        new_jeu = Jeu()
        new_jeu.plateau = self.plateau.clone()
        new_jeu.current_turn = self.current_turn
        new_jeu.game_over = self.game_over
        # the players do not store state other than their symbol, it's safe to recreate
        new_jeu.joueurs = [Joueur("X"), Joueur("O")]
        # To avoid circular imports and complex cloning, the state logic on clone is
        # kept strictly to NormalState for Minimax calculation.
        from GameState import NormalState
        new_jeu.game_state = NormalState(new_jeu)
        return new_jeu

    def play_turn(self, direction, x, y):
        return self.game_state.play_turn(direction, x, y)

    def check_legal(self, direction, x, y, pion):

        if 0 < x < GameConfig.TAILLE_PLATEAU - 1 and 0 < y < GameConfig.TAILLE_PLATEAU - 1:
            return False

        if pion is not None and not type(self.plateau.grid[x][y]) is PionVide and not type(
                self.plateau.grid[x][y]) is type(pion):
            return False
        return True

    def get_legal_moves(self, current_joueur):
        moves = []
        directions = ["up", "down", "left", "right"]
        for i in range(GameConfig.TAILLE_PLATEAU):
            for j in range(GameConfig.TAILLE_PLATEAU):
                # only border pieces
                if i == 0 or i == GameConfig.TAILLE_PLATEAU - 1 or j == 0 or j == GameConfig.TAILLE_PLATEAU - 1:
                    if type(self.plateau.get_pion(i, j)) is PionVide or self.plateau.get_pion(i, j).symbol() == current_joueur.symbol:
                        pion_to_simulate = PionFactory.create_pion(current_joueur.symbol)
                        for d in directions:
                            if self.check_legal(d, i, j, pion_to_simulate):
                                # Some directions are impossible from certain edges (like "up" from the top row isn't practically useful if the piece is already there and we try to insert from bottom etc)
                                # But the logic in check_legal/play_turn handles the generic shift.
                                # Let's just generate all and if play_turn returns False we ignore it.
                                # Actually check_legal handles the basic rules, the shift itself is valid if it's a border.
                                # So just add the move.
                                # But it's illegal to push in the opposite direction of the extraction if it doesn't change anything
                                # E.g. pulling from left and inserting on the left (direction="right")
                                if (j == 0 and d == "right") or \
                                   (j == GameConfig.TAILLE_PLATEAU - 1 and d == "left") or \
                                   (i == 0 and d == "down") or \
                                   (i == GameConfig.TAILLE_PLATEAU - 1 and d == "up"):
                                    continue
                                moves.append((d, i, j))
        return moves

    def check_victory(self):
        for i in range(GameConfig.TAILLE_PLATEAU):
            # Check lignes et colones
            row = [self.plateau.get_pion(i, j) for j in range(GameConfig.TAILLE_PLATEAU)]
            col = [self.plateau.get_pion(j, i) for j in range(GameConfig.TAILLE_PLATEAU)]
            if self.check_line(row) or self.check_line(col):
                return row[0] if self.check_line(row) else col[0]

        # Check diagonals
        diag1 = [self.plateau.get_pion(i, i) for i in range(GameConfig.TAILLE_PLATEAU)]
        diag2 = [self.plateau.get_pion(i, GameConfig.TAILLE_PLATEAU - 1 - i) for i in range(GameConfig.TAILLE_PLATEAU)]
        if self.check_line(diag1) or self.check_line(diag2):
            return diag1[0] if self.check_line(diag1) else diag2[0]
        return None

    def check_line(self, line):
        symbols = [pion.symbol() for pion in line]
        return symbols[0] != " " and all(symbol == symbols[0] for symbol in symbols)

    def check_draw(self):
        for i in range(GameConfig.TAILLE_PLATEAU):
            for j in range(GameConfig.TAILLE_PLATEAU):
                if type(self.plateau.get_pion(i, j)) is PionVide:
                    return False
        return True

    def reset_game(self):
        self.plateau = Plateau()
        self.joueurs = [Joueur("X"), Joueur("O")]
        self.current_turn = 0
        self.game_over = False
        self.game_state = NormalState(self)
