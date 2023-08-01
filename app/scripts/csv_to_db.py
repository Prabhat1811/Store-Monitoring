"""
Python script for fetching data from csv and putting it in our database.

Right now, It fetches the files locally.
For real-world scenario we can create a separate space where new files are uploaded regularly.
We can then automate this script to run on a daily basis to check if any new files are uploaded.
If yes, Then download, process and put them in the db.
"""

from datetime import datetime
from time import time

from pydantic import BaseModel, Field
from sqlmodel import Session, SQLModel, create_engine
from tqdm import tqdm

from app.config import settings
from app.models.report import Menu_Hours, Store_Status, Store_Timezone

FILEPATH = "./app/data_csv"
BATCH_SIZE = 10000

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


create_db_and_tables(engine)


def load_to_db(filename, schema, fields, batch_size=BATCH_SIZE):
    """
    Used batch inserts because of speed

    Here is the data I observed when inserting around 80000 records,
    1. Insert one by one,
        a. Status - Incomplete
        b. Time taken - 30 seconds
        c. Records inserted - 3004
    2. Insert in batch, size = 1000,
        a. Status - Complete
        b. Time taken - 11 seconds
        c. Records inserted - 86198
    3. Insert in batch, size = 5000,
        a. Status - Complete
        b. Time taken - 8.5 seconds
        c. Records inserted - 86198
    4. Insert in batch, size = 10000,
        a. Status - Complete
        b. Time taken - 7.5 seconds
        c. Records inserted - 86198

    I decided to go with batches size of 5000 and 10000

    It is taking close to 5 minutes to upload around 2 million records from csv to SQLite database.
    I don't think this is optimal and can be brought down to less than half.
    """
    print(f"Started with: {filename}")

    fields_dict = {}

    with open(f"{FILEPATH}/{filename}", "r") as csv_file:
        batch = []
        for i, data in enumerate(tqdm(csv_file)):
            if not i:
                if len(fields) != len(data.strip().split(",")):
                    print("Fields do not match, aborting...")
                    return
                continue

            processed_data = data.strip().split(",")

            for field, value in zip(fields, processed_data):
                # Check for timestampm_utc field and strip ` UTC` from it
                if field == "timestamp_utc":
                    fields_dict[field] = value.rstrip(" UTC")
                else:
                    fields_dict[field] = value

            db_data = schema(**fields_dict)
            db_data.process_for_insert()
            batch.append(db_data)

            if len(batch) >= batch_size:
                try:
                    with Session(engine) as session:
                        session.bulk_save_objects(batch)
                        session.commit()
                        batch = []
                except:
                    print("Error inserting. Check fields")
                    return

        # Insert any remaining records
        if batch:
            try:
                with Session(engine) as session:
                    session.bulk_save_objects(batch)
                    session.commit()
            except:
                print("Error inserting. Check fields")
                return

    print("Finished")


def main():
    menu_hours_fields = ["store_id", "day", "start_time_local", "end_time_local"]
    store_status_fields = ["store_id", "status", "timestamp_utc"]
    store_timezones = ["store_id", "timezone"]

    load_to_db("menu_hours.csv", Menu_Hours, menu_hours_fields, batch_size=5000)
    load_to_db("store_status.csv", Store_Status, store_status_fields, batch_size=20000)
    load_to_db("store_timezones.csv", Store_Timezone, store_timezones, batch_size=5000)


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Time taken: {round(time() - start_time, 2)}s\n")
