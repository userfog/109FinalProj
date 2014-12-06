# link in relevant files and modules
from classes import Hand
from classes import HandRoster
from classes import Round
from pprint import pprint

# paths to files
HANDS_DATA = "../hdb"
ROSTER_DATA = "../hroster"
PLAYER_DATA = "../pdb/"


def get_data():
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
    # (key,value) = (timestamp,[data for each player at table])
    # Note: Reason for the try/except statements is because some of the data
    # is inconsistent; that data is just skipped
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
                if round.timestamp in rounds:
                    rounds[round.timestamp].append(round)
                else:
                    rounds[round.timestamp] = [round]
            except:
                continue
        pdb_file.close()
    pdb_filenames.close()

    # Create a dictionary of winning rounds
    # At the end, we filter to get only rounds where we know what cards
    # the player won the round with
    winning_rounds = {}
    for ts in rounds:
        for round in rounds[ts]:
            if round.pot_amount_won > 0:
                winning_rounds[ts] = round
                if ts in hands:            
                    winning_rounds[ts].board = hands[ts].board
                break
    winning_rounds = {r: winning_rounds[r] for r in winning_rounds if winning_rounds[r].showdn_cards != []}
    return [hands, hand_rosters, rounds, winning_rounds]

# Create dictionary of hands and their profit
# (c=clover,h=heart,d=diamond,s=spade)
# e.g. keys would be (2c,2h),(2c,2d),(2s,2h),(2s,2d),(2c,2s),(2h,2d)
