import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class NPC(SqlAlchemyBase):
    __tablename__ = 'npcs'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    race = sa.Column(sa.String(30))
    char_class = sa.Column('class', sa.String(30))
    background = sa.Column(sa.Text)
    level = sa.Column(sa.Integer)

    strength = sa.Column(sa.Integer)
    dexterity = sa.Column(sa.Integer)
    constitution = sa.Column(sa.Integer)
    intelligence = sa.Column(sa.Integer)
    wisdom = sa.Column(sa.Integer)
    charisma = sa.Column(sa.Integer)
    image = sa.Column(sa.String(255))

    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))
    location_id = sa.Column(sa.Integer, sa.ForeignKey('locations.id'))

    campaign = relationship("Campaign", back_populates="npcs")
    location = relationship("Location", back_populates="npcs")