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


def load_menu_hours(filename):
    with open(f"{FILEPATH}/{filename}", "r") as csv_file:
        # Read file line by line
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

            with Session(engine) as session:
                session.add(db_menu_hours)

                session.commit()


def load_store_status():
    pass


def load_store_timezones():
    pass


if __name__ == "__main__":
    load_menu_hours("menu_hours.csv")
