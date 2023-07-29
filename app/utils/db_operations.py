from sqlmodel import Session, and_, select

from app.models.report import Menu_Hours, Store_Status, Store_Timezone


def get_all_store_timezones(session: Session):

    query = select(Store_Timezone)
    store_ids = session.exec(query).all()
    return store_ids


def get_store_timings(store_id: str, session: Session):

    query = select(Store_Timezone, Menu_Hours).where(
        and_(
            Store_Timezone.store_id == store_id,
            Store_Timezone.store_id == Menu_Hours.store_id,
        )
    )
    store_timings = session.exec(query).all()
    return store_timings


def get_store_status(store_id, session: Session):

    query = (
        select(Store_Timezone, Store_Status)
        .where(
            and_(
                Store_Timezone.store_id == store_id,
                Store_Timezone.store_id == Store_Status.store_id,
            )
        )
        .order_by(Store_Status.timestamp_utc.asc())
    )
    store_status = session.exec(query).all()
    return store_status
