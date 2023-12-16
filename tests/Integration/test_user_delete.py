import pytest

@pytest.fixture
def setup_exist_user(client):
    client.post("/api/users", json={
        "id": "3b27d130-9a97-4752-8690-d4d551120a83",
        "email": "testuser@email.com",
        "username": "testuser",
        "password": "Testuser.123",
        "name": "Test User",
        "phone": "0912345678",
    })
    client.post("/api/users", json={
        "id": "3b27d130-9a97-4752-8690-d4d551120a84",
        "email": "testuser1@email.com",
        "username": "testuser1",
        "password": "Testuser.123",
        "name": "Test User 1",
        "phone": "0912345678",
    })
    yield
    client.delete("/api/users/testuser")
    client.delete("/api/users/testuser1")


def assert_status_code_and_error_message(
    client, expected_status_code, expected_message
):
    response = client.delete("/api/users/3b27d130-9a97-4752-8690-d4d551120a83")
    assert response.status_code == expected_status_code
    assert expected_message in response.json["message"]


class TestDeleteUserApi:
    def test_not_existed_user(self, client):
        assert_status_code_and_error_message(
            client,
            404,
            f"User not found",
        )

    @pytest.mark.usefixtures("setup_exist_user")
    def test_deleted_user(self, client):
        client.delete("/api/users/3b27d130-9a97-4752-8690-d4d551120a83")
        assert_status_code_and_error_message(
            client,
            409,
            f"User `testuser` already deleted",
        )

    @pytest.mark.usefixtures("setup_exist_user")
    def test_one(self, client):
        response = client.delete("/api/users/3b27d130-9a97-4752-8690-d4d551120a83")
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
        
