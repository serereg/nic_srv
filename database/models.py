from gino import Gino


db = Gino()


class Cooler(db.Model):
    __tablename__ = "coolers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False, default=lambda: "")
