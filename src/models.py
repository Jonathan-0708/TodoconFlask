from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    done = db.Column(db.Boolean, unique=False, nullable=False)

    def __repr__(self): #método que devuelve información de la clase en forma de string %r valor variable
        return 'La tarea es %r' % self.name

    def serialize(self): #retorna un Json
        return {
            "id": self.id,
            "name": self.name,
            "done": self.done,
        }