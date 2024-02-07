import pytest
from views.response_view import RESTfulResponse


@pytest.fixture
def fake_result_data():
    return {
        "id": "1",
        "email": "john@gmail.com",
        "username": "john123",
        "password": "123456",
        "name": "John",
    }


class TestRESTfulResponse:
    def test_instantiation_without_arguments(self):
        restful_response = RESTfulResponse()
        assert isinstance(restful_response, RESTfulResponse)

    def test_serialization_with_all_fields(self, fake_result_data):
        restful_response = RESTfulResponse(data=fake_result_data)
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == fake_result_data

    def test_serialization_with_hidden_fields(self, fake_result_data: dict):
        restful_response = RESTfulResponse(data=fake_result_data, hide_fields=["name"])
        assert isinstance(restful_response.to_serializable(), dict)
        del fake_result_data["name"]
        assert restful_response.to_serializable() == fake_result_data

    def test_serialization_with_list_data(self, fake_result_data: dict):
        restful_response = RESTfulResponse(data=[fake_result_data, fake_result_data])
        assert isinstance(restful_response.to_serializable(), list)
        assert restful_response.to_serializable() == [
            fake_result_data,
            fake_result_data,
        ]

    def test_serialization_with_hidden_fields_and_list_data(
        self, fake_result_data: dict
    ):
        restful_response = RESTfulResponse(
            data=[fake_result_data, fake_result_data], hide_fields=["name"]
        )
        assert isinstance(restful_response.to_serializable(), list)
        del fake_result_data["name"]
        assert restful_response.to_serializable() == [
            fake_result_data,
            fake_result_data,
        ]

    def test_serialization_with_empty_list_data(self):
        restful_response = RESTfulResponse(data=[])
        assert isinstance(restful_response.to_serializable(), list)
        assert restful_response.to_serializable() == []

    def test_serialization_with_empty_data(self):
        restful_response = RESTfulResponse()
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {}

    def test_serialization_with_non_dict_or_list_data(self):
        with pytest.raises(TypeError):
            RESTfulResponse(data=1)

    def test_serialization_with_pagination_all_items_on_one_page(
        self, fake_result_data: dict
    ):
        restful_response = RESTfulResponse(
            data=[fake_result_data, fake_result_data],
            pagination=(1, 2, 2),
        )
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {
            "data": [fake_result_data, fake_result_data],
            "pagination": {
                "current_page": 1,
                "next_page": None,
                "current_page_items": 2,
                "total_pages": 1,
                "total_items": 2,
            },
        }

    def test_serialization_with_pagination_multiple_pages(self, fake_result_data: dict):
        restful_response = RESTfulResponse(
            data=[fake_result_data, fake_result_data],
            pagination=(1, 2, 4),
        )
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {
            "data": [fake_result_data, fake_result_data],
            "pagination": {
                "current_page": 1,
                "next_page": 2,
                "current_page_items": 2,
                "total_pages": 2,
                "total_items": 4,
            },
        }

    def test_serialization_with_hidden_fields_and_pagination(
        self, fake_result_data: dict
    ):
        restful_response = RESTfulResponse(
            data=[fake_result_data, fake_result_data],
            hide_fields=["name"],
            pagination=(1, 2, 4),
        )
        assert isinstance(restful_response.to_serializable(), dict)
        del fake_result_data["name"]
        assert restful_response.to_serializable() == {
            "data": [fake_result_data, fake_result_data],
            "pagination": {
                "current_page": 1,
                "next_page": 2,
                "current_page_items": 2,
                "total_pages": 2,
                "total_items": 4,
            },
        }

    def test_serialization_with_pagination_and_empty_data(self):
        restful_response = RESTfulResponse(pagination=(1, 2, 0))
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {
            "data": [],
            "pagination": {
                "current_page": 1,
                "next_page": None,
                "current_page_items": 0,
                "total_pages": 1,
                "total_items": 0,
            },
        }

    def test_serialization_with_pagination_and_empty_data_and_hide_fields(self):
        restful_response = RESTfulResponse(pagination=(1, 2, 0), hide_fields=["name"])
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {
            "data": [],
            "pagination": {
                "current_page": 1,
                "next_page": None,
                "current_page_items": 0,
                "total_pages": 1,
                "total_items": 0,
            },
        }

    def test_serialization_with_pagination_and_empty_data_and_hide_fields_and_data(
        self,
    ):
        restful_response = RESTfulResponse(
            data=[],
            pagination=(1, 2, 0),
            hide_fields=["name"],
        )
        assert isinstance(restful_response.to_serializable(), dict)
        assert restful_response.to_serializable() == {
            "data": [],
            "pagination": {
                "current_page": 1,
                "next_page": None,
                "current_page_items": 0,
                "total_pages": 1,
                "total_items": 0,
            },
        }
