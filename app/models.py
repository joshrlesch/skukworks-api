from app import db

class Events(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	eventId = db.Column(db.Integer, index=True, unique=True)
	riderId = db.Column(db.String(64), index=True, unique=True)
	speed = db.Column(db.Float, index=True)
	eventName = db.Column(db.String(120), index=True)
	createTime = db.Column(db.DateTime)
	updateTime = db.Column(db.DateTime)

	def __repr__(self):
		return '<Events %r' % (self.eventId)