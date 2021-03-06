from app.static_assets import messages    
from app.tools.general_purpose_tools import *

from app.client_api import league_helpers as lapi
from app.client_api import player_helpers as papi
from app.client_api import match_helpers as mapi

import traceback

def welcome():
    ''' 
    Provide welcome interface logic. 
    This is the top level main menu: 
    1: League Management
    2: Player Management
    3: Match Management
    4: Exit
    '''
    try:
        method = raw_input(messages.welcome)
        if method == '1':
            return 1
        elif method == '2':
            return 2
        elif method == '3':
            return 3
        elif method == '4':
            return -1
        else:
            return 0
    except:
        traceback.print_exc()
        return 0

def league_manage():
    ''' 
    Provide league management interface logic. 
    Options:
    1: Create a league
    2: Generate next round's matches
    3: Generate leaderboard
    4: Delete last round's matches
    5: Generate cross-league matches
    6: Back
    '''
    try:
        method = raw_input(messages.league_manage)
        if method == '1':
            print('Manually adjust full names and column names before submitting. Columns required: "Full_Name", "Email"')
            league_csv = raw_input('Enter league csv file name:')
            lapi.create_league(league_csv)
            return 1
        elif method == '2':
            league_id = raw_input('Enter league id:')
            lapi.generate_matches(league_id)
            return 1
        elif method == '3':
            league_id = raw_input('Enter league id:')
            results_csv = raw_input('Enter league csv file name:')
            lapi.generate_leaderboard(league_id, results_csv)
            return 1
        elif method == '4':
            league_id = raw_input('Enter league id:')
            lapi.delete_last_matches(league_id)
            return 1
        elif method == '5':
            league1_id = raw_input('Enter league 1 id:')
            league2_id = raw_input('Enter league 2 id:')
            lapi.generate_crossleague_matches(league1_id, league2_id)
            return 1
        elif method == '6':
            return 0
        else:
            return 1
    except:
        traceback.print_exc()
        return 1


def player_manage():
    ''' 
    Provide player management interface logic. 
    Options:
    1: Add a Player
    2: Delete a Player
    3: Get Player Stats
    4: Back
    '''
    try:
        method = raw_input(messages.player_manage)
        if method == '1':
            email = raw_input("Enter player's email:")
            validate_email(email)
            name = raw_input("Enter player's full name:")
            league_id = raw_input("Enter league's id:")
            papi.add_player(email, name, league_id)
            return 2
        elif method == '2':
            email = raw_input("Enter player's email:")
            papi.delete_player(email)
            return 2
        elif method == '3':
            email = raw_input("Enter player's email:")
            papi.print_player_stats(email)
            return 2
        elif method == '4':
            return 0
        else:
            return 2
    except:
        # traceback.print_exc()
        return 2

def match_manage():
    ''' 
    Provide match management interface logic. 
    Options:
    1: Update a Match
    2: Adjust Match Result
    3: Back
    '''
    try:
        method = raw_input(messages.match_manage)
        if method == '1':
            match_id = int(raw_input("Enter match id:"))
            mapi.print_match_details(match_id)

            email_p1 = raw_input("Enter New Player 1 Email:")
            email_p2 = raw_input("Enter New Player 2 Email:")
            mapi.update_match(match_id, email_p1, email_p2)

            return 3
        elif method == '2':
            match_id = int(raw_input("Enter match id:"))
            mapi.print_match_details(match_id)

            score_p1 = raw_input("Enter Score Player 1:")
            score_p2 = raw_input("Enter Score Player 2:")
            mapi.adjust_result(match_id, int(score_p1), int(score_p2))

            return 3
        elif method == '3':
            return 0
        else:
            return 3
    except:
        traceback.print_exc()
        return 3
