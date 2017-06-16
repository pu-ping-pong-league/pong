from sqlalchemy import and_, func, case, desc

HALL_OF_FAME_LIMIT = 10
FRAMES_PER_SECOND = 23

class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    video = db.relationship('Video', backref='user', lazy='dynamic')
    votes = db.relationship('Vote', backref='user', lazy='dynamic') 
    registered_on = db.Column(db.DateTime, nullable=False)
    last_active_on = db.Column(db.DateTime, nullable=False)
    stored_score = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = flask_bcrypt.generate_password_hash(password, app.config.get('BCRYPT_LOG_ROUNDS')).decode()
        now = datetime.datetime.now()
        self.registered_on = now
        self.last_active_on = now
        self.stored_score = 0