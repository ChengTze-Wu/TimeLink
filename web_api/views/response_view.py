'''
Author: Cheng-Tze Wu
Date: 2023-12-18
Contact: chengtzewu@gmail.com
'''

from typing import Tuple, Optional


class RESTfulResponse:
    '''
    RESTfulResponse is a class that handles the serialization of data
    to be returned to the client.

    Attributes:
        data (dict | list): data to be serialized
        hide_fields (list): list of fields to be hidden
        pagination (tuple): pagination data (page, per_page, total_items)

    Methods:
        to_serializable: return serialized data


    Basic Example:
        >>> from web_api.views.response_view import RESTfulResponse
        >>> result_data = {
                "name": "John Doe",
                "age": 30,
                "email": "john@email.com",
            }
        >>> restful_response = RESTfulResponse(
                data=result_data, 
                hide_fields=["age"])
        >>> restful_response.to_serializable()
        {"name": "John Doe", "email": "john@email.com"}

    Example with pagination:
        >>> from web_api.views.response_view import RESTfulResponse
        >>> restful_response = RESTfulResponse(
                data = dataset,
                hide_fields=["age"],
                pagination=(1, 10, 100),
            )
        >>> restful_response.to_serializable()
        {
            "data": [
                {
                    "name": "John Doe",
                    "email": "john@email.com"
                }, ...
            ],
            "pagination": {
                "current_page": 1,
                "next_page": 2,
                "current_page_items": 10,
                "total_pages": 10,
                "total_items": 100,
            },
        }
    '''

    def __init__(
        self,
        data: Optional[dict | list] = None,
        hide_fields: Optional[list] = None,
        pagination: Optional[Tuple[int, int, int]] = None,
    ):
        if data and not isinstance(data, (dict, list)):
            raise TypeError("data type must be dict, list")

        self.__data = data
        self.__hide_fields = hide_fields if hide_fields is not None else []
        self.__pagination = pagination

    def __hide_fields_handler(self, data: dict) -> dict:
        return {
            key: value
            for key, value in data.items()
            if key not in self.__hide_fields
        }

    def __pagination_handler(self, dataset: list) -> dict:
        page, per_page, total_items = self.__pagination
        current_page_items = len(dataset)
        total_pages, has_remainder = divmod(total_items, per_page) if total_items > 0 else (1, 0)
        if has_remainder:
            total_pages += 1
        next_page = page + 1 if page < total_pages else None
        return {
            "current_page": page,
            "next_page": next_page,
            "current_page_items": current_page_items,
            "total_pages": total_pages,
            "total_items": total_items,
        }

    def __handle(self):
        if isinstance(self.__data, list):
            dataset = [self.__hide_fields_handler(data) for data in self.__data]
            if self.__pagination:
                return {"data": dataset, "pagination": self.__pagination_handler(dataset)}
            return dataset
        if isinstance(self.__data, object):
            return self.__hide_fields_handler(self.__data)
        return {}

    def to_serializable(self) -> dict | list:
        if not self.__data:
            if self.__pagination:
                return {"data": [], "pagination": self.__pagination_handler([])}
            return [] if isinstance(self.__data, list) else {}
        return self.__handle()