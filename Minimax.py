import math
import GameConfig
from GameState import VictoryState, DrawState

def evaluate_board(jeu, current_symbol):
    score = 0
    opponent_symbol = "O" if current_symbol == "X" else "X"

    def evaluate_line(line):
        my_count = sum(1 for pion in line if pion.symbol() == current_symbol)
        opp_count = sum(1 for pion in line if pion.symbol() == opponent_symbol)
        
        if my_count == 5:
            return 100000
        elif opp_count == 5:
            return -100000
        
        if my_count > 0 and opp_count == 0:
            return 10 ** my_count
        elif opp_count > 0 and my_count == 0:
            return -(10 ** opp_count)
        return 0

    for i in range(GameConfig.TAILLE_PLATEAU):
        row = [jeu.plateau.get_pion(i, j) for j in range(GameConfig.TAILLE_PLATEAU)]
        col = [jeu.plateau.get_pion(j, i) for j in range(GameConfig.TAILLE_PLATEAU)]
        score += evaluate_line(row)
        score += evaluate_line(col)

    diag1 = [jeu.plateau.get_pion(i, i) for i in range(GameConfig.TAILLE_PLATEAU)]
    diag2 = [jeu.plateau.get_pion(i, GameConfig.TAILLE_PLATEAU - 1 - i) for i in range(GameConfig.TAILLE_PLATEAU)]
    score += evaluate_line(diag1)
    score += evaluate_line(diag2)

    return score

def get_best_move(jeu, depth, alpha, beta, is_maximizing, ai_symbol):
    if type(jeu.game_state) is VictoryState:
        if jeu.game_state.winner.symbol() == ai_symbol:
            return None, 1000000
        else:
            return None, -1000000
    
    if type(jeu.game_state) is DrawState:
        return None, 0
    
    if depth == 0:
        return None, evaluate_board(jeu, ai_symbol)

    current_player = jeu.joueurs[jeu.current_turn]
    legal_moves = jeu.get_legal_moves(current_player)

    if len(legal_moves) == 0:
        return None, evaluate_board(jeu, ai_symbol)

    best_move = None

    if is_maximizing:
        max_eval = -math.inf
        for move in legal_moves:
            simulated_jeu = jeu.clone()
            simulated_jeu.play_turn(move[0], move[1], move[2])
            
            _, eval = get_best_move(simulated_jeu, depth - 1, alpha, beta, False, ai_symbol)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = math.inf
        for move in legal_moves:
            simulated_jeu = jeu.clone()
            simulated_jeu.play_turn(move[0], move[1], move[2])
            
            _, eval = get_best_move(simulated_jeu, depth - 1, alpha, beta, True, ai_symbol)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move, min_eval
