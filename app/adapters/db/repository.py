from typing import Iterable, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import WishModel


class WishRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> WishModel:
        m = WishModel(**data)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return m

    def get(self, wish_id: int) -> Optional[WishModel]:
        return self.db.get(WishModel, wish_id)

    def list(
        self, *, q: Optional[str], purchased: Optional[bool], price_lte: Optional[int]
    ) -> Iterable[WishModel]:
        stmt = select(WishModel)
        if purchased is not None:
            stmt = stmt.where(WishModel.is_purchased == purchased)
        if q:
            like = f"%{q}%"
            stmt = stmt.where(
                (WishModel.title.ilike(like)) | (WishModel.notes.ilike(like))
            )
        if price_lte is not None:
            stmt = stmt.where(
                (WishModel.price_estimate <= price_lte)
                | (WishModel.price_estimate.is_(None))
            )
        return self.db.execute(stmt.order_by(WishModel.id.desc())).scalars().all()

    def update(self, wish_id: int, patch: dict) -> Optional[WishModel]:
        m = self.get(wish_id)
        if not m:
            return None
        for k, v in patch.items():
            setattr(m, k, v)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return m

    def delete(self, wish_id: int) -> bool:
        m = self.get(wish_id)
        if not m:
            return False
        self.db.delete(m)
        self.db.commit()
        return True

    def mark_purchased(self, wish_id: int) -> Optional[WishModel]:
        m = self.get(wish_id)
        if not m:
            return None
        m.is_purchased = True
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return m
