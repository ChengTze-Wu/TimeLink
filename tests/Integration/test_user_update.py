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
    client.delete("/api/users/3b27d130-9a97-4752-8690-d4d551120a83")
    client.delete("/api/users/3b27d130-9a97-4752-8690-d4d551120a84")


def assert_status_code_and_error_message(
    client,  json_data, expected_status_code, expected_message
):
    response = client.put("/api/users/3b27d130-9a97-4752-8690-d4d551120a83", json=json_data)
    assert response.status_code == expected_status_code
    response_messages = " ".join(response.json["message"])
    assert expected_message in response_messages


class TestUpdateUserApi:
    def test_invalid_content_type(self, client):
        response = client.put("/api/users/3b27d130-9a97-4752-8690-d4d551120a83", data={"username": "testuser2"})
        assert response.status_code == 400
        response_messages = " ".join(response.json["message"])
        assert "Content-Type must be application/json" in response_messages


    def test_empty_json_body(self, client):
        response = client.put("/api/users/3b27d130-9a97-4752-8690-d4d551120a83", json={})
        assert response.status_code == 400
        response_messages = " ".join(response.json["message"])
        assert "Request body must not be empty" in response_messages


    @pytest.mark.parametrize(
        "field, value, expected_message",
        [
            ("name", 123, "Invalid types: name"),
            ("password", 123, "Invalid types: password"),
            ("email", 123, "Invalid types: email"),
            ("username", 123, "Invalid types: username"),
            ("phone", 123, "Invalid types: phone"),
            ("is_active", 123, "Invalid types: is_active"),
            ("is_deleted", 123, "Invalid types: is_deleted"),
            ("name", "t" * 51, "Fields with too long values: name"),
            ("password", "t" * 101, "Fields with too long values: password"),
            ("email", "t" * 101, "Fields with too long values: email"),
            ("username", "t" * 101, "Fields with too long values: username"),
            ("phone", "t" * 51, "Fields with too long values: phone"),
        ],
    )
    def test_invalid_input(
        self, client, field, value, expected_message
    ):
        assert_status_code_and_error_message(
            client, {field:value}, 400, expected_message
        )


    def test_invalid_email_and_password(self, client):
        assert_status_code_and_error_message(
            client, 
            {
                "email": "test",
                "password": "test",
            }, 
            400, 
            "Invalid field"
        )


    @pytest.mark.usefixtures("setup_exist_user")
    def test_existed_email(self, client):
        assert_status_code_and_error_message(
            client,
            {"email": "testuser1@email.com"},
            409,
            f"Email `testuser1@email.com` already exists",
        )


    @pytest.mark.usefixtures("setup_exist_user")
    def test_existed_username(self, client):
        assert_status_code_and_error_message(
            client,
            {"username": "testuser1"},
            409,
            f"Username `testuser1` already exists",
        )


    def test_update_not_existed_user(self, client):
        assert_status_code_and_error_message(
            client,
            {"name": "Test User 2"},
            404,
            f"User not found",
        )


    @pytest.mark.usefixtures("setup_exist_user")
    def test_one(self, client):
        response = client.put("/api/users/3b27d130-9a97-4752-8690-d4d551120a83", json={"name": "Test User 2"})
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
        assert response.json["is_active"] is True
        assert response.json["is_deleted"] is False
        assert response.json["name"] == "Test User 2"
