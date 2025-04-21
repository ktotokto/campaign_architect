import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Campaign(SqlAlchemyBase):
    __tablename__ = 'campaigns'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))

    user = relationship("User", back_populates="campaigns")
    players = relationship("Player", back_populates="campaign")
    items = relationship("Item", back_populates="campaign")
    npcs = relationship("NPC", back_populates="campaign")
    spells = relationship("Spell", back_populates="campaign")
    monsters = relationship("Monster", back_populates="campaign")
    locations = relationship("Location", back_populates="campaign")
    events = relationship("Event", back_populates="campaign")