from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    loaned_to = db.Column(db.String(120), index=True)
    rfid = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<Book {}>'.format(self.title)