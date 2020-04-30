from .models import User
from app import mr_mallow


class UserSerializer(mr_mallow.SQLAlchemySchema):
    class Meta:
        model = User

    email = mr_mallow.auto_field()
    username = mr_mallow.auto_field()
    id = mr_mallow.auto_field()
