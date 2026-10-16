from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.database import get_db
from app.db.models.user import UserModel
from app.schemas.auth import Token, UserRegister, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Регистрация командира")
async def register_user(
    user_in: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрирует нового командира отряда в базе данных.
    
    * **201 Created**: Пользователь успешно создан.
    * **400 Bad Request**: Имя пользователя уже занято.
    """
    stmt = select(UserModel).where(UserModel.username == user_in.username)
    result = await db.execute(stmt)
    if result.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )

    new_user = UserModel(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password)
    )
    db.add(new_user)
    await db.flush()
    return new_user


@router.post("/token", response_model=Token, summary="Получение JWT токена")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентифицирует пользователя по логину/паролю и выдает JWT токен формата Bearer.
    """
    stmt = select(UserModel).where(UserModel.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")