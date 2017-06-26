import traceback

from app import db
from mod_api import models
from tools.pong_tools import *
from tools.general_purpose_tools import *


def create_league(league_csv):    
    # create league instance
    try:
        league_name = league_csv.split('.')[0]
        league = models.League(name=league_name)
        db.session.add(league)
        db.session.commit()
    except:
        db.session.rollback()
        traceback.print_exc()
        return

    # create and add players to the league
    players = list()
    with open(league_csv, 'rb') as csvfile:
        player_reader = csv.DictReader(csvfile)
        for row in player_reader:
            try:
                players.append(row)
                player = models.Player(league_id=league, email=row['Email'], name=row['Full_Name'])
                db.session.add(player)
                db.session.commit()
            # block duplicates
            except:
                print row['Full_Name'], 'failed.'
                db.session.rollback()
                # traceback.print_exc()            

    print players

def generate_matches(league_id, test=False):
    # fetch league and update round count
    league = models.League.get_league_by_id(league_id)
    if not test:
        league.round_count = league.round_count + 1
        self.commit()
    league.commit()

    order = models.Player.net_wins.desc()
    all_players = models.Player.query.filter_by(league=league_id).order_by(order).all() 

    count = len(all_players)
    max_wins = all_players[0]['net_wins']
    
    # first-middle matching
    unmatched_player_id = None
    order = models.Player.net_sets.desc()
    while count > 0:
        players = models.Player.query.filter_by(league=league_id, net_wins=wins).order_by(order).all()
        unmatched_player_id = match_em(league, players, unmatched_player_id)
        count = count - players_len
        wins = wins - 1

    # Bye case
    if unmatched_player_id:
        new_match = models.Match(league.league_id, league.round_count, unmatched_player_id, None)
        new_match.commit(insert=True)

    export_matches(league_id, league.round_count)

def generate_leaderboard(league_id, results_csv):
    process_results(results_csv)
    league = models.League.get_league_by_id(league_id)

    # generate leaderboard csv
    csv_name = league.name + ' - Leaderboard Round ' + str(league.round_count) + '.csv'
    order = models.Player.net_wins.desc()
    league_players = models.Player.query.filter_by(league=league_id).order_by(order).all() # figure out how to order by two parameters
    keys = models.Player.key_fields()
    csv_export(csv_name, league_players, keys)

def delete_last_matches(league_id):
    league = models.League.get_league_by_id(league_id)
    target_matches = models.Match.query.filter_by(league=league_id, round_count=round_count)
    for match in target_matches: 
        match.delete()

def add_player(email, name, league_id):
    player = models.Player(row['Email'], row['Full_Name'], league.league_id)
    player.commit()

def delete_player(player_email):
    player = models.Player.query.filter_by(email=player_email).first()
    player.delete()






# TO DO:
# adjust repeated matches 
# retain matches when player quits the league --> check sqlalchemy signature for foreign keys
# add ssh key to github
# build a client main to run upon execution
# elo system
# add error statements