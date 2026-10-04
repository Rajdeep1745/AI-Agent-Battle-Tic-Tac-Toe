"""Depth study and alternating AI-vs-AI tournament."""
import csv, os, random, time
from game import TicTacToe
from agents import Agent
from heuristic import evaluate_h1,evaluate_h2

def play_game(first_agent,second_agent,depth_override=None):
    game=TicTacToe(); agents={"X":first_agent,"O":second_agent}
    nodes={first_agent.name:0,second_agent.name:0}; pruned={first_agent.name:0,second_agent.name:0}
    start=time.perf_counter(); player="X"; moves=0
    while not game.is_terminal():
        agent=agents[player]
        if depth_override is not None: agent=Agent(agent.name,depth_override,agent.evaluator)
        move,stats=agent.choose_move(game,player)
        game.make_move(move,player); moves+=1
        nodes[agent.name]+=stats.nodes; pruned[agent.name]+=stats.pruned
        player="O" if player=="X" else "X"
    elapsed=time.perf_counter()-start
    return {"winner":game.check_winner() or "DRAW","moves":moves,"nodes":nodes,"pruned":pruned,"time":elapsed}

def depth_experiment():
    rows=[]
    # Fixed H1 and X as the AI; opponent uses the same agent policy at each depth.
    for depth in (1,2,3,4):
        ai=Agent("DEPTH_AI",depth,evaluate_h1); opponent=Agent("OPPONENT",depth,evaluate_h1)
        outcomes=[]; total_nodes=total_pruned=0; total_time=0
        for i in range(20):
            first=ai if i%2==0 else opponent
            second=opponent if i%2==0 else ai
            result=play_game(first,second)
            outcomes.append("AI" if result["winner"]=="X" and first is ai or result["winner"]=="O" and second is ai else ("DRAW" if result["winner"]=="DRAW" else "OPPONENT"))
            total_nodes+=sum(result["nodes"].values()); total_pruned+=sum(result["pruned"].values()); total_time+=result["time"]
        rows.append({"depth":depth,"games":20,"ai_wins":outcomes.count("AI"),"opponent_wins":outcomes.count("OPPONENT"),"draws":outcomes.count("DRAW"),"avg_nodes_per_game":round(total_nodes/20,2),"avg_pruned_per_game":round(total_pruned/20,2),"avg_time_seconds":round(total_time/20,6)})
    return rows

def run_tournament():
    nexus=Agent("NEXUS",3,evaluate_h1); titan=Agent("TITAN",3,evaluate_h2); rows=[]
    for i in range(10):
        first,second=(nexus,titan) if i%2==0 else (titan,nexus)
        result=play_game(first,second)
        rows.append({"game":i+1,"first":first.name,"winner":result["winner"],"moves":result["moves"],
          "nexus_nodes":result["nodes"]["NEXUS"],"titan_nodes":result["nodes"]["TITAN"],
          "nexus_pruned":result["pruned"]["NEXUS"],"titan_pruned":result["pruned"]["TITAN"],
          "execution_time_seconds":round(result["time"],6)})
    return rows

def save_csv(path,rows):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)

def summarize(rows):
    return {"NEXUS wins":sum(r["winner"]=="NEXUS" for r in rows),"TITAN wins":sum(r["winner"]=="TITAN" for r in rows),
      "Draws":sum(r["winner"]=="DRAW" for r in rows),"Average moves":round(sum(r["moves"] for r in rows)/len(rows),2),
      "Average execution time (s)":round(sum(r["execution_time_seconds"] for r in rows)/len(rows),6)}

if __name__=="__main__":
    random.seed(42)
    depth=depth_experiment(); battle=run_tournament()
    save_csv("results/depth_experiment.csv",depth); save_csv("results/results.csv",battle)
    print("Depth experiment:")
    for row in depth: print(row)
    print("\nBattle summary:",summarize(battle))
    print("Saved results/depth_experiment.csv and results/results.csv")
