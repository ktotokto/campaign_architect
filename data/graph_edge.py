import sqlalchemy as sa
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class GraphEdge(SqlAlchemyBase):
    __tablename__ = 'graph_edges'

    id = sa.Column(sa.Integer, primary_key=True)
    label = sa.Column(sa.String(100), default="Связано")
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))
    from_event_id = sa.Column(sa.Integer, sa.ForeignKey('events.id'), nullable=False)
    to_event_id = sa.Column(sa.Integer, sa.ForeignKey('events.id'), nullable=False)

    campaign = relationship("Campaign", back_populates="graph_edges")
    from_event = relationship("Event", foreign_keys=[from_event_id])
    to_event = relationship("Event", foreign_keys=[to_event_id])