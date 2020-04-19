from app import db

class User(db.Model):
    # 表的名字:,或者derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case
    __tablename__ = 'sys_user'
    #colums
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    real_name = db.Column(db.String(80), unique=True, nullable=False)
    isactive = db.Column(db.String(20), unique=True, nullable=False)
    theme = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


