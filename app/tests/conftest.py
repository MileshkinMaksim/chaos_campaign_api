import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.main import app
from app.config import settings
from app.db.database import Base, get_db
from app.db.models.user import UserModel
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import Faction, UnitStatus, WeightClass
from app.core.security import create_access_token, get_password_hash

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = async_sessionmaker(
        bind=engine, 
        class_=AsyncSession, 
        expire_on_commit=False,
        autoflush=False
    )
    
    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_db] = lambda: test_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac
        
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_user(test_db: AsyncSession) -> UserModel:
    user = UserModel(
        username="test_commander",
        hashed_password=get_password_hash("password123")
    )
    test_db.add(user)
    await test_db.flush()
    return user


@pytest_asyncio.fixture(scope="function")
async def auth_headers(test_user: UserModel) -> dict:
    token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture(scope="function")
async def test_force(test_db: AsyncSession, test_user: UserModel) -> ForceModel:
    force = ForceModel(
        owner_id=test_user.id,
        name="Iron Hand Mercenaries",
        sponsoring_faction=Faction.MERCENARY,
        warchest_points=1000,
        support_points=500,
        reputation_score=10
    )
    test_db.add(force)
    await test_db.flush()

    pilot = PilotModel(
        force_id=force.id,
        name="Buster McCall",
        gunnery=4,
        piloting=5,
        experience_points=1000,
        edge_points=1
    )
    test_db.add(pilot)

    unit = MechUnitModel(
        force_id=force.id,
        chassis="Starslayer",
        model="STAGE-3C",
        tonnage=50,
        weight_class=WeightClass.MEDIUM,
        bv2=1340,
        status=UnitStatus.OPERATIONAL
    )
    test_db.add(unit)
    await test_db.flush()

    # Явная подгрузка связей через selectinload во избежание MissingGreenlet
    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force.id)
        .options(
            selectinload(ForceModel.pilots),
            selectinload(ForceModel.units)
        )
    )
    result = await test_db.execute(stmt)
    return result.scalar_one()