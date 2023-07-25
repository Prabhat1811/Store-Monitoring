"""
Python script for fetching data from csv and putting it in our database
"""

from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from app.models.report import Menu_Hours

engine = create_engine(
    settings.db_uri,
    echo=settings.db_echo,
    connect_args=settings.db_connect_args,
)


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


FILEPATH = "./app/data_csv"


create_db_and_tables(engine)


def load_menu_hours(filename, batch_size=1000):
    """
    Used batch inserts because of speed

    Here is the data I observed when inserting around 80000 records,
    1. Insert one by one:
        a. Status - Incomplete
        b. Time taken - 30 seconds
        c. Records inserted - 3004
    2. Insert in batch, size = 1000:
        a. Status - Complete
        b. Time taken - 11 seconds
        c. Records inserted - 86198
    3. Insert in batch, size = 5000:
        a. Status - Complete
        b. Time taken - 8.5 seconds
        c. Records inserted - 86198
    4. Insert in batch, size = 10000:
        a. Status - Complete
        b. Time taken - 7.5 seconds
        c. Records inserted - 86198

    I decided to go with batch size of 5000
    """

    with open(f"{FILEPATH}/{filename}", "r") as csv_file:
        batch = []
        for i, data in enumerate(csv_file):
            if not i:
                continue

            store_id, day, start_time_local, end_time_local = data.strip().split(",")
            db_menu_hours = Menu_Hours(
                store_id=store_id,
                day=day,
                start_time_local=start_time_local,
                end_time_local=end_time_local,
            )
            batch.append(db_menu_hours)

            if len(batch) >= batch_size:
                with Session(engine) as session:
                    session.bulk_save_objects(batch)
                    session.commit()
                    batch = []

        # Insert any remaining records
        if batch:
            with Session(engine) as session:
                session.bulk_save_objects(batch)
                session.commit()


def load_store_status(filename, batch_size=1000):
    pass


def load_store_timezones(filename, batch_size=1000):
    pass


if __name__ == "__main__":
    load_menu_hours("menu_hours.csv", batch_size=5000)
