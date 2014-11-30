# link in relevant files and modules
from classes import Hand
from classes import HandRoster
from classes import Round
from pprint import pprint

# paths
HANDS_DATA = "../hdb"
ROSTER_DATA = "../hroster"
PLAYER_DATA = "../pdb/"

# Create dictionary of all hands. Note: can print an object using
# "pprint (vars(hand))".
# (key,value) = (timestamp,Hand)
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
# (key,value) = (timestamp,HandRoster)
hand_rosters = {}
hand_roster_file = open(ROSTER_DATA)
for line in hand_roster_file:
    m = [s.replace("\n","") for s in line.split(" ") if s != ""]
    hand_roster = HandRoster(int(m[0]),int(m[1]),m[2:])
    hand_rosters[hand_roster.timestamp] = hand_roster
hand_roster_file.close()

# Create a dictionary of rounds
# (key,value) = (timestamp + player_name,Round)
# Note: Reason for the try/except statements is because some of the data
# is inconsistent; this data is just skipped
rounds = {}
pdb_filenames = open("pdb_filenames.txt")
for pdb_filename in pdb_filenames:
    pdb_file_path = (PLAYER_DATA + pdb_filename).replace("\n","")
    pdb_file = open(pdb_file_path)
    for line in pdb_file:
        m = [s.replace("\n","") for s in line.split() if s != ""]
        try:
            round = Round(m[0],int(m[1]),int(m[2]),int(m[3]),m[4],m[5],
                          m[6],m[7],int(m[8]),int(m[9]),int(m[10]),m[11:])
            rounds[str(round.timestamp) + round.player] = round
        except:
            continue
    pdb_file.close()
pdb_filenames.close()

for elt in hands:
    print "Hand object"
    pprint (vars(hands[elt]))
    print ""
    break
for elt in hand_rosters:
    print "Hand Roster object"
    pprint (vars(hand_rosters[elt]))
    print ""
    break
for elt in rounds:
    print "Round object"
    pprint (vars(rounds[elt]))
    print ""
    break
