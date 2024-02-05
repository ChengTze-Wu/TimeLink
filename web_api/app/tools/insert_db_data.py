import os
from sqlalchemy import create_engine
from sqlalchemy import text
from faker import Faker
from werkzeug.security import generate_password_hash

DATABASE = os.getenv('DATABASE')
if DATABASE is None:
    raise ValueError('DATABASE Environment Variable is not set')

fake = Faker(locale='zh_TW')
engine = create_engine(DATABASE, echo=False)

def insert_users_data(num:int=100):
    list_of_fake_data = []
    hashed_password = generate_password_hash('P@ssw0rd123')
    for i in range(num):
        username = f"{fake.user_name()}{i}"
        datetime = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
        list_of_fake_data.append({
            'id': fake.uuid4(),
            'email': f"{username}@mail.com",
            'username': username,
            'password': hashed_password,
            'name': fake.name(),
            'phone': fake.phone_number(),
            'is_active': True,
            'is_deleted': False,
            'created_at': datetime,
            'updated_at': datetime
        })

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE user_account CASCADE;"))
        conn.execute(text("""
            INSERT INTO user_account (id, email, username, password, name, phone, is_active, is_deleted, created_at, updated_at)
            VALUES (:id, :email, :username, :password, :name, :phone, :is_active, :is_deleted, :created_at, :updated_at)
        """), list_of_fake_data)
        conn.commit()



def insert_services_data(num:int=100):
    SERVICES = ['剪髮', '染髮', '燙髮', '護髮', '按摩', 
            '美甲', '美睫', '美容', '美體', '其他', 
            '燙睫毛', '燙眉毛', '掃毛', '剃毛', '修眉', 
            '修鬍子', '掃地', '洗碗', '洗衣服', '烘衣服', 
            '燙衣服', '燙襯衫', '燙西裝', '燙裙子', '燙褲子']
    fake = Faker(locale='zh_TW')
    list_of_fake_data = []
    for _ in range(num):
        datetime = fake.date_time_between(start_date='-1y', end_date='now', tzinfo=None)
        list_of_fake_data.append({
            "id": fake.uuid4(),
            'name': fake.random_element(SERVICES),
            'price': fake.pyint(),
            'image': fake.image_url(),
            'description': fake.text(),
            'is_active': True,
            'is_deleted': False,
            'created_at': datetime,
            'updated_at': datetime
        })

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE service CASCADE;"))
        conn.execute(text("""
            INSERT INTO service (id, name, price, image, description, is_active, is_deleted, created_at, updated_at)
            VALUES (:id, :name, :price, :image, :description, :is_active, :is_deleted, :created_at, :updated_at)
        """), list_of_fake_data)
        conn.commit()


def insert_role_data():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE role CASCADE;"))
        conn.execute(text("""
            INSERT INTO role (id, name)
            VALUES (:id, :name)
        """), [
            {
                "id": fake.uuid4(),
                "name": "ADMIN"
            },
            {
                "id": fake.uuid4(),
                "name": "GROUP_OWNER"
            },
            {
                "id": fake.uuid4(),
                "name": "GROUP_MEMBER"
            }
        ])
        conn.commit()


if __name__ == "__main__":
    insert_role_data()