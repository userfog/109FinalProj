import os
import pandas as pd

# Directories
DATA_ROOT = "../holdem/200104/"
DATA_HROSTER = DATA_ROOT + "hroster"
DATA_HDB = DATA_ROOT + "hdb"
DATA_PLAYER_ROOT = DATA_ROOT + "pdb/"

def name_to_file(name):
    return DATA_PLAYER_ROOT + "pdb." + name

# Columns
hroster_columns = ["timestamp", "num_players", "name1", "name2", "name3", "name4", "name5", "name6", "name7", "name8", "name9", "name10"]
hand_columns = ["timestamp", "dealer", "hand", "play", "flop", "turn", "river", "showdn", "board"]
player_columns = ["player", "timestamp", "play", "pos", "prflop", "flop", "turn", "river", "bankroll", "action", "winnings", "cards"]

    
# Get a hand from a row of a DataFrame
def hand_from_roster(row):
    player_dataframes = []
    ts = row.timestamp
    num = row.num_players
    cols = ["name" + str(i) for i in xrange(1,num+1)]
    print cols
    for name in cols:
        player = row[name]
        print player
        with open(name_to_file(player), "r") as plyr_file:
            plyr_df = pd.read_csv(plyr_file, names=player_columns, delim_whitespace=True) 
            plyr_df = plyr_df[plyr_df.timestamp == ts]
            player_dataframes.append(plyr_df)
    # Failing with Memory error wtf
    d = pd.concat(player_dataframes)
    print d.head(n=5)
    return d


def num_players_to_df(df, num):
    target = df[df.num_players == num]
    print target.head()
    # return target.apply(hand_from_roster, axis=1)
    hands = []
    for idx, row in target.iterrows():
        hands.append(hand_from_roster(row))
    return pd.concat(hands)


def main():
    # Build hroster data frame
    hroster_df = None
    with open(DATA_HROSTER, "r") as roster:
        hroster_df = pd.read_csv(roster, names=hroster_columns, delim_whitespace=True)
    # hroster_df.head()
    print "alive"
    print num_players_to_df(hroster_df, 2).head()
    print "Made it"
        


if __name__ == '__main__':
    main()
            