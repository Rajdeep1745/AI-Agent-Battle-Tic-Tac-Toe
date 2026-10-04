"""Two comparable positional heuristics for Tic-Tac-Toe."""
from game import TicTacToe

def evaluate_h1(board, player):
    """Threat-focused: open two-in-a-row threats dominate."""
    opponent = "O" if player=="X" else "X"
    winner = board.check_winner()
    if winner==player: return 100
    if winner==opponent: return -100
    score=0
    for line in TicTacToe.WIN_LINES:
        cells=[board.board[i] for i in line]
        mine=cells.count(player); theirs=cells.count(opponent)
        if theirs==0:
            if mine==2: score+=12
            elif mine==1: score+=2
        if mine==0:
            if theirs==2: score-=12
            elif theirs==1: score-=2
    return score

def evaluate_h2(board, player):
    """Position-focused: combines threats with center and corner control."""
    opponent = "O" if player=="X" else "X"
    winner=board.check_winner()
    if winner==player: return 100
    if winner==opponent: return -100
    score=0
    for line in TicTacToe.WIN_LINES:
        cells=[board.board[i] for i in line]
        mine=cells.count(player); theirs=cells.count(opponent)
        if theirs==0:
            score += {1:2,2:10}.get(mine,0)
        if mine==0:
            score -= {1:2,2:10}.get(theirs,0)
    weights={4:5,0:3,2:3,6:3,8:3}
    for pos,w in weights.items():
        if board.board[pos]==player: score+=w
        elif board.board[pos]==opponent: score-=w
    return score
