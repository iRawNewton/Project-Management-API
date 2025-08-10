""" from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.models.user import SignupRequest, LoginRequest, UserInDB, UserPublic
from app.db.database import db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Signup route
@router.post("/signup")
async def signup(payload: SignupRequest):
    if await db["users"].find_one({"email": payload.email}):
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_pw = hash_password(payload.password)
    user = UserInDB(email=payload.email, hashed_password=hashed_pw)

    result = await db["users"].insert_one(user.dict())
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}

# Login route
@router.post("/login")
async def login(payload: LoginRequest):
    user = await db["users"].find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=timedelta(minutes=60))
    return {"access_token": token, "token_type": "bearer"}

# Protected route example
@router.get("/me", response_model=UserPublic)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await db["users"].find_one({"_id": payload.get("sub")})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserPublic(**user)
 """


from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta
from app.models.user import SignupRequest, LoginRequest, UserInDB, UserPublic
from app.db.database import db
from app.core.security import hash_password, verify_password, create_access_token, decode_access_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Helper response format
def api_response(success: bool, message: str, data: dict = None):
    return {
        "success": success,
        "message": message,
        "data": data or {}
    }

# Signup route
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(payload: SignupRequest):
    if await db["users"].find_one({"email": payload.email}):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered."
        )

    hashed_pw = hash_password(payload.password)
    user = UserInDB(email=payload.email, hashed_password=hashed_pw)
    result = await db["users"].insert_one(user.dict())

    return api_response(
        success=True,
        message="User created successfully.",
        data={"user_id": str(result.inserted_id)}
    )

# Login route
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest):
    user = await db["users"].find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials."
        )

    token = create_access_token(data={"sub": str(user["_id"])}, expires_delta=timedelta(minutes=60))

    return api_response(
        success=True,
        message="Login successful.",
        data={"access_token": token, "token_type": "bearer"}
    )

# Protected route
@router.get("/me", response_model=UserPublic, status_code=status.HTTP_200_OK)
async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

    user = await db["users"].find_one({"_id": payload.get("sub")})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    return user  # FastAPI automatically validates and returns UserPublic
