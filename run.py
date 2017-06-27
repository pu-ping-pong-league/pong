from app.static_assets import messages    
from app.pong_client import *
from app.tools.general_purpose_tools import *

import traceback

def welcome():
    try:
        method = raw_input(messages.welcome)
        if method == '1':
            return 1
        elif method == '2':
            return 2
        elif method == '3':
            return -1
        else:
            return 0
    except:
        traceback.print_exc()
        return 0

def league_manage():
    try:
        method = raw_input(messages.league_manage)
        if method == '1':
            print 'Manually adjust full names and column names before submitting. Columns required: "Full_Name", "Email"'
            league_csv = raw_input("Enter league's csv file name:")
            create_league(league_csv)
            return 1
        elif method == '2':
            league_id = raw_input("Enter league's id:")
            generate_matches(league_id)
            return 1
        elif method == '3':
            league_id = raw_input("Enter league's id:")
            results_csv = raw_input("Enter results csv file name:")
            generate_leaderboard(league_id, results_csv)
            return 1
        elif method == '4':
            league_id = raw_input("Enter league's id:")
            delete_last_matches(league_id)
            return 0
        elif method == '5':
            return 0
        else:
            return 1
    except:
        traceback.print_exc()
        return 1


def player_manage():
    try:
        method = raw_input(messages.player_manage)
        if method == '1':
            email = raw_input("Enter player's email:")
            validate_email(email)
            name = raw_input("Enter player's full name:")
            league_id = raw_input("Enter league's id:")
            add_player(email, name, league_id)
            return 2
        elif method == '2':
            email = raw_input("Enter player's email:")
            delete_player(email)
            return 2
        elif method == '3':
            email = raw_input("Enter player's email:")
            get_player_stats(email)
            return 2
        elif method == '4':
            return 0
        else:
            return 2
    except:
        # traceback.print_exc()
        return 2

def dfs(state):
    while(state <= 2 and state >= 0):
        if state == 0:
            state = welcome()
        elif state == 1:
            state = league_manage()
        elif state == 2:
            state = player_manage()
    exit()

dfs(0)