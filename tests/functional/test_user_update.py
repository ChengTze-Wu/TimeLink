import pytest

@pytest.fixture
def setup_exist_user(client):
    client.post("/api/users", json={
        "email": "testuser@email.com",
        "username": "testuser",
        "password": "Testuser.123",
        "name": "Test User",
        "phone": "0912345678",
    })
    client.post("/api/users", json={
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
    client,  json_data, expected_status_code, expected_message
):
    response = client.put("/api/users/testuser", json=json_data)
    assert response.status_code == expected_status_code
    assert expected_message in response.json["message"]


class TestUpdateUserApi:
    def test_invalid_content_type(self, client):
        response = client.put("/api/users/testuser", data={"username": "testuser2"})
        assert response.status_code == 400
        assert "Content-Type must be application/json" in response.json["message"]


    def test_empty_json_body(self, client):
        response = client.put("/api/users/testuser", json={})
        assert response.status_code == 400
        assert "Request body must not be empty" in response.json["message"]


    @pytest.mark.parametrize(
        "field, value, expected_message",
        [
            ("name", 123, "Fields with invalid types: name"),
            ("password", 123, "Fields with invalid types: password"),
            ("email", 123, "Fields with invalid types: email"),
            ("username", 123, "Fields with invalid types: username"),
            ("phone", 123, "Fields with invalid types: phone"),
            ("is_active", 123, "Fields with invalid types: is_active"),
            ("is_deleted", 123, "Fields with invalid types: is_deleted"),
            ("name", "t" * 51, "Fields with invalid lengths: name"),
            ("password", "t" * 101, "Fields with invalid lengths: password"),
            ("email", "t" * 101, "Fields with invalid lengths: email"),
            ("username", "t" * 101, "Fields with invalid lengths: username"),
            ("phone", "t" * 51, "Fields with invalid lengths: phone"),
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
            "Fields with invalid values: email, password"
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
            f"User `testuser` not found",
        )


    @pytest.mark.usefixtures("setup_exist_user")
    def test_one(self, client):
        response = client.put("/api/users/testuser", json={"name": "Test User 2"})
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
