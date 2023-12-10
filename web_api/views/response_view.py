from web_api.db.models import BaseModel
from typing import List, Tuple

class RESTfulResponse():
    def __init__(self, model: List[BaseModel]|BaseModel, hide_fields: list=[], pagination: Tuple[int,int,int]=(None,None,None)):
        self.__model = model
        self.__hide_fields = hide_fields
        self.__pagination = pagination  # (page, per_page, total_items)

    def __hide_fields_handler(self, model: BaseModel) -> dict:
        dict_data = model.to_dict()
        for field in self.__hide_fields:
            if field in dict_data:
                dict_data.pop(field)
        return dict_data

    def __pagination_handler(self, data: List[dict]) -> dict:
        page, per_page, total_items = self.__pagination
        current_page_items = len(data)
        total_pages = total_items // per_page + 1 if total_items % per_page else total_items // per_page
        next_page = page + 1 if page < total_pages else None
        return {
            'current_page': page,
            'next_page': next_page,
            'current_page_items': current_page_items,
            'total_pages': total_pages,
            'total_items': total_items,
        }
    
    def __handle(self):
        if isinstance(self.__model, list):
            data = [self.__hide_fields_handler(model) for model in self.__model]
            if self.__pagination:
                return {
                    'data': data,
                    'pagination': self.__pagination_handler(data)
                }
            return data
        if isinstance(self.__model, object):
            return self.__hide_fields_handler(self.__model)
        return {}

    def to_dict(self) -> dict:
        return self.__handle()