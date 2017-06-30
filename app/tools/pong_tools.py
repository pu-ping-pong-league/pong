from app.mod_api import models
from general_purpose_tools import *

from app import db

def match_em(league, players, unmatched_player):
    # handle potential unmatched player
    if unmatched_player:
        players = [unmatched_player] + players
        unmatched_player = None

    # generate matches usin cut in the middle and overlap format
    players_len = len(players)
    if players_len % 2 == 0:
        players_middle = players_len / 2  
        for i in range(players_middle):
            player1 = players[i].name
            player2 = players[i + players_middle].name
            new_match = models.Match_(league, player1, player2)
            db.session.add(new_match)
    else: 
        players_middle = players_len / 2 + 1
        unmatched_player = players[players_middle - 1]
        for i in range(players_middle - 1):
            player1 = players[i].name
            player2 = players[i + players_middle].name
            new_match = models.Match_(league, player1, player2)
            db.session.add(new_match)

    return unmatched_player

def format_matches(matches):
    formatted_matches = list()
    for match in matches:
        formatted_match = dict()
        formatted_match['Match Id'] = match.match_id
        formatted_match['Player 1'] = match.player1_name
        formatted_match['Player 2'] = match.player2_name
        formatted_match['Score Player 1'] = match.score_player1
        formatted_match['Score Player 2'] = match.score_player2
        formatted_matches.append(formatted_match) 

    return formatted_matches

def export_matches(league):
    # fetch and format matches for csv export
    matches = league.get_ordered_matches_for_round(league.round_count)
    formatted_matches = format_matches(matches)

    csv_name = league.name + ' - Fixtures Round ' + str(league.round_count) + '.csv'
    keys = ['Match Id', 'Player 1', 'Player 2', 'Score Player 1', 'Score Player 2']
    csv_export(csv_name, formatted_matches, keys)

def process_results(results_csv):
    # create and add players to the league
    with open(resuts_csv, 'rb') as csvfile:
        matches_reader = csv.Dictreader(csvfile)
        for row in matches_reader:
            match = models.Match_.get_match_by_id(row['Match_id'])
            match.update_score(row['Score_player1'], row['Score_player2'])
            player1 = models.Player.get_player_by_id(row['Player1_id'])
            player1.update_stats(row['Score_player1'])
            player2 = models.Player.get_player_by_id(row['Player2_id'])
            player2.update_stats(row['Score_player2'])

