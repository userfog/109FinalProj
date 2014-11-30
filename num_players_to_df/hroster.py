import os
import pandas as pd
import StringIO as sio
import io
import csv
import pprint
pp = pprint.PrettyPrinter(indent=8)

DEBUG = True

fp = open("log.txt", "w")

# Directories
DATA_ROOT = "C:/Users/Zachary/Downloads/finalprojcs109/109FInalProj/holdem/200104/"
DATA_HROSTER = DATA_ROOT + "hroster"
DATA_HDB = DATA_ROOT + "hdb"
DATA_PLAYER_ROOT = DATA_ROOT + "pdb/"
INVALID_CARD = "XX"

def name_to_file(name):
    return DATA_PLAYER_ROOT + "pdb." + name

# Columns
hroster_columns = ["timestamp", "num_players", "name1", "name2", "name3", "name4", "name5", "name6", "name7", "name8", "name9", "name10"]
hand_columns = ["timestamp", "dealer", "hand", "play", "flop", "turn", "river", "showdn", "board"]
player_columns = ["player", "timestamp", "play", "pos", "prflop", "flop", "turn", "river", "bankroll", "action", "winnings", "c1", "c2"]


def convert_pdb_to_csv(f):
    out = sio.StringIO()
    s = f.read().split('\n')
    for l in s:
        l = l.split()
        if len(l) == 11:
            l.extend([INVALID_CARD, INVALID_CARD])
        l = ",".join(l)
        if len(l) > 0:
            out.write(l + "\n")
    return out

def player_to_df(name):
    with open(name_to_file(name), "r") as plyr_file:
        c = convert_pdb_to_csv(plyr_file)
        return pd.read_csv(io.BytesIO(c.getvalue()), names=player_columns)

def player_hand(name, ts):
    plyr_df = player_to_df(name)
    plyr_df = plyr_df[plyr_df.timestamp == ts]
    if len(plyr_df) == 0 and DEBUG:
        fp.write("Name: " + name + " " + "Timestamp: " + str(ts) + "\n")
    return plyr_df
    
# Get a hand from a row of a DataFrame
def hand_from_roster(row):
    player_dataframes = pd.DataFrame(columns=player_columns)
    ts = row.timestamp
    num = row.num_players
    cols = ["name" + str(i) for i in xrange(1,num+1)]
    for idx, name in enumerate(cols):
        player = row[name]
        player_dataframes = player_dataframes.append(player_hand(player, ts))
    return player_dataframes


def num_players_to_df(df, num):
    target = df[df.num_players == num]
    l = len(target)
    print l
    hands = pd.DataFrame(columns=player_columns)
    for idx, row in target.iterrows():
        print idx
        hands = hands.append(hand_from_roster(row))
    return hands

def main():
    # Build hroster data frame
    hroster_df = None
    with open(DATA_HROSTER, "r") as roster:
        hroster_df = pd.read_csv(roster, names=hroster_columns, delim_whitespace=True)
    pp.pprint(num_players_to_df(hroster_df, 2).head())

if __name__ == '__main__':
    main()