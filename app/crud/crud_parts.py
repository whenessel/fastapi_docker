
from sqlalchemy.orm import Session

from app.models.models import Tag


# def get_parts(db: Session, sort_column: str, sort_order: str, is_hidden: bool | None = None) -> Tag:
#     query = select(Tag).where(Tag.deleted_at.is_(None))

#     if is_hidden is True:
#         query = query.where(not_(Tag.is_hidden.is_(True)))

#     query = query.order_by(text(f"{sort_column} {sort_order}"))

#     result = db.execute(query)

#     return result.scalars().all()


# def get_part_by_uuid(db: Session, uuid: UUID) -> Tag:
#     query = select(Tag).where(Tag.uuid == uuid)

#     result = db.execute(query)

#     return result.scalar_one_or_none()


# def get_part_by_name(db: Session, name: str) -> Tag:
#     query = select(Tag).where(Tag.name == name).where(Tag.deleted_at.is_(None))

#     result = db.execute(query)

#     return result.scalar_one_or_none()


# def get_parts_id_by_uuid(db: Session, uuid: list[UUID]) -> Tag:
#     query = select(Tag.id).filter(Tag.uuid.in_(uuid))

#     result = db.execute(query)

#     return result.scalars().all()


def create_part(db: Session, data: dict) -> Tag:
    new_part = Tag(**data)
    db.add(new_part)
    db.commit()
    db.refresh(new_part)

    return new_part


def update_part(db: Session, db_part: Tag, update_data: dict) -> Tag:
    for key, value in update_data.items():
        setattr(db_part, key, value)

    db.add(db_part)
    db.commit()
    db.refresh(db_part)

    return db_part
