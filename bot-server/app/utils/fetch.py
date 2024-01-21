import os
import httpx

class APIServerFetchClient:
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

    async def post(self, endpoint, data, **kwargs):
        return await self.__request("POST", endpoint, json=data, **kwargs)

    async def put(self, endpoint, data, **kwargs):
        return await self.__request("PUT", endpoint, json=data, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self.__request("DELETE", endpoint, **kwargs)

    async def __request(self, method, endpoint, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, f'{self.base_url}{endpoint}', headers=self.headers, timeout=self.__timeout, **kwargs)
            return response