from libgravatar import Gravatar
from sqlalchemy.orm import Session

from m12.database.models import User
from m12.schemas import UserIn, UserOut


async def get_user_by_email(email: str, db: Session) -> UserOut:
    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserIn, db: Session) -> UserOut:
    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
