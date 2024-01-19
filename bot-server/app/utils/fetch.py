import os
import httpx

BOT_VERSION = f"/{os.getenv("BOT_VERSION", "0.0.1")}"

class APIServerFetchClient:
    def __init__(self, base_url: str | None = None):
        self.base_url = os.getenv("API_SERVER_HOST", base_url)
        self.headers = {'user-agent': f'TimeLink-Line-Bot{BOT_VERSION}'}
        self.timeout = 2

    async def get(self, endpoint, **kwargs):
        return await self._request("GET", endpoint, **kwargs)

    async def post(self, endpoint, data, **kwargs):
        return await self._request("POST", endpoint, json=data, **kwargs)

    async def put(self, endpoint, data, **kwargs):
        return await self._request("PUT", endpoint, json=data, **kwargs)

    async def delete(self, endpoint, **kwargs):
        return await self._request("DELETE", endpoint, **kwargs)

    async def _request(self, method, endpoint, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            response = await client.request(method, f'{self.base_url}{endpoint}', headers=self.headers, timeout=self.timeout, **kwargs)
            return response