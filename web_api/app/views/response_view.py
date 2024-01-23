'''
Author: Cheng-Tze Wu
Date: 2023-12-18
Contact: chengtzewu@gmail.com
'''
from typing import Tuple, Optional, List, Dict, Union

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
        >>> from views.response_view import RESTfulResponse
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
        >>> from views.response_view import RESTfulResponse
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
                }, app.
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
        data: Optional[Union[Dict, List]] = None,
        hide_fields: Optional[List[str]] = [],
        pagination: Optional[Tuple[int, int, int]] = None,
    ):
        self.data = data
        self._validate_data(self.data)
        self.hide_fields = hide_fields
        self.pagination = pagination

    @staticmethod
    def _validate_data(data):
        if data and not isinstance(data, (dict, list)):
            raise TypeError("Data type must be dict or list")

    def _apply_field_filters(self, data_item: Dict) -> Dict:
        return {key: value for key, value in data_item.items() if key not in self.hide_fields}

    def _generate_pagination_info(self, current_page_items: int) -> Dict[str, Union[int, None]]:
        page, per_page, total_items = self.pagination
        total_pages = max((total_items + per_page - 1) // per_page, 1)
        next_page = page + 1 if page < total_pages else None

        return {
            "current_page": page,
            "next_page": next_page,
            "current_page_items": current_page_items,
            "total_pages": total_pages,
            "total_items": total_items,
        }

    def _process_data(self) -> Union[Dict, List]:
        processed_data = {}

        if isinstance(self.data, list):
            processed_data = [self._apply_field_filters(item) for item in self.data]

        if isinstance(self.data, dict):
            processed_data = self._apply_field_filters(self.data)

        if self.pagination:
            processed_data = [] if not processed_data else processed_data
            pagination_info = self._generate_pagination_info(len(processed_data) if isinstance(self.data, list) else 0)
            return {"data": processed_data, "pagination": pagination_info}

        return processed_data

    def to_serializable(self) -> Union[Dict, List]:
        return self._process_data()