from dotenv import load_dotenv
import os
import requests
import pandas as pd
import time
from requests.exceptions import ConnectionError, Timeout

load_dotenv()

API_KEY = os.getenv("RIOT_API_KEY")

session = requests.Session()
session.headers.update({"X-Riot-Token": API_KEY})

def get_ids_noob(region, queue, tier, division):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}"
    res = session.get(url).json()
    players = []
    for player in res:
        players.append(player.get("puuid"))
    return players

def get_ids_masters(region, queue):
    url = f"https://{region}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queue}"
    res = session.get(url).json().get("entries")

    players = []
    for player in res:
        players.append(player.get("puuid"))
    return players

def get_matches(region, puuid):
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
    payload = {"count": 5}
    res = session.get(url, params=payload)
    return res.json()


def get_results_robust(region, matchId):

    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchId}"
    while True: # my chungus ass internet man
        try:
            res = session.get(url, timeout=10) 

            if res.status_code == 200:
                data = res.json()
                players = data.get("info", {}).get("participants", [])
                if not players:
                    print(f"Match {matchId} had no participant data. Skipping.")
                    return None

                match_data = {
                    "id": matchId,
                    "winners": ",".join([p.get("championName") for p in players if p.get("win")]),
                    "losers": ",".join([p.get("championName") for p in players if not p.get("win")])
                }
                return match_data
        
            elif res.status_code in [404, 403]:
                print(f"Permanent error for match {matchId}: Status {res.status_code}. Skipping.")
                return None
            # freaking requests brah    
            else:
                print(f"API Error for {matchId}: Status {res.status_code}. Retrying in 5 seconds...")
                time.sleep(5)

        except (ConnectionError, Timeout):
            time.sleep(15)

if __name__ == "__main__":
    REGION = "americas"
    REGION2 = "na1"
    
    CSV_FILE_PATH = "matches.csv"
    CSV_HEADERS = ["id", "winners", "losers"]

    if not os.path.exists(CSV_FILE_PATH):
        pd.DataFrame(columns=CSV_HEADERS).to_csv(CSV_FILE_PATH, index=False)
        print("Created matches.csv with headers.")

    matches = set()
    # ids = get_ids_noob(REGION2, "RANKED_SOLO_5x5", "DIAMOND", "I")
    ids = get_ids_masters(REGION2, "RANKED_SOLO_5x5")
    print(f" {len(ids)} playes")
    
    for i, id in enumerate(ids):
        player_match = get_matches(REGION, id)
        if isinstance(player_match, list):
            print(f"match: {i}")
            matches.update(player_match)
        time.sleep(1.2)

    print(f"matches {len(matches)}")
    

    
    for i, match_id in enumerate(list(matches)):
        print(f"match {i+1}/{len(matches)}: {match_id}")
        
        data = get_results_robust(REGION, match_id)
        
        if data:

            df_row = pd.DataFrame([data]) 
            
            df_row.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            print(f"saved {match_id} to CSV.")
        
        time.sleep(1.2)

    print("\nDONE!!!")