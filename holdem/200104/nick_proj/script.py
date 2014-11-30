# link in relevant files and modules
from classes import Hand
from classes import HandRoster
from classes import Round
from pprint import pprint

# paths
HANDS_DATA = "../hdb"
ROSTER_DATA = "../hroster"

# Create dictionary of all hands. Note: can print an object using
# "pprint (vars(hand))"
hands = {}
hands_file = open(HANDS_DATA)
for line in hands_file:
    m = [s.replace("\n","") for s in line.split(" ") if s != ""]
    hand = Hand(int(m[0]),int(m[1]),int(m[2]),int(m[3]),int(m[4].split("/")[0]),
                    int(m[4].split("/")[1]),int(m[5].split("/")[0]),
                    int(m[5].split("/")[1]),int(m[6].split("/")[0]),
                    int(m[6].split("/")[1]),int(m[7].split("/")[0]),
                    int(m[7].split("/")[1]),m[8:])
    hands[hand.timestamp] = hand
hands_file.close()

# Create a dictionary of hand rosters
hand_rosters = {}
hand_roster_file = open(ROSTER_DATA)
for line in hand_roster_file:
    m = [s.replace("\n","") for s in line.split(" ") if s != ""]
    hand_roster = HandRoster(int(m[0]),int(m[1]),m[2:])
    hand_rosters[hand_roster.timestamp] = hand_roster
hand_roster_file.close()
