import os
import httpx
from abc import ABC, abstractmethod
import redis.asyncio as redis
import logging

class FetchClient(ABC):
    @abstractmethod
    async def get(self, endpoint, **kwargs):
        pass

    @abstractmethod
    async def post(self, endpoint, data, **kwargs):
        pass

    @abstractmethod
    async def put(self, endpoint, data, **kwargs):
        pass

    @abstractmethod
    async def delete(self, endpoint, **kwargs):
        pass


class APIServerFetchClient(FetchClient):
    BOT_VERSION = f"/{os.getenv("BOT_VERSION", "0.0.1")}"

    def __init__(self, base_url: str | None = None):
        self.base_url = os.getenv("API_SERVER_HOST", base_url)
        self.headers = {
            'user-agent': f'TimeLinkBotServer{self.BOT_VERSION}',
            'Authorization': f'Bearer {os.getenv("API_SERVER_ACCESS_TOKEN")}'
        }
        self.__timeout = 2

    def set_timeout(self, timeout: int | float):
        if not isinstance(timeout, int | float):
            raise TypeError("timeout must be int or float")
        if timeout < 0:
            raise ValueError("timeout must be greater than 0")
        self.__timeout = timeout

    async def get(self, endpoint, **kwargs):
        return await self.__request("GET", endpoint, **kwargs)

    async def post(self, endpoint, data: None = None, **kwargs):
        return await self.__request("POST", endpoint, json=data, **kwargs)

    async def put(self, endpoint, data: None = None, **kwargs):
        return await self.__request("PUT", endpoint, json=data, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.__request("DELETE", endpoint, **kwargs)

    async def __request(self, method, endpoint, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, f'{self.base_url}{endpoint}', headers=self.headers, timeout=self.__timeout, **kwargs)
            return response


class RedisClient:
    ENV_REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    ENV_REDIS_PORT = os.getenv("REDIS_PORT", "6379")
    ENV_DB = os.getenv("REDIS_DB", "0")
    ENV_CLIENT_NAME = os.getenv("REDIS_CLIENT_NAME", "TimeLinkBotServer")

    def __init__(self, host: str | None = None, port: int | None = None, db: int = 0, ttl_seconds: int = 60, exc_info: bool = False):
        host = host or self.ENV_REDIS_HOST
        port = port or self.ENV_REDIS_PORT
        db = db or self.ENV_DB
        self._pool = redis.ConnectionPool(host=host, port=port, db=db, decode_responses=True, encoding="utf-8", client_name=self.ENV_CLIENT_NAME)
        self._ex = ttl_seconds
        self._exc_info = exc_info

    async def get(self, key: str) -> str | None:
        try:
            async with redis.Redis(connection_pool=self._pool) as conn:
                return await conn.get(key)
        except redis.ConnectionError as e:
            logging.error("Redis connection error. Skipping get operation.")
            logging.error(e, exc_info=self._exc_info)

    async def set(self, key: str, value: str) -> None:
        try:
            async with redis.Redis(connection_pool=self._pool) as conn:
                await conn.set(key, value, ex=self._ex)
        except redis.ConnectionError as e:
            logging.error("Redis connection error. Skipping set operation.")
            logging.error(e, exc_info=self._exc_info)

    async def delete(self, key: str) -> None:
        try:
            async with redis.Redis(connection_pool=self._pool) as conn:
                await conn.delete(key)
        except redis.ConnectionError as e:
            logging.error("Redis connection error. Skipping delete operation.")
            logging.error(e, exc_info=self._exc_info)

    async def close(self):
        await self._pool.aclose()
        self._pool = None
        logging.info("Redis connection pool all closed.")
