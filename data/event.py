import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), nullable=False)
    is_quest = sa.Column(sa.Boolean, default=False)
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="events")