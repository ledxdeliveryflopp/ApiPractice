from sqlalchemy import Column, UUID, String
from src.settings.models import DefaultModel


class EmailCode(DefaultModel):
    __tablename__ = "code"

    title = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_email = Column(String, nullable=False)
