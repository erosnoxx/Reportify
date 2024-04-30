from sqlalchemy.dialects.postgresql import UUID
from app.settings import db
from app.services import get_now, generate_uuid
from flask_login import UserMixin
from app.services import check_hashed_pwd


class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=generate_uuid, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=get_now, nullable=False)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    def check_password(self, password):
        return check_hashed_pwd(self.password, password)

    def to_dict(self):
        return {
            'id': str(self.id),
            'fisrt_name': self.full_name,
            'last_name': self.last_name,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'created_at': self.created_at,
        }