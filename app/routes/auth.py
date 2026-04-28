from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserResponse
from app.models.auth import Token, UserToken
from app.services.user_service import UserService
from app.database import get_database
from app.utils.security import create_access_token, create_refresh_token, verify_password, verify_token, settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

async def get_user_service():
    db = get_database()
    return UserService(db)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    if await service.get_user_by_email(user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return await service.create_user(user_in)

@router.post("/login", response_model=UserToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
):
    user = await service.get_user_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    refresh_token = create_refresh_token(data={"sub": user["email"]})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "name": user["name"],
        "email": user["email"],
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    service: UserService = Depends(get_user_service)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(refresh_token, expected_type="refresh")
    if not payload:
        raise credentials_exception
    
    email = payload.get("sub")
    user = await service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
        
    new_access_token = create_access_token(data={"sub": email})
    new_refresh_token = create_refresh_token(data={"sub": email}) # Rotate refresh token
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
