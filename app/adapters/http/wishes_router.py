from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.adapters.db.repository import WishRepository
from app.adapters.http.schemas import WishCreate, WishOut, WishUpdate
from app.security import require_jwt
from app.shared.db import get_db

router = APIRouter(prefix="/wishes", tags=["wishes"])


@router.post(
    "",
    response_model=WishOut,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_jwt)],
)
def create_wish(body: WishCreate, db: Session = Depends(get_db)):
    repo = WishRepository(db)
    return repo.create(body.model_dump())


@router.get("", response_model=List[WishOut])
def list_wishes(
    q: Optional[str] = Query(
        None,
        description="search in title/notes",
        max_length=100,
    ),
    purchased: Optional[bool] = Query(None, description="filter by purchase status"),
    price_lte: Optional[int] = Query(None, ge=0, description="price <= value"),
    db: Session = Depends(get_db),
):
    repo = WishRepository(db)
    return list(repo.list(q=q, purchased=purchased, price_lte=price_lte))


@router.get("/{wish_id}", response_model=WishOut)
def get_wish(wish_id: int, db: Session = Depends(get_db)):
    repo = WishRepository(db)
    m = repo.get(wish_id)
    if not m:
        raise HTTPException(status_code=404, detail="wish not found")
    return m


@router.patch("/{wish_id}", response_model=WishOut, dependencies=[Depends(require_jwt)])
def update_wish(wish_id: int, body: WishUpdate, db: Session = Depends(get_db)):
    repo = WishRepository(db)
    m = repo.update(wish_id, body.model_dump(exclude_unset=True))
    if not m:
        raise HTTPException(status_code=404, detail="wish not found")
    return m


@router.delete(
    "/{wish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_jwt)],
)
def delete_wish(wish_id: int, db: Session = Depends(get_db)):
    repo = WishRepository(db)
    ok = repo.delete(wish_id)
    if not ok:
        raise HTTPException(status_code=404, detail="wish not found")
    return


@router.post(
    "/{wish_id}/purchase", response_model=WishOut, dependencies=[Depends(require_jwt)]
)
def mark_purchased(wish_id: int, db: Session = Depends(get_db)):
    repo = WishRepository(db)
    m = repo.mark_purchased(wish_id)
    if not m:
        raise HTTPException(status_code=404, detail="wish not found")
    return m
