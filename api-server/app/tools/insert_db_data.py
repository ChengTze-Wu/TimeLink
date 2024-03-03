import os
from sqlalchemy import create_engine
from sqlalchemy import text
from faker import Faker
from werkzeug.security import generate_password_hash
import time

DATABASE = os.getenv("DATABASE")
if DATABASE is None:
    raise ValueError("DATABASE Environment Variable is not set")

fake = Faker(locale="zh_TW")
engine = create_engine(DATABASE, echo=False)


def insert_users_data(num: int = 100):
    list_of_fake_data = []
    hashed_password = generate_password_hash("P@ssw0rd123")
    for i in range(num):
        username = f"{fake.user_name()}{i}"
        datetime = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
        list_of_fake_data.append(
            {
                "id": fake.uuid4(),
                "email": f"{username}@mail.com",
                "username": username,
                "password": hashed_password,
                "name": fake.name(),
                "phone": fake.phone_number(),
                "is_active": True,
                "is_deleted": False,
                "created_at": datetime,
                "updated_at": datetime,
            }
        )

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE user_account CASCADE;"))
        conn.execute(
            text(
                """
            INSERT INTO user_account (id, email, username, password, name, phone, is_active, is_deleted, created_at, updated_at)
            VALUES (:id, :email, :username, :password, :name, :phone, :is_active, :is_deleted, :created_at, :updated_at)
        """
            ),
            list_of_fake_data,
        )
        conn.commit()


def insert_services_data(num: int = 100):
    SERVICES = [
        "剪髮",
        "染髮",
        "燙髮",
        "護髮",
        "按摩",
        "美甲",
        "美睫",
        "美容",
        "美體",
        "其他",
        "燙睫毛",
        "燙眉毛",
        "掃毛",
        "剃毛",
        "修眉",
        "修鬍子",
        "掃地",
        "洗碗",
        "洗衣服",
        "烘衣服",
        "燙衣服",
        "燙襯衫",
        "燙西裝",
        "燙裙子",
        "燙褲子",
    ]
    fake = Faker(locale="zh_TW")
    list_of_fake_data = []
    for _ in range(num):
        datetime = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
        list_of_fake_data.append(
            {
                "id": fake.uuid4(),
                "name": fake.random_element(SERVICES),
                "price": fake.pyint(),
                "image": fake.image_url(),
                "description": fake.text(),
                "is_active": True,
                "is_deleted": False,
                "created_at": datetime,
                "updated_at": datetime,
            }
        )

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE service CASCADE;"))
        conn.execute(
            text(
                """
            INSERT INTO service (id, name, price, image, description, is_active, is_deleted, created_at, updated_at)
            VALUES (:id, :name, :price, :image, :description, :is_active, :is_deleted, :created_at, :updated_at)
        """
            ),
            list_of_fake_data,
        )
        conn.commit()


def insert_role_data():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE role CASCADE;"))
        conn.execute(
            text(
                """
            INSERT INTO role (id, name)
            VALUES (:id, :name)
        """
            ),
            [
                {"id": fake.uuid4(), "name": "ADMIN"},
                {"id": fake.uuid4(), "name": "GROUP_OWNER"},
                {"id": fake.uuid4(), "name": "GROUP_MEMBER"},
            ],
        )
        conn.commit()


def insert_appointments_data(num: int = 1000000):
    USERS = [
        'b49c010b-8aa9-4b52-a4be-13a626aec022',
        'f8fa5ed5-6895-40e3-8bc3-67d5257aff0c',
        '32d2581c-53ec-4e36-aed5-f1d25fcc4e14'
    ]

    SERVICES = [
        '54c7484d-36a6-4ce2-ace7-986aed2df2cb',
        '9603f819-ee44-4a4a-a903-ba7fb8c120fe',
        '07f7b593-08a1-4510-bd62-1097a6bdc632',
        'fad06634-312a-43ce-892e-312bde613b74',
        '0d5f2640-e9f2-4a4a-96f9-eb88e9ad9569',
    ]

    fake = Faker(locale="zh_TW")
    list_of_fake_data = []

    fake_data_produce_start_time = time.time()
    print("Fake Data Produce Start:")
    for _ in range(num):
        print(f"\r{'#' * int(_ / num * 100)}", end="")
        datetime = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
        reserved_at = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
        list_of_fake_data.append(
            {
                "id": fake.uuid4(),
                "user_id": fake.random_element(USERS),
                "service_id": fake.random_element(SERVICES),
                "notes": fake.text(200),
                "reserved_at": reserved_at,
                "is_active": True,
                "is_deleted": False,
                "created_at": datetime,
                "updated_at": datetime,
            }
        )
    fake_data_produce_end_time = time.time()
    print(f"Fake Data Produce End, Spend Time: {fake_data_produce_end_time - fake_data_produce_start_time: .3f} seconds")
    print("Insert DB Start...")
    insert_db_start_time = time.time()
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE appointment CASCADE;"))
        conn.execute(
            text(
                """
                INSERT INTO appointment (id, user_id, service_id, reserved_at, notes, is_active, is_deleted, created_at, updated_at)
                VALUES (:id, :user_id, :service_id, :reserved_at, :notes, :is_active, :is_deleted, :created_at, :updated_at)
                """
            ),
            list_of_fake_data,
        )
        conn.commit()
    insert_db_end_time = time.time()
    print(f"Insert DB End, Spend Time: {insert_db_end_time - insert_db_start_time: .3f} seconds")
    print(f"\nAll Done. Total Time: {insert_db_end_time - fake_data_produce_start_time :.3f} seconds")


def turncate_table(table_name: str):
    with engine.connect() as conn:
        conn.execute(text(f"TRUNCATE TABLE {table_name} CASCADE;"))
        conn.commit()

if __name__ == "__main__":
    insert_appointments_data(10000)
