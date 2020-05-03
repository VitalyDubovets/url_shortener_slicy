import re

from .. import db


class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    public = db.Column(db.Boolean())
    privacy = db.Column(db.Boolean())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    long_url = db.Column(db.String(120), index=True)
    short_url = db.Column(db.String(120), index=True)
    count_of_visits = db.Column(db.Integer)

    def __str__(self):
        return self.long_url

    def check_and_save_link(self):
        if not re.match('^http[s]?://', self.long_url):
            self.long_url = 'https://' + self.long_url
        db.session.add(self)
        db.session.commit()
