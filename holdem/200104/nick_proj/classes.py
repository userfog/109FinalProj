class Hand:
    """Defines a class for a hand. All of the information comes from 
       a row in the hdb file"""
    def __init__(self,timestamp,dealer,game_num,
                 num_players_dealt_cards,num_players_flop,
                 pot_size_flop,num_players_turn,pot_size_turn,
                 num_players_river,pot_size_river,
                 num_players_showdn,pot_size_showdn,board):
        self.timestamp = timestamp
        self.dealer = dealer
        self.game_num = game_num
        self.num_players_dealt_cards = num_players_dealt_cards
        self.num_players_flop = num_players_flop
        self.pot_size_flop = pot_size_flop
        self.num_players_turn = num_players_turn
        self.pot_size_turn = pot_size_turn
        self.num_players_river = num_players_river
        self.pot_size_river = pot_size_river
        self.num_players_showdn = num_players_showdn
        self.pot_size_showdn = pot_size_showdn
        self.board = board

class WinningHand(Hand):
    """Defines a class for a hand. All of the information comes from
       a row in the hdb file. Should only be used to store data regarding
       hands that won!""" 

class HandRoster:
    """Defines a class for a hand roster. All of the information comes
       from a single row in hroster; essentially shows who played for
       each round, aka timestamp (a unique integer)"""
    def __init__(self,timestamp,num_players,player_nicknames):
        self.timestamp = timestamp
        self.num_players = num_players
        self.player_nicknames = player_nicknames

class Round:
    """Defines a class for a round. All of the information comes from
       a single row in a pdb. file; essentially shows all information
       regarding a particular player made for a particular round, aka 
       timestamp (a unique integer)"""
    def __init__(self,player,timestamp,num_players_dealt_cards,
                 player_pos,bet_action_preflop,bet_action_flop,
                 bet_action_turn,bet_action_river,start_bankroll,
                 total_action,pot_amount_won,showdn_cards):
        self.player = player
        self.timestamp = timestamp
        self.num_players_dealt_cards = num_players_dealt_cards     
        self.player_pos = player_pos
        self.bet_action_preflop = bet_action_preflop
        self.bet_action_flop = bet_action_flop
        self.bet_action_turn = bet_action_turn
        self.bet_action_river = bet_action_river
        self.start_bankroll = start_bankroll
        self.total_action = total_action
        self.pot_amount_won = pot_amount_won
        self.showdn_cards = showdn_cards
