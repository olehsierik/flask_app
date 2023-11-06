from sqlalchemy import UniqueConstraint, Integer, String, VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref
from app.database import db
from typing import List


class User(db.Model):
    __table_args__ = (
        UniqueConstraint('username', name='unique_constraint_username'),
    )

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name = mapped_column(VARCHAR(100), nullable=False)
    last_name = mapped_column(VARCHAR(100), nullable=False)
    username = mapped_column(VARCHAR(50), unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    events: Mapped[List['Event']] = relationship('Event', backref=backref('creator'))
    events_users: Mapped[List['EventUser']] = relationship('EventUser', backref=backref('user'))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if hasattr(self, c.name)}
