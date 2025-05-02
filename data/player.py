import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase


class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    race = sa.Column(sa.String(30))
    char_class = sa.Column('class', sa.String(30))
    level = sa.Column(sa.Integer)
    background = sa.Column(sa.Text)

    strength = sa.Column(sa.Integer)
    dexterity = sa.Column(sa.Integer)
    constitution = sa.Column(sa.Integer)
    intelligence = sa.Column(sa.Integer)
    wisdom = sa.Column(sa.Integer)
    charisma = sa.Column(sa.Integer)
    skills = sa.Column(sa.String(500))

    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="players")