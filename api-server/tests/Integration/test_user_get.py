import pytest


@pytest.fixture
def setup_exist_user(client):
    client.post(
        "/api/users",
        json={
            "id": "88f73f9b-2402-4a5a-837f-4d151dbd554f",
            "email": "testuser@email.com",
            "username": "testuser",
            "password": "Testuser.123",
            "name": "Test User",
            "phone": "0912345678",
        },
    )
    client.post(
        "/api/users",
        json={
            "id": "88f73f9b-2402-4a5a-837f-4d151dbd553f",
            "email": "testuser1@email.com",
            "username": "testuser1",
            "password": "Testuser.123",
            "name": "Test User 1",
            "phone": "0912345678",
        },
    )
    client.post(
        "/api/users",
        json={
            "id": "88f73f9b-2402-4a5a-837f-4d151dbd552f",
            "email": "testuser2@email.com",
            "username": "testuser2",
            "password": "Testuser.123",
            "name": "Test User 2",
            "phone": "0912345678",
            "is_active": False,
        },
    )
    client.post(
        "/api/users",
        json={
            "id": "88f73f9b-2402-4a5a-837f-4d151dbd551f",
            "email": "testuser3@email.com",
            "username": "testuser3",
            "password": "Testuser.123",
            "name": "Test User 3",
            "phone": "0912345678",
            "is_deleted": True,
        },
    )
    client.post(
        "/api/users",
        json={
            "id": "88f73f9b-2402-4a5a-837f-4d151dbd550f",
            "email": "testuser4@email.com",
            "username": "testuser4",
            "password": "Testuser.123",
            "name": "Test User 4",
            "phone": "0912345678",
            "is_active": False,
            "is_deleted": True,
        },
    )
    yield
    client.delete("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd554f")
    client.delete("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd553f")
    client.delete("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd552f")
    client.delete("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd551f")
    client.delete("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd550f")


def assert_status_code_and_error_message(
    client, expected_status_code, expected_message
):
    response = client.get("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd554f")
    assert response.status_code == expected_status_code
    response_messages = " ".join(response.json["message"])
    assert expected_message in response_messages


class TestGetOneUserApi:
    def test_not_existed_user(self, client):
        assert_status_code_and_error_message(
            client,
            404,
            f"User not found",
        )

    @pytest.mark.usefixtures("setup_exist_user")
    def test_one(self, client):
        response = client.get("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd554f")
        assert response.status_code == 200
        assert set(response.json.keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
            "line_user_id",
        }
        assert response.json["is_deleted"] is False

    @pytest.mark.usefixtures("setup_exist_user")
    def test_deleted_user(self, client):
        response = client.get("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd551f")
        assert response.status_code == 200
        assert set(response.json.keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
            "line_user_id",
        }
        assert response.json["is_deleted"] is True

    @pytest.mark.usefixtures("setup_exist_user")
    def test_disabled_user(self, client):
        response = client.get("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd552f")
        assert response.status_code == 200
        assert set(response.json.keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
            "line_user_id",
        }
        assert response.json["is_active"] is False

    @pytest.mark.usefixtures("setup_exist_user")
    def test_deleted_and_disabled_user(self, client):
        response = client.get("/api/users/88f73f9b-2402-4a5a-837f-4d151dbd550f")
        assert response.status_code == 200
        assert set(response.json.keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "is_active",
            "is_deleted",
            "created_at",
            "updated_at",
            "line_user_id",
        }
        assert response.json["is_active"] is False
        assert response.json["is_deleted"] is True


class TestGetAllUserApi:
    def test_with_empty_db(self, client):
        response = client.get("/api/users")
        assert response.status_code == 200
        assert response.json == {
            "data": [],
            "pagination": {
                "current_page": 1,
                "next_page": None,
                "current_page_items": 0,
                "total_pages": 1,
                "total_items": 0,
            },
        }

    @pytest.mark.usefixtures("setup_exist_user")
    def test_with_dafault_pagination(self, client):
        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json["data"]) == 3
        assert set(response.json["data"][0].keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "created_at",
            "updated_at",
            "line_user_id",
            "is_active",
        }
        assert response.json["pagination"] == {
            "current_page": 1,
            "next_page": None,
            "current_page_items": 3,
            "total_pages": 1,
            "total_items": 3,
        }

    @pytest.mark.usefixtures("setup_exist_user")
    def test_pagination(self, client):
        response = client.get("/api/users?page=1&per_page=2")
        assert response.status_code == 200
        assert len(response.json["data"]) == 2
        assert set(response.json["data"][0].keys()) == {
            "id",
            "email",
            "username",
            "name",
            "phone",
            "created_at",
            "updated_at",
            "line_user_id",
            "is_active",
        }
        assert response.json["pagination"] == {
            "current_page": 1,
            "next_page": 2,
            "current_page_items": 2,
            "total_pages": 2,
            "total_items": 3,
        }
