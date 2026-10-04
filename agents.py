"""Named AI agents."""
import random
from minimax import minimax, SearchStats
from minimax import other

class Agent:
    def __init__(self,name,depth,evaluator):
        self.name=name; self.depth=depth; self.evaluator=evaluator

    def choose_move(self,game,player):
        stats=SearchStats(); best=-float("inf"); choices=[]
        for move in game.get_valid_moves():
            game.board[move]=player
            score=minimax(game,other(player),player,self.depth-1,-float("inf"),float("inf"),self.evaluator,stats)
            game.board[move]=" "
            if score>best: best=score; choices=[move]
            elif score==best: choices.append(move)
        return random.choice(choices),stats
