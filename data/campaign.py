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
    players = relationship("Player", back_populates="campaign", cascade="all, delete")
    items = relationship("Item", back_populates="campaign", cascade="all, delete")
    npcs = relationship("NPC", back_populates="campaign", cascade="all, delete")
    spells = relationship("Spell", back_populates="campaign", cascade="all, delete")
    monsters = relationship("Monster", back_populates="campaign", cascade="all, delete")
    locations = relationship("Location", back_populates="campaign", cascade="all, delete")
    events = relationship("Event", back_populates="campaign", cascade="all, delete")
    graph_edges = relationship("GraphEdge", back_populates="campaign", cascade="all, delete")

    @property
    def created_date_formatted(self):
        return self.created_date.strftime("%Y-%m-%d %H:%M")

    @property
    def updated_date_formatted(self):
        return self.updated_date.strftime("%Y-%m-%d %H:%M")
