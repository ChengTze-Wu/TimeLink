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
    response_messages = " ".join(response.json["message"])
    assert expected_message in response_messages


class TestCreateUserApi:
    def test_invalid_content_type(self, client, client_json_data):
        response = client.post("/api/users", data=client_json_data)
        assert response.status_code == 400
        response_messages = " ".join(response.json["message"])
        assert "Content-Type must be application/json" in response_messages

    def test_empty_json_body(self, client):
        response = client.post("/api/users", json={})
        assert response.status_code == 400
        response_messages = " ".join(response.json["message"])
        assert "Request body must not be empty" in response_messages

    @pytest.mark.parametrize(
        "field, value, expected_message",
        [
            ("password", "test", "Invalid field: password"),
            ("email", "test", "Invalid field: email"),
            ("password", "", "Invalid field: password"),
            ("email", "", "Invalid field: email"),
            ("name", 123, "Invalid types: name"),
            ("password", 123, "Invalid types: password"),
            ("email", 123, "Invalid field: email"),
            ("username", 123, "Invalid types: username"),
            ("name", "t" * 51, "Fields with too long values: name"),
            ("password", "t" * 101, "Fields with too long values: password"),
            ("email", "t" * 101, "Fields with too long values: email"),
            ("username", "t" * 101, "Fields with too long values: username"),
        ],
    )
    def test_invalid_input(
        self, client, client_json_data, field, value, expected_message
    ):
        client_json_data[field] = value
        assert_status_code_and_error_message(
            client, client_json_data, 400, expected_message
        )

    def test_invalid_email_and_password(self, client, client_json_data):
        client_json_data["email"] = "test"
        client_json_data["password"] = "test"
        assert_status_code_and_error_message(
            client, client_json_data, 400, "Invalid field"
        )

    def test_existed_email(self, client, client_json_data):
        client.post("/api/users", json=client_json_data)
        client_json_data["username"] = "test2"
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
