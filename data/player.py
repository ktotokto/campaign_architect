import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Player(SqlAlchemyBase):
    __tablename__ = 'players'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    race = sa.Column(sa.String(30))
    class_ = sa.Column('class', sa.String(30))
    level = sa.Column(sa.Integer)
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="players")