import uuid
from typing import Optional
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class PilotModel(Base):
    __tablename__ = "pilots"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gunnery: Mapped[int] = mapped_column(Integer, default=4)
    piloting: Mapped[int] = mapped_column(Integer, default=5)
    experience_points: Mapped[int] = mapped_column(Integer, default=0)
    total_xp_earned: Mapped[int] = mapped_column(Integer, default=0)
    edge_points: Mapped[int] = mapped_column(Integer, default=1)
    is_temporary_hire: Mapped[bool] = mapped_column(Boolean, default=False)

    force: Mapped[Optional["ForceModel"]] = relationship("ForceModel", back_populates="pilots")