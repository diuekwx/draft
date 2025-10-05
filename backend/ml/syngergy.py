from itertools import combinations
from collections import defaultdict
import numpy as np
import pandas as pd


df = pd.read_csv("matches.csv")

df = df.dropna(subset=["winners", "losers"])

def build_stats(df):
    pair_results = defaultdict(list)
    counter_results = defaultdict(list)

    for _, row in df.iterrows():
        winners = row["winners"].split(",")
        losers = row["losers"].split(",")

        for c1, c2 in combinations(sorted(winners), 2):
            pair_results[(c1, c2)].append(1)

        for c1, c2 in combinations(sorted(losers), 2):
            pair_results[(c1, c2)].append(0)

        for w in winners:
            for l in losers:
                counter_results[(w, l)].append(1)
                counter_results[(l, w)].append(0)

    pair_winrates = {pair: np.mean(outcomes) for pair, outcomes in pair_results.items()}
    counter_winrates = {pair: np.mean(outcomes) for pair, outcomes in counter_results.items()}
    return pair_winrates, counter_winrates

def get_synergy_score(team, pair_winrates):
    pairs = list(combinations(sorted(team), 2))
    scores = [pair_winrates.get((c1, c2), 0.5) for c1, c2 in pairs] 
    return np.mean(scores) if scores else 0.5

def get_counter_score(teamA, teamB, counter_winrates):
    scores = [counter_winrates.get((a, b), 0.5) for a in teamA for b in teamB]
    return np.mean(scores) if scores else 0.5

def encode_matches(df, champ_to_idx):
    X, y = [], []
    n_champs = len(champ_to_idx)

    for _, row in df.iterrows():
        winners = row["winners"].split(",")
        losers = row["losers"].split(",")

        win_team = np.zeros(n_champs)
        lose_team = np.zeros(n_champs)

        for champ in winners:
            if champ in champ_to_idx:
                win_team[champ_to_idx[champ]] = 1

        for champ in losers:
            if champ in champ_to_idx:
                lose_team[champ_to_idx[champ]] = 1

        features = np.concatenate([win_team, lose_team])
        X.append(features)
        y.append(1)  

        features_rev = np.concatenate([lose_team, win_team])
        X.append(features_rev)
        y.append(0)  

    return np.array(X), np.array(y)

def add_roles(input_csv, output_csv):
    roles = ["Top", "Jungle", "Mid", "ADC", "Support"]
    df = pd.read_csv(input_csv)
    df = df.dropna()
    new_rows = []
    
    for _, row in df.iterrows():
        winners = row["winners"].split(",")
        losers = row["losers"].split(",")
        
        if len(winners) == 5 and len(losers) == 5:
            winners_with_roles = [f"{champ}_{roles[i]}" for i, champ in enumerate(winners)]
            losers_with_roles = [f"{champ}_{roles[i]}" for i, champ in enumerate(losers)]
            
            new_rows.append({
                "id": row["id"],
                "winners": ",".join(winners_with_roles),
                "losers": ",".join(losers_with_roles)
            })
    
    new_df = pd.DataFrame(new_rows)
    new_df.to_csv(output_csv, index=False)
    print(f"doena")

if __name__ == "__main__":
    add_roles("matches.csv", "matches_roles.csv")