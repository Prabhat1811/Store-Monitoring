from sqlmodel import Session, select

from app.models.report import Store_Timezone


def get_store_ids(session: Session):

    query = select(Store_Timezone)
    store_ids = session.exec(query).all()
    print(type(store_ids))
    return store_ids
