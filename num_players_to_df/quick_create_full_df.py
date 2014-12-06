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

player_columns = ["player", "timestamp", "play", "pos", "prflop", "flop", "turn", "river", "bankroll", "action", "winnings", "c1", "c2", "num_players"]

def main():
	full = pd.DataFrame(columns=player_columns)
	for i in xrange(2, 11):
	    print "Num Players = " + str(i)
	    helper = pd.read_csv(("num_players_%d.csv" % i)) 
	    helper["num_players"] = [i]*len(helper)
	    full = full.append(helper)
	full.to_csv("all_players.csv")

if __name__ == '__main__':
	main()