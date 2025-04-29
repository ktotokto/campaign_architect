import sqlalchemy as sa
from datetime import datetime
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase


class Campaign(SqlAlchemyBase):
    __tablename__ = 'campaigns'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    system = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text)
    created_date = sa.Column(sa.DateTime, default=datetime.now)
    updated_date = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    user = relationship("User", back_populates="campaigns")
    players = relationship("Player", back_populates="campaign")
    items = relationship("Item", back_populates="campaign")
    npcs = relationship("NPC", back_populates="campaign")
    spells = relationship("Spell", back_populates="campaign")
    monsters = relationship("Monster", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    events = relationship("Event", back_populates="campaign")

    @property
    def created_date_formatted(self):
        return self.created_date.strftime("%Y-%m-%d %H:%M")

    @property
    def updated_date_formatted(self):
        return self.updated_date.strftime("%Y-%m-%d %H:%M")
