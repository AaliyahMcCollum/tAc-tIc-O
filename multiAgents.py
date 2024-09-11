from GameStatus_5120 import GameStatus


def minimax(game_state: GameStatus, depth: int, maximizingPlayer: bool, alpha=float('-inf'), beta=float('inf')):
    terminal = game_state.is_terminal()
    if (depth==0) or (terminal):
        newScores = game_state.get_scores(terminal)
        return newScores, None
    
    #using minimax to return the best movement
    if maximizingPlayer:
        value= float('-inf')
        for n in game_state.get_moves():
            child = game_state.get_new_state(n)
            tmp= minimax(child, depth-1, False, alpha, beta)[0]
            if tmp > value:
                value = tmp
                best_movement = n
            if tmp > game_state.oldScores:
                game_state.oldScores = tmp
            if beta <= value:
                break
            alpha= max(alpha, value)
            
    else: 
        value = float('inf')
        for n in game_state.get_moves():
            child = game_state.get_new_state(n)
            tmp = minimax(child, depth-1, True, alpha, beta)[0]
            if tmp < value:
                value = tmp
                best_movement = n
            if tmp < game_state.oldScores:
                game_state.oldScores = tmp
            if alpha >= value:
                break
            beta = min(beta, value)
            
    return value, best_movement
    

    

def negamax(game_status: GameStatus, depth: int, turn_multiplier: int, alpha=float('-inf'), beta=float('inf')):
    terminal = game_status.is_terminal()
    if (depth==0) or (terminal):
        scores = game_status.get_negamax_scores(terminal)
        return scores, None
    else:
        best_score = float('-inf')
        best_move = None
        for move in sorted(game_status.get_moves()):
            new_state = game_status.get_new_state(move)
            score, _ = negamax(new_state, depth - 1,2, -beta, -alpha)
            score = -score  # Negate the score
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
            if alpha >= beta:
                break
        return best_score, best_move
