import traceback

from app import app, db
from app.mod_api import models

def print_match_details(match_id):
    try:
        match = models.Match_.get_match_by_id(match_id)
        print(models.League.get_league_by_id(match.league_id).name, '- Round', match.round_count)
        print(match.player1_name, '-', match.player2_name)
        print('Score:', match.score_player1, '-', match.score_player2, '\n')
    except:
        print('Match with given match_id could not be fetched.')
        raise

def update_match(match_id, email_p1, email_p2):
    try:    
        match = models.Match_.get_match_by_id(match_id)

        # fetch players
        player1 = models.Player.get_player_by_email(email_p1)
        player2 = models.Player.get_player_by_email(email_p2)
        old_player1 = models.Player.get_player_by_name(match.player1_name)
        old_player2 = models.Player.get_player_by_name(match.player2_name)

        # update match if players found
        if player1 is not None and player2 is not None:            
            match.player1_name = player1.name
            match.player2_name = player2.name
            match.commit()

            # update player_stats
            player1.update_stats()
            player2.update_stats()
            old_player1.update_stats()
            old_player2.update_stats()

            print('\n')
            print_match_details(match_id)
        else:
            db.session.rollback()
            print('Players with given email not identified.')
            return
    except:
        db.session.rollback()
        traceback.print_exc()
        return

def adjust_result(match_id, score_p1, score_p2):
    try:    
        match = models.Match_.get_match_by_id(match_id)

        # update match if found
        if match is not None:  
            match.update_score(match.player1_name, match.player2_name, score_p1, score_p2)

            print('\n')
            print_match_details(match_id)
        else:
            db.session.rollback()
            print('Match not identified.')
            return
    except:
        db.session.rollback()
        traceback.print_exc()
        return



"""
Next steps: 
5) Handle Repeated Matchups
7) test for auto deletion based on penalty points
"""