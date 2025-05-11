import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    item_type = sa.Column(sa.String(50))
    rarity = sa.Column(sa.String(30))
    description = sa.Column(sa.Text)
    weight = sa.Column(sa.Float)
    value = sa.Column(sa.String(50))
    image = sa.Column(sa.String(255))
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="items")