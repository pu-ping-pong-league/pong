import traceback

from app import app, db
from app.mod_api import models
from app.tools.pong_tools import *
from app.tools.general_purpose_tools import *


def create_league(league_csv):    
    # create league instance
    try:
        league_name = league_csv.split('.')[0] ## small back upon creation with non existent csv
        league = models.League(name=league_name)
        db.session.add(league)
  
        # create and add players to the league
        players = list()
        with open(league_csv, 'rb') as csvfile:
            # initialize league if csv loaded succesfully
            player_reader = csv.DictReader(csvfile)
            db.session.commit()
            print league_name, '--> initialized successfully'

            players_added = 0
            duplicate_entries_found = 0

            for row in player_reader:
                try:
                    validate_email(email=row['Email'], name=row['Full_Name'])
                    players.append(row)
                    player = models.Player(league=league, email=row['Email'], name=row['Full_Name'])
                    db.session.add(player)
                    db.session.commit()
                    players_added = players_added + 1
                # block duplicates
                except:
                    print row['Full_Name'], 'creation failed.'
                    db.session.rollback()
                    duplicate_entries_found = duplicate_entries_found + 1
                    # traceback.print_exc() 
    except:
        db.session.rollback()
        print league_name, '--> initialization failed'
        # traceback.print_exc()
        return

    print '------------------SUMMARY------------------'
    print 'Number of Players Initialized:', players_added
    print 'Number of Duplicate Entries:', duplicate_entries_found
    print '-------------------------------------------'   

    
def generate_matches(league_id, test=False):
    try:
        # fetch league and update round count
        league = models.League.get_league_by_id(league_id)
        if not test:
            league.round_count = league.round_count + 1            

        # update player stats and fetch players of league in descending order of net wins
        all_players = league.get_all_players_sorted()
        ref_points = all_players[0].net_wins
        min_points = all_players[-1].net_wins

        # first-middle matching
        unmatched_player = None
        while ref_points >= min_points:
            current_players = list()
            for i in range(len(all_players)):
                player_points = all_players[i].net_wins
                if player_points == ref_points:
                    current_players.append(all_players[i])
                elif player_points < ref_points:
                    break
            if current_players:
                unmatched_player = match_em(league, current_players, unmatched_player)
            ref_points = ref_points - 1

        # Case of odd number of players; generate bye match (no opponent)
        if unmatched_player:
            new_match = models.Match_(league, unmatched_player.name, app.config['BYE'])
            db.session.add(new_match)            

        export_matches(league)
        db.session.commit()
    except:
        db.session.rollback()
        print 'Failed to generate new matches for', league.name, 'round', league.round_count
        traceback.print_exc()  
        return


def generate_leaderboard(league_id, results_csv):
    try:
        league = models.League.get_league_by_id(league_id)
        process_results(results_csv)

        # generate leaderboard csv
        csv_name = league.name + ' - Leaderboard Round ' + str(league.round_count) + '.csv'
        league_players = league.get_all_players_sorted()
        format_players(league_players)
        keys = models.Player.key_fields()
        csv_export(csv_name, league_players, keys)
    except:
        db.session.rollback()
        print 'Failed to generate leaderboard for', league.name, 'round', league.round_count
        traceback.print_exc()  
        return

def delete_last_matches(league_id):
    try:
        league = models.League.get_league_by_id(league_id)
        target_matches = models.Match_.query.filter_by(league_id=league_id, round_count=league.round_count)
        for match in target_matches: 
            match.delete()
        league.round_count = league.round_count - 1
        league.commit()
    except:
        db.session.rollback()
        print 'Failed to delet last matches for', league.name, 'round', league.round_count
        traceback.print_exc()  
        return
