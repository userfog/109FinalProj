import os
import pandas as pd
import StringIO as sio
import io
import csv
import pprint
import datetime
import collections
import copy
pp = pprint.PrettyPrinter(indent=8)

# Directories
DATA_ROOT = "C:/Users/Zachary/Downloads/finalprojcs109/109FInalProj/holdem/200104/"
DATA_HROSTER = DATA_ROOT + "hroster"
DATA_HDB = DATA_ROOT + "hdb"
DATA_PLAYER_ROOT = DATA_ROOT + "pdb/"
INVALID_CARD = "XX"
COLUMNS_NO_SHOWDOWN = 11
COLUMNS_SHOWDOWN = 13

DEBUG = True

fp = open("log.txt", "w")


# Columns
hroster_columns = ["timestamp", "num_players", "name1", "name2", "name3", "name4", "name5", "name6", "name7", "name8", "name9", "name10"]
hand_columns = ["timestamp", "dealer", "hand", "play", "flop", "turn", "river", "showdn", "board"]
player_columns = ["player", "timestamp", "play", "pos", "prflop", "flop", "turn", "river", "bankroll", "action", "winnings", "c1", "c2"]

class MyCache:
    def __init__(self, limit):
        # Limited number of accesses
        self.lim = limit
        self.name_to_dataframe = {}
        self.name_and_previous_access = {}

    def add(self, name, df):
        t = datetime.datetime.now()
        # If the name is not in the list and we have more information in the 
        if len(self.name_to_dataframe) > self.lim:
            m = min(y for y in self.name_and_previous_access.values())
            name_to_evict = [x for x,y in self.name_and_previous_access.iteritems() if y == m]

            del self.name_to_dataframe[name_to_evict]
            del self.name_and_previous_access[name_to_evict]

        self.name_and_previous_access[name] = t
        self.name_to_dataframe[name] = df

    def get(self, name, default=None):
        t = datetime.datetime.now()
        if name in self.name_to_dataframe:
            self.name_and_previous_access[name] = t
            return self.name_to_dataframe[name]
        return default

c = {}

# Check to make sure a given file has the correct number of columns
def broken_files(l):
    ret = []
    for name in l:
        h = open(name_to_file(name), "r").read().split("\n")
        del h[-1]
        h = [e.split() for e in h]
        for i, j in enumerate(h):
            if len(j) == COLUMNS_NO_SHOWDOWN:
                # Did not got to showdown
                continue
            if len(j) == COLUMNS_SHOWDOWN:
                # Went to Showdown
                continue
            else:
                ret.append(name + " " + str(i))
    return ret


# Given a root converts a players name to a file name
def name_to_file(name):
    return DATA_PLAYER_ROOT + "pdb." + name

# Given a file converts it to a stream of bytes
def convert_pdb_to_csv(f):
    out = sio.StringIO()
    s = f.read().split('\n')
    for l in s:
        l = l.split()
        if len(l) == COLUMNS_NO_SHOWDOWN:
            l.extend([INVALID_CARD, INVALID_CARD])
        l = ",".join(l)
        # Check to make sure this is not EOF
        if len(l) > 0:
            out.write(l + "\n")
    return out




# Given a player name return DataFrame
def player_to_df(name):
    try:
        df = c.get(name, -1)
        if type(df) != int:
            return df
        with open(name_to_file(name), "r") as plyr_file:
            my_csv = convert_pdb_to_csv(plyr_file)
            new_df = pd.read_csv(io.BytesIO(my_csv.getvalue()), names=player_columns)
            c[name] = new_df
            return c.get(name)
    except:
        # Error reading csv to DataFrame
        return -1

# Given a players name and a timestamp, get their play for the given timestamp
def player_hand(name, ts):
    plyr_df = player_to_df(name)

    # Error opening
    if type(plyr_df) == int and plyr_df == -1 and DEBUG:
        fp.write("Error Converting CSV to Dataframe\nName: " + name + " " + "Timestamp: " + str(ts) + "\n")
        return plyr_df

    plyr_df = plyr_df[plyr_df.timestamp == ts]
    
    # Error finding
    if len(plyr_df) == 0 and DEBUG:
        fp.write("Error Player on Roster but Timestamp not Found\nName: " + name + " " + "Timestamp: " + str(ts) + "\n")

    return plyr_df
    
# Get a hand from a row of a DataFrame
def hand_from_roster(row):
    player_dataframes = pd.DataFrame(columns=player_columns)
    ts = row.timestamp
    num = row.num_players
    cols = ["name" + str(i) for i in xrange(1,num+1)]
    for idx, name in enumerate(cols):
        player = row[name]
        p = player_hand(player, ts)
        # If there is an error opening a players file, throughout the entire round
        if type(p) == int and p == -1:
            if DEBUG:
                fp.write("Hand From Roster: Name: " + name + "Timestamp: " + str(ts) + "\n")
            return pd.DataFrame(columns=player_columns)
        # add individuals playe to hand
        player_dataframes = player_dataframes.append(p)
    return player_dataframes

# Given the roster dataframe and a number of players it will return all of the
# hands from the roster dataframe that include that number of players
def num_players_to_df(df, num):
    target = df[df.num_players == num]
    l = len(target)
    hands = pd.DataFrame(columns=player_columns)
    for idx, row in target.iterrows():
        hands = hands.append(hand_from_roster(row))
    return hands

def main():
    # make sure none of the files rows which are the wrong number of columns 
    if DEBUG:
        names = [el.replace("pdb.", "") for el in os.listdir(DATA_PLAYER_ROOT)]
        l = broken_files(names)
        if len(l) > 0:
            pp.pprint(l)
            return 1 

    # Build hroster data frame
    hroster_df = None
    with open(DATA_HROSTER, "r") as roster:
        hroster_df = pd.read_csv(roster, names=hroster_columns, delim_whitespace=True)

    # Get bounds
    min_num_players = hroster_df.num_players.min()
    max_num_players = hroster_df.num_players.max()

    # Generate CSVs for all possible number of players in a given hand
    for i in xrange(10, 11):
        print "Num Players = " + str(i)
        num_players_to_df(hroster_df, i).to_csv(("num_players_%d.csv" % i)) 

    # Success
    return 0

if __name__ == '__main__':
    main()