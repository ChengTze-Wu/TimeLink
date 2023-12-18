from typing import Tuple, Optional, List, Dict, Union

class RESTfulResponse:
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