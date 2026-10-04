"""Command-line entry point."""
import argparse, random
from game import TicTacToe
from agents import Agent
from heuristic import evaluate_h1,evaluate_h2
from experiment import depth_experiment,run_tournament,save_csv,summarize

def main():
    parser=argparse.ArgumentParser(description="AI Agent Battle: Tic-Tac-Toe")
    parser.add_argument("mode",choices=["depth","battle","play"],help="experiment to run")
    args=parser.parse_args(); random.seed(42)
    if args.mode=="depth":
        rows=depth_experiment(); save_csv("results/depth_experiment.csv",rows)
        for row in rows: print(row)
    elif args.mode=="battle":
        rows=run_tournament(); save_csv("results/results.csv",rows)
        for row in rows: print(row)
        print(summarize(rows))
    else:
        agents={"X":Agent("NEXUS",3,evaluate_h1),"O":Agent("TITAN",3,evaluate_h2)}
        game=TicTacToe(); player="X"
        while not game.is_terminal():
            game.display(); move,stats=agents[player].choose_move(game,player)
            print(f"{agents[player].name} chooses cell {move+1}; nodes={stats.nodes}, pruned={stats.pruned}")
            game.make_move(move,player); player="O" if player=="X" else "X"
        game.display(); print("Result:",game.check_winner() or "DRAW")
if __name__=="__main__": main()
