import uuid

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models import BaseModel


class ProductOrm(BaseModel):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    price: Mapped[int]
    amount: Mapped[int]
