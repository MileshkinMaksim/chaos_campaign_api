import uuid
from typing import List, Optional
from sqlalchemy import Enum as SQLEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from app.schemas.force import Faction, UnitStatus, WeightClass


class ForceModel(Base):
    __tablename__ = "forces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sponsoring_faction: Mapped[Faction] = mapped_column(SQLEnum(Faction), default=Faction.MERCENARY)
    warchest_points: Mapped[int] = mapped_column(Integer, default=1000)
    support_points: Mapped[int] = mapped_column(Integer, default=500)
    reputation_score: Mapped[int] = mapped_column(Integer, default=10)

    # Двунаправленные связи
    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="forces")
    units: Mapped[List["MechUnitModel"]] = relationship(
        "MechUnitModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
    )
    pilots: Mapped[List["PilotModel"]] = relationship(
        "PilotModel", 
        back_populates="force", 
        cascade="all, delete-orphan"
    )


class MechUnitModel(Base):
    __tablename__ = "mech_units"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    force_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("forces.id", ondelete="CASCADE"), nullable=True)
    chassis: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    tonnage: Mapped[int] = mapped_column(Integer, nullable=False)
    weight_class: Mapped[WeightClass] = mapped_column(SQLEnum(WeightClass), nullable=False)
    bv2: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[UnitStatus] = mapped_column(SQLEnum(UnitStatus), default=UnitStatus.OPERATIONAL)
    assigned_pilot_id: Mapped[Optional[str]] = mapped_column(
        String(36), 
        ForeignKey("pilots.id", ondelete="SET NULL"), 
        nullable=True
    )

    force: Mapped[Optional["ForceModel"]] = relationship("ForceModel", back_populates="units")