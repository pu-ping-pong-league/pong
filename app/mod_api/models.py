from sqlalchemy import and_, func, case, desc
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

from app import db

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

    def get_all_players_sorted_by_net_wins(self):
        order = Player.net_wins.desc()
        return Player.query.filter_by(league_id=self.league_id).order_by(order).all() 

    def get_all_players_sorted_by_net_sets(self, net_wins):
        order = Player.net_sets.desc()
        return Player.query.filter_by(league_id=self.league_id, net_wins=net_wins).order_by(order).all()

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
    games_won = db.Column(db.Integer, nullable=False, default=0)
    games_lost = db.Column(db.Integer, nullable=False, default=0)
    sets_won = db.Column(db.Integer, nullable=False, default=0)
    sets_lost = db.Column(db.Integer, nullable=False, default=0)
    penalty_points = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, nullable=False, default=1000)

    @hybrid_property
    def net_wins(self):
        return self.games_won - self.games_lost

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

    def update_stats(self, score):
        if score == WIN:
            self.games_won = self.games_won + 1
            self.sets_won = self.sets_won + WIN
        elif score < WIN:
            self.sets_won = self.sets_won + WIN
        else:
            self.penalty_points = self.penalty_points + 1
        self.commit()

    @staticmethod
    def get_player_by_id(player_id):
        return Player.query.filter_by(player_id=player_id).first()

    @staticmethod
    def get_player_by_email(player_email):
        return Player.query.filter_by(email=player_email).first()

    @staticmethod
    def key_fields():
        return ['email', 'name', 'games_won', 'games_lost', 'net_wins', 'sets_won', 'sets_lost', 'net_sets', 'penalty_points']

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

    def update_score(self, score_player1, score_player2):
        self.completed = True
        self.score_player1 = score_player1
        self.score_player2 = score_player2        
        self.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_match_by_id(match_id):
        return Match_.query.filter_by(match_id=match_id).first()


