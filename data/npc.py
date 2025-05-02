import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class NPC(SqlAlchemyBase):
    __tablename__ = 'npcs'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    role = sa.Column(sa.String(50))
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    location = relationship("Location", back_populates="locations")
    campaign = relationship("Campaign", back_populates="npcs")