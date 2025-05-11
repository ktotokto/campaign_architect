import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Location(SqlAlchemyBase):
    __tablename__ = 'locations'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text)
    type = sa.Column(sa.String(50))
    image = sa.Column(sa.String(255))
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="locations")
    npcs = relationship("NPC", back_populates="location")