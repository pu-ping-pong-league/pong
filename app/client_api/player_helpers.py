import traceback

from app import app, db
from app.mod_api import models
from app.tools.pong_tools import *

def add_player(email, name, league_id):
    ''' Add player with given email and name to league with given league_id. '''
    try:
        league = models.League.get_league_by_id(int(league_id))
        player = models.Player(league, email, name)
        player.commit(insert=True)
        print(name, 'successfully added.')
    except:
        db.session.rollback()
        # traceback.print_exc()  
        return

def delete_player(email):
    ''' 
    Delete player with given email from their league.
    TODO: Ensure each player can be in only one or more than one leagues
          and adjust deletion logic accordingly.
    '''
    try:
        player = models.Player.get_player_by_email(email)
        name = player.name
        player.delete()
        print(name, 'successfully deleted.')
    except:
        db.session.rollback()
        # traceback.print_exc()  
        return

def print_player_stats(email):
    ''' Print stats of player with given email. '''
    try:
        player = models.Player.get_player_by_email(email)
        stats = dict(league=player.league.name, net_wins=player.net_wins, wins=player.matches_won, losses=player.matches_lost,
                     net_sets=player.net_sets, sets_won=player.sets_won, sets_lost=player.sets_lost, penalty_points=player.penalty_points, rating=player.rating)
        print('Player stats of', player.name, ':')
        for k,v in sorted(stats.iteritems()):
            print(k, '=', v)
    except:
        print('Invalid email. Please enter a valid email.')
        traceback.print_exc()  
        return   
