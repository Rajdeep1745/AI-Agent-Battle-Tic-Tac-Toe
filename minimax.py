"""Minimax with alpha-beta pruning and measurable search statistics."""
from dataclasses import dataclass

@dataclass
class SearchStats:
    nodes: int=0
    pruned: int=0

def minimax(board, current, maximizing_player, depth, alpha, beta, evaluator, stats):
    stats.nodes += 1
    winner=board.check_winner()
    if winner==maximizing_player: return 100+depth
    if winner is not None: return -100-depth
    if board.is_draw(): return 0
    if depth==0: return evaluator(board,maximizing_player)

    moves=board.get_valid_moves()
    if current==maximizing_player:
        best=-float("inf")
        for move in moves:
            board.board[move]=current
            value=minimax(board, other(current), maximizing_player, depth-1, alpha,beta,evaluator,stats)
            board.board[move]=" "
            best=max(best,value); alpha=max(alpha,best)
            if beta<=alpha:
                stats.pruned += len(moves)-moves.index(move)-1
                break
        return best
    best=float("inf")
    for move in moves:
        board.board[move]=current
        value=minimax(board, other(current), maximizing_player, depth-1, alpha,beta,evaluator,stats)
        board.board[move]=" "
        best=min(best,value); beta=min(beta,best)
        if beta<=alpha:
            stats.pruned += len(moves)-moves.index(move)-1
            break
    return best

def other(player): return "O" if player=="X" else "X"
