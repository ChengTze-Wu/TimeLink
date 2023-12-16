import pytest


@pytest.fixture
def client_json_data() -> dict:
    return {
        "email": "test@test.com",
        "username": "test",
        "password": "Test.1234",
        "name": "test",
    }


def assert_status_code_and_error_message(
    client, json_data, expected_status_code, expected_message
):
    response = client.post("/api/users", json=json_data)
    assert response.status_code == expected_status_code
    assert expected_message == response.json["message"]


class TestCreateUserApi:
    def test_invalid_content_type(self, client, client_json_data):
        response = client.post("/api/users", data=client_json_data)
        assert response.status_code == 400
        assert "Content-Type must be application/json" == response.json["message"]

    def test_empty_json_body(self, client):
        response = client.post("/api/users", json={})
        assert response.status_code == 400
        assert "Request body must not be empty" == response.json["message"]

    @pytest.mark.parametrize(
        "field, value, expected_message",
        [
            ("password", "test", "Fields with invalid values: password"),
            ("email", "test", "Fields with invalid values: email"),
            ("name", "", "Missing required fields: name"),
            ("password", "", "Missing required fields: password"),
            ("email", "", "Missing required fields: email"),
            ("username", "", "Missing required fields: username"),
            ("name", 123, "Fields with invalid types: name"),
            ("password", 123, "Fields with invalid types: password"),
            ("email", 123, "Fields with invalid types: email"),
            ("username", 123, "Fields with invalid types: username"),
            ("name", "t" * 51, "Fields with invalid lengths: name"),
            ("password", "t" * 101, "Fields with invalid lengths: password"),
            ("email", "t" * 101, "Fields with invalid lengths: email"),
            ("username", "t" * 101, "Fields with invalid lengths: username"),
        ],
    )
    def test_invalid_input(
        self, client, client_json_data, field, value, expected_message
    ):
        client_json_data[field] = value
        assert_status_code_and_error_message(
            client, client_json_data, 400, expected_message
        )

    def test_multiple_empty_input(self, client, client_json_data):
        client_json_data["name"] = ""
        client_json_data["password"] = ""
        client_json_data["email"] = ""
        assert_status_code_and_error_message(
            client,
            client_json_data,
            400,
            "Missing required fields: email, password, name",
        )

    def test_invalid_email_and_password(self, client, client_json_data):
        client_json_data["email"] = "test"
        client_json_data["password"] = "test"
        assert_status_code_and_error_message(
            client, client_json_data, 400, "Fields with invalid values: email, password"
        )

    def test_existed_email(self, client, client_json_data):
        client.post("/api/users", json=client_json_data)
        assert_status_code_and_error_message(
            client,
            client_json_data,
            409,
            f"Email `{client_json_data['email']}` already exists",
        )

    def test_existed_username(self, client, client_json_data):
        client.post("/api/users", json=client_json_data)
        client_json_data["email"] = "test2@test.com"
        assert_status_code_and_error_message(
            client,
            client_json_data,
            409,
            f"Username `{client_json_data['username']}` already exists",
        )

    def test_create_one(self, client, client_json_data: dict):
        response = client.post("/api/users", json=client_json_data)
        assert response.status_code == 201
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
