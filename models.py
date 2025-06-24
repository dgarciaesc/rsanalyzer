from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SearchResult(db.Model):
    __tablename__ = 'search_results'

    id = db.Column(db.Integer, primary_key=True)
    listing_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    currency = db.Column(db.String(3))
    location = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    search_date = db.Column(db.DateTime, default=datetime.utcnow)
    raw_data = db.Column(db.JSON)

    def __repr__(self):
        return f'<SearchResult {self.listing_id}>' 