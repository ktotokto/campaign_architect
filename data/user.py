import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(50), unique=True, nullable=False)
    email = sa.Column(sa.String(100), unique=True)
    hashed_password = sa.Column(sa.String(200))
    is_active = sa.Column(sa.Boolean, default=True)

    campaigns = relationship("Campaign", back_populates="user")

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
