import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Event(SqlAlchemyBase):
    __tablename__ = 'events'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    description = sa.Column(sa.Text)
    date = sa.Column(sa.String(50))
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="events")
    connections = relationship("GraphEdge",
                                  foreign_keys="[GraphEdge.from_event_id]",
                                  back_populates="from_event")