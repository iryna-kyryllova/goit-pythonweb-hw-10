from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.database.models import User
from src.schemas.contacts import ContactBase, ContactResponse, ContactBirthdayRequest
from src.services.contacts import ContactService
from src.services.auth import get_current_user
from src.conf import messages

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse], status_code=status.HTTP_200_OK)
async def read_contacts(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip, limit, user)
    return contacts


@router.get(
    "/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_200_OK
)
async def read_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactBase, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body, user)


@router.put(
    "/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_201_CREATED
)
async def update_contact(
    body: ContactBase, contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    contact_service = ContactService(db)
    contact = await contact_service.remove_contact(contact_id, user)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=messages.CONTACT_NOT_FOUND
        )
    return


@router.get(
    "/search", response_model=List[ContactResponse], status_code=status.HTTP_200_OK
)
async def search_contacts(
    text: str, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)
):
    contact_service = ContactService(db)
    contacts = await contact_service.search_contacts(text, skip, limit, user)
    return contacts


@router.post(
    "/week-birthdays",
    response_model=List[ContactResponse],
    status_code=status.HTTP_200_OK,
)
async def get_week_birthdays(
    body: ContactBirthdayRequest, db: AsyncSession = Depends(get_db)
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_week_birthdays(body.days)
    return contacts
