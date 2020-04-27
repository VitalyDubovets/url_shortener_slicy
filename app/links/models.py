from .. import db


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    public = db.Column(db.Boolean())
    privacy = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    long_url = db.Column(db.String(120), index=True)
    short_url = db.Column(db.String(120), index=True)
