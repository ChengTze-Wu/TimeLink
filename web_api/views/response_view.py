from typing import Tuple, Optional


class RESTfulResponse:
    def __init__(
        self,
        data: Optional[dict | list] = None,
        hide_fields: Optional[list] = None,
        pagination: Optional[Tuple[int, int, int]] = None, # (page, per_page, total_items)
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