from .models import Link
from app import mr_mallow


class LinkSerializer(mr_mallow.SQLAlchemyAutoSchema):
    class Meta:
        model = Link
        include_fk = True
        ordered = True
