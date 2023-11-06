from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship, backref
from app.database import db
from datetime import datetime
from typing import List


class Event(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    created_by = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    begin_at = mapped_column(String, nullable=False)
    end_at = mapped_column(String, nullable=False)
    max_users = mapped_column(Integer, nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=False)
    event_users: Mapped[List['EventUser']] = relationship('EventUser', backref=backref('event'))

    def available_for_registration(self, user_id: int):
        return (
                self.max_users - len(self.event_users) > 0 and
                any(event_user.user_id == user_id for event_user in self.event_users) == False and
                datetime.strptime(self.end_at, "%Y-%m-%d").date() >= datetime.now().date() and self.is_active == True
        )

    def available_slots(self):
        return self.max_users - len(self.event_users)

    def is_user_registered(self, user_id):
        return any(event_user.user_id == user_id for event_user in self.event_users)

    def set_date(self):
        self.begin_at = datetime.strptime(self.begin_at, "%Y-%m-%d")
        self.end_at = datetime.strptime(self.end_at, "%Y-%m-%d")

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if hasattr(self, c.name)}


class EventUser(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_id = mapped_column(Integer, ForeignKey('event.id'), nullable=False)
    user_id = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = mapped_column(String, nullable=False)
    score = mapped_column(Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns if hasattr(self, c.name)}
