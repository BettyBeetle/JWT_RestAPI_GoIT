from fastapi import APIRouter, HTTPException, Depends, status, Query
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html

from typing import List
from sqlalchemy.orm import Session

from m12.database.db import get_db
from m12.schemas import ContactsIn, ContactsOut
from m12.repository import contacts as repository_contacts
from m12.repository.contacts import upcoming_birthdays
from m12.database.models import User, Contacts
from m12.services.auth import auth_service


router = APIRouter(prefix='/contacts')

@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="RestApi Docs"
    )

@router.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint():
    return JSONResponse(get_openapi(title="RestApi", version="1.0.0", routes=router.routes))



@router.get("/", response_model=List[ContactsOut])
# async def read_contacts(
#         search: str = Query(None, description="Search contacts by first name, last name, or email"),
#         skip: int = Query(0, ge=0),
#         limit: int = Query(100, ge=1),
#         current_user: User= Depends(auth_service.get_current_user),
#         db: Session = Depends(get_db)
# ):
#     # async def read_contacts(skip: int = 0, limit: int = 100,
#     #                         current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
#     #     contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
#     #     return contacts
#
#     if search:
#         contacts = await repository_contacts.search_contacts(search, skip, limit, current_user, db)
#     else:
#         contacts = await repository_contacts.get_contacts(skip, limit, current_user, db)
#     if not contacts:
#         raise HTTPException(status_code=404, detail="No contacts found")
#     return contacts

async def search_contacts(search: str, skip: int, limit: int, current_user: User, db: Session):
    query = db.query(Contacts).filter(Contacts.user_id == current_user.id)

    if search:
        query = query.filter(
            or_(
                Contacts.first_name.ilike(f"%{search}%"),
                Contacts.last_name.ilike(f"%{search}%"),
                Contacts.email.ilike(f"%{search}%")
            )
        )

    contacts = query.offset(skip).limit(limit).all()
    return contacts


@router.get("/{contact_id}", response_model=ContactsOut)
async def read_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactsOut)
async def create_contact(body: ContactsIn, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.put("/{contact_id}", response_model=ContactsOut)
async def update_contact(body: ContactsIn, contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body,  current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact



@router.delete("/{contact_id}", response_model=ContactsOut)
async def remove_contact(contact_id: int, current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.get("/upcoming_birthdays/", response_model=List[ContactsOut])
async def get_upcoming_birthdays(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    upcoming_birthdays_list = await upcoming_birthdays(db)
    upcoming_birthdays_out_list = [ContactsOut(
                                        id=contact.id,
                                        first_name = contact.first_name,
                                        last_name = contact.last_name,
                                        email = contact.email,
                                        phone_number = contact.phone_number,
                                        date_of_birth = contact.date_of_birth,
                                        nick = contact.nick,
                                    ) for contact in upcoming_birthdays_list]
    # result = await upcoming_birthdays(current_user, db)
    # return result
    return upcoming_birthdays_out_list