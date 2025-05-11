import sqlalchemy as sa
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class GraphEdge(SqlAlchemyBase):
    __tablename__ = 'graph_edges'

    id = sa.Column(sa.Integer, primary_key=True)
    from_id = sa.Column(sa.Integer, nullable=False)
    to_id = sa.Column(sa.Integer, nullable=False)
    label = sa.Column(sa.String(100), default="Связано")
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="graph_edges")