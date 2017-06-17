from app.mod_api import models
from general_purpose_tools import *

def match_em(league, players, unmatched_player_id):
	if unmatched_player_id:
        # add player to the beginning of players list
        unmatched_player_id = None

    players_len = len(players)
    if players_len % 2 == 0:
        players_middle = players_len / 2  
        for i in range(players_middle):
            player1_id = players[i]['player_id']
            player2_id = players[i + players_middle]['player_id']
            new_match = models.Match(league.league_id, league.round_count, player1_id, player2_id)
            new_match.commit(insert=True)
    else: 
        players_middle = players_len / 2 + 1
        unmatched_player_id = players[players_middle - 1]['player_id']
        for i in range(players_middle - 1):
            player1_id = players[i]['player_id']
            player2_id = players[i + players_middle]['player_id']
            new_match = models.Match(league.league_id, league.round_count, player1_id, player2_id)
            new_match.commit(insert=True)

    return unmatched_player_id

def format_matches(matches):
	formatted_matches = list()
    for match in matches:
        formatted_match = dict()
        formatted_match['Match_id'] = match.match_id
        formatted_match['Player1_id'] = match.player1
        formatted_match['Player2_id'] = match.player2
        formatted_match['Player1'] = models.Player.get_player_by_id(matches.player1).name
        formatted_match['Player2'] = models.Player.get_player_by_id(matches.player2).name if not match.player2 else 'Bye'
        formatted_match['Score_player1'] = match.score_player1
        formatted_match['Score_player2'] = match.score_player2
        formatted_matches.append(formatted_match) 

    return formatted_matches

def export_matches(league_id, round_count):
    # fetch and format matches for export
    order = Player.match_id.asc()
    matches = models.Match.query.filter_by(league=league_id, round_count=round_count).order_by(order)    
    formatted_matches = format_matches(matches)

    league = models.League.get_league_by_id(league_id).name
    csv_name = league + ' - Matches Round ' + str(round_count) + '.csv'
    keys = ['Match_id', 'Player1_id', 'Player2_id', 'Player1', 'Player2', 'Score_player1', 'Score_player2']
    csv_export(csv_name, formatted_matches, keys)

def process_results(results_csv):
    # create and add players to the league
    with open(resuts_csv, 'rb') as csvfile:
        matches_reader = csv.Dictreader(csvfile)
        for row in matches_reader:
            match = models.Match.get_match_by_id(row['Match_id'])
            match.update_score(row['Score_player1'], row['Score_player2'])
            player1 = models.Player.get_player_by_id(row['Player1_id'])
            player1.update_stats(row['Score_player1'])
            player2 = models.Player.get_player_by_id(row['Player2_id'])
            player2.update_stats(row['Score_player2'])

