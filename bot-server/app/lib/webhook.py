# Copyright (c) 2024 ChengTze.

import asyncio
import inspect
from linebot.v3.webhook import WebhookHandler
from linebot.v3.webhooks import MessageEvent
from linebot.v3.utils import LOGGER, PY3


class AsyncWebhookHandler(WebhookHandler):
    '''
    Async Webhook Handler.

    This class is a subclass of WebhookHandler from line bot sdk.
    It is modified to support async event handlers.
    '''
    def __init__(self, channel_secret):
        super().__init__(channel_secret)

    def add(self, event, message=None):
        def decorator(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Handler must be a coroutine function")

            if isinstance(message, (list, tuple)):
                for it in message:
                    self.__add_handler(func, event, message=it)
            else:
                self.__add_handler(func, event, message=message)

            return func

        return decorator

    def default(self):
        def decorator(func):
            if not asyncio.iscoroutinefunction(func):
                raise TypeError("Handler must be a coroutine function")

            self._default = func
            return func

        return decorator

    async def handle(self, body, signature):
        payload = self.parser.parse(body, signature, as_payload=True)

        for event in payload.events:
            func = None
            key = None

            if isinstance(event, MessageEvent):
                key = self.__get_handler_key(
                    event.__class__, event.message.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                key = self.__get_handler_key(event.__class__)
                func = self._handlers.get(key, None)

            if func is None:
                func = self._default

            if func is None:
                LOGGER.info('No handler of ' + key + ' and no default handler')
            else:
                await self.__invoke_func(func, event, payload)

    def __add_handler(self, func, event, message=None):
        key = self.__get_handler_key(event, message=message)
        self._handlers[key] = func

    @classmethod
    async def __invoke_func(cls, func, event, payload):
        (has_varargs, args_count) = cls.__get_args_count(func)
        if has_varargs or args_count == 2:
            await func(event, payload.destination)
        elif args_count == 1:
            await func(event)
        else:
            await func()
        
    @staticmethod
    def __get_args_count(func):
        if PY3:
            arg_spec = inspect.getfullargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))
        else:
            arg_spec = inspect.getargspec(func)
            return (arg_spec.varargs is not None, len(arg_spec.args))
        
    @staticmethod
    def __get_handler_key(event, message=None):
        if message is None:
            return event.__name__
        else:
            return event.__name__ + "_" + message.__name__