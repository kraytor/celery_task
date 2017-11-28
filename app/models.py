from app import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime, default=db.func.now())
    ip = db.Column(db.String(120), nullable=False)
    function = db.Column(db.String(120), nullable=False)
    in_data = db.Column(db.String(255), nullable=False)
    result = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "{} {} {} {}".format(
                self.date,
                self.ip,
                self.in_data,
                self.result)


db.create_all()
