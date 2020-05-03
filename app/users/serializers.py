from .models import User
from app import mr_mallow


class UserSerializer(mr_mallow.SQLAlchemySchema):
    class Meta:
        model = User
        include_fk = True
        ordered = True

    id = mr_mallow.auto_field()
    username = mr_mallow.auto_field()
    email = mr_mallow.auto_field()
    links = mr_mallow.auto_field()
