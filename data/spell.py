import sqlalchemy as sa
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase

class Spell(SqlAlchemyBase):
    __tablename__ = 'spells'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(100), nullable=False)
    level = sa.Column(sa.Integer, nullable=False)
    components = sa.Column(sa.Text)
    school = sa.Column(sa.String(50))
    range = sa.Column(sa.String(100))
    duration = sa.Column(sa.String(100))
    casting_time = sa.Column(sa.String(50))
    description = sa.Column(sa.Text)
    campaign_id = sa.Column(sa.Integer, sa.ForeignKey('campaigns.id'))

    campaign = relationship("Campaign", back_populates="spells")