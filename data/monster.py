import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Monster(SqlAlchemyBase):
    __tablename__ = 'monsters'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    cr = sa.Column(sa.String(20))
    monster_type = sa.Column(sa.String(50))
    description = sa.Column(sa.Text)
    image = sa.Column(sa.String(255))
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="monsters")