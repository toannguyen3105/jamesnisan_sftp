from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False, comment="Content")
    created_at = db.Column(db.Integer, nullable=True, comment="Item is created at")
    created_by = db.Column(db.String(30), nullable=True, comment="Item is created by")
    updated_at = db.Column(db.Integer, nullable=True, comment="Item is updated at")
    updated_by = db.Column(db.String(30), nullable=True, comment="Item is updated by")

    def __init__(self, content, created_at, created_by, updated_at, updated_by):
        self.content = content
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    def json(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'created_by': self.created_by,
            'updated_at': self.updated_at,
            'updated_by': self.updated_by
        }

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
