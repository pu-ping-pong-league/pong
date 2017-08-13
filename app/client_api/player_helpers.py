import traceback

from app import app, db
from app.mod_api import models
from app.tools.pong_tools import *

def add_player(email, name, league_id):
    try:
        league = models.League.get_league_by_id(int(league_id))
        player = models.Player(league, email, name)
        player.commit(insert=True)
        print name, 'successfully added.'
    except:
        db.session.rollback()
        # traceback.print_exc()  
        return

def delete_player(player_email):
    try:
        player = models.Player.get_player_by_email(player_email)
        name = player.name
        player.delete()
        print name, 'successfully deleted.'
    except:
        db.session.rollback()
        # traceback.print_exc()  
        return

def get_player_stats(player_email):
    try:
        player = models.Player.get_player_by_email(player_email)
        stats = dict(league=player.league.name, net_wins=player.net_wins, wins=player.matches_won, losses=player.matches_lost,
                     net_sets=player.net_sets, sets_won=player.sets_won, sets_lost=player.sets_lost, penalty_points=player.penalty_points, rating=player.rating)
        print '\nPlayer stats of', player.name, ':\n'
        for k,v in sorted(stats.iteritems()):
            print k, '=', v
    except:
        print 'Invalid email. Please enter a valid email.'
        traceback.print_exc()  
        return   

"""
Next steps: 
5) Handle Repeated Matchups
7) test for auto deletion based on penalty points
"""