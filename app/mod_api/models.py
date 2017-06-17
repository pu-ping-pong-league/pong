from sqlalchemy import and_, func, case, desc

WIN = 2

class League(db.Model):
    league_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league_name = db.Column(db.String(255), unique=True, nullable=False)
    round_count = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, name):
        self.league_name = name

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_league_by_id(league_id):
        return League.query.filter_by(league_id=league_id).first()

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league = db.relationship('League', backref='player', lazy='dynamic')
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    games_won = db.Column(db.Integer, nullable=False, default=0)
    games_lost = db.Column(db.Integer, nullable=False, default=0)
    sets_won = db.Column(db.Integer, nullable=False, default=0)
    sets_lost = db.Column(db.Integer, nullable=False, default=0)
    penalty_points = db.Column(db.Integer, nullable=False, default=0)

    @hybrid_property
    def net_wins(self):
        return self.games_won - self.games_lost

    @hybrid_property
    def net_sets(self):
        return self.sets_won - self.sets_lost

    def __init__(self, email, name, league_id):
        self.email = email
        self.name = name
        self.league = league_id

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    # ensure it does not delete matches
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
    def key_fields():
        return ['email', 'name', 'games_won', 'games_lost', 'net_wins', 'sets_won', 'sets_lost', 'net_sets', 'penalty_points']

class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    league = db.relationship('League', backref='match', lazy='dynamic')
    round_count = db.Column(db.Integer, nullable=False, default=0)
    player1 = db.relationship('Player', backref='match', lazy='dynamic')
    player2 = db.relationship('Player', backref='match', lazy='dynamic')
    completed = db.Column(db.Boolean, nullable=False, default=False)
    score_player1 = games_won = db.Column(db.Integer, default=None)
    score_player2 = games_won = db.Column(db.Integer, default=None)

    def __init__(self, league_id, round_count, p1_id, p2_id):
        self.league = league_id
        self.round_count = round_count
        self.player1 = p1_id
        self.player2 = p2_id
        if not p2_id:
            score_player1 = WIN        

    def commit(self, insert=False):
        if insert:
            db.session.add(self)
        db.session.commit()

    def update_score(self, score_player1, score_player2):
        if score_player1 and score_player2:
            self.completed = True
        self.score_player1 = score_player1
        self.score_player2 = score_player2        
        self.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_match_by_id(match_id):
        return Match.query.filter_by(match_id=match_id).first()


