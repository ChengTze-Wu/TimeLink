import pytest
from app import create_app


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": "postgresql+psycopg2://tltester:passw0rd123@127.0.0.1:55432/2023-timelink-test",
        }
    )

    # other setup can go here
    with app.app_context():
        from db.exec import init_db

        init_db()

    yield app

    # clean up / reset resources here
    with app.app_context():
        from db.exec import drop_db

        drop_db()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
