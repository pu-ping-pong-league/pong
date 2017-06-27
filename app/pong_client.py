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
                validate_email(email=row['Email'], name=row['Full_Name'])
                players.append(row)
                player = models.Player(league=league, email=row['Email'], name=row['Full_Name'])
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
    try:
        league = models.League.get_league_by_id(int(league_id))
        player = models.Player(league, email, name)
        player.commit(insert=True)
        print name, 'successfully added.'
    except:
        db.session.rollback()
        traceback.print_exc()  
        return

def delete_player(player_email):
    try:
        player = models.Player.get_player_by_email(player_email)
        name = player.name
        player.delete()
        print name, 'successfully deleted.'
    except:
        db.session.rollback()
        traceback.print_exc()  
        return

def get_player_stats(player_email):
    try:
        player = models.Player.get_player_by_email(player_email)
        stats = dict(league=player.league.name, victories=player.games_won, losses=player.games_lost,
                     sets_won=player.sets_won, sets_lost=player.sets_lost, penalty_points=player.penalty_points, rating=player.rating)
        print '\nPlayer stats of', player.name, ':\n'
        for k,v in sorted(stats.iteritems()):
            print k, '=', v
    except:
        print 'Invalid email. Please enter a valid email.'
        # traceback.print_exc()  
        return    





# Debt:
# adjust repeated matches 
# retain matches when player quits the league --> check sqlalchemy signature for foreign keys
# add ssh key to github
# elo system