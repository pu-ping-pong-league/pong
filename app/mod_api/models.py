from sqlalchemy import and_, func, case, desc, or_
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app import app, db

class League(db.Model):
    league_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    round_count = db.Column(db.Integer, nullable=False, default=0)
    players = db.relationship('Player', backref='league', lazy='dynamic')
    # matches = db.relationship('Match', backref='league', lazy='dynamic')
    
    def __init__(self, name):
        self.name = name

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_all_players_sorted(self):
        all_players = Player.query.filter_by(league_id=self.league_id).all()
        for player in all_players:
            player.update_stats()
        return Player.query.filter_by(league_id=self.league_id).order_by(Player.net_wins.desc(), Player.net_sets.desc()).all()

    def get_ordered_matches_for_round(self, round_count):
        order = Match_.match_id.asc()
        return Match_.query.filter_by(league_id=self.league_id, round_count=round_count).order_by(order) 

    @staticmethod
    def get_league_by_id(league_id):
        return League.query.filter_by(league_id=league_id).first()

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    matches_won = db.Column(db.Integer, nullable=False, default=0)
    matches_lost = db.Column(db.Integer, nullable=False, default=0)
    sets_won = db.Column(db.Integer, nullable=False, default=0)
    sets_lost = db.Column(db.Integer, nullable=False, default=0)
    penalty_points = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=1000)
  
    @hybrid_property
    def net_wins(self):
        return self.matches_won - self.matches_lost

    @hybrid_property
    def net_sets(self):
        return self.sets_won - self.sets_lost

    def __init__(self, league, email, name):
        self.league = league
        self.email = email
        self.name = name        

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_stats(self):
        # check if player is above the penalty points limit
        penalty_points = self.get_penalty_points()
        if penalty_points >= app.config['PENALTY_THRESHOLD']:
            print self.email
            self.delete()
        else:
            # update player stats
            self.penalty_points = penalty_points
            player_stats = self.get_stats()
            self.matches_won = player_stats[0]
            self.matches_lost = player_stats[1]
            self.sets_won = player_stats[2]
            self.sets_lost = player_stats[3]
            self.commit()

    def get_stats(self):
        matches_won = 0
        matches_lost = 0
        sets_won = 0
        sets_lost = 0

        # match stats when player is player 1
        matches_p1 = Match_.query.filter_by(player1_name=self.name, completed=True).all()
        for match in matches_p1:
            # check if match has been played
            if (match.score_player1 + match.score_player2) > 0:
                if match.score_player1 == app.config['VICTORY']:
                    matches_won = matches_won + 1
                else:
                    matches_lost = matches_lost + 1
                sets_won = sets_won + match.score_player1
                sets_lost = sets_lost + match.score_player2

        # match stats when player is player 2
        matches_p2 = Match_.query.filter_by(player2_name=self.name, completed=True).all()
        for match in matches_p2:
            # check if match has been played
            if (match.score_player1 + match.score_player2) > 0:
                if match.score_player2 == app.config['VICTORY']:
                    matches_won = matches_won + 1
                else:
                    matches_lost = matches_lost + 1
                sets_won = sets_won + match.score_player2
                sets_lost = sets_lost + match.score_player1        

        points = matches_won - matches_lost
        net_sets = sets_won - sets_lost
        return [matches_won, matches_lost, sets_won, sets_lost]         

    def get_penalty_points(self):
        penalty_points = 0
        matches = Match_.query.filter(and_(or_(Match_.player1_name==self.name, Match_.player2_name==self.name), Match_.completed)).all()
        for match in matches:
            if (match.score_player1 + match.score_player2) <= 0:
                penalty_points = penalty_points + 1
                if penalty_points >= app.config['PENALTY_THRESHOLD']:
                    return penalty_points

        return penalty_points

    @staticmethod
    def get_player_by_id(player_id):
        return Player.query.filter_by(player_id=player_id).first()

    @staticmethod
    def get_player_by_email(player_email):
        return Player.query.filter_by(email=player_email).first()

    @staticmethod
    def get_player_by_name(player_name):
        return Player.query.filter_by(name=player_name).first()

    @staticmethod
    def key_fields():
        return ['email', 'name', 'net_wins', 'matches_won', 'matches_lost', 'net_sets', 'sets_won', 'sets_lost', 'penalty_points']

class Match_(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    round_count = db.Column(db.Integer, nullable=False, default=0)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    player1_name = db.Column(db.String(255), nullable=False)
    player2_name = db.Column(db.String(255), nullable=False)
    score_player1 = db.Column(db.Integer, default=0)
    score_player2 = db.Column(db.Integer, default=0)

    def __init__(self, league, player1_name, player2_name):
        self.league_id = league.league_id
        self.round_count = league.round_count
        self.player1_name = player1_name
        self.player2_name = player2_name       

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update_score(self, player1_name, player2_name, score_player1, score_player2):
        self.completed = True
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.score_player1 = score_player1
        self.score_player2 = score_player2
        self.commit()

    @staticmethod
    def get_match_by_id(match_id):
        return Match_.query.filter_by(match_id=match_id).first()


