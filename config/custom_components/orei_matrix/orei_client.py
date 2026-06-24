import aiohttp
import json


class OreiHttpClient:
    def __init__(self, host:str, session: aiohttp.ClientSession):
        self._host = host
        self._session = session

    def _base_url(self):
        return f"http://{self._host}/cgi-bin/instr"

    async def post(self, payload: dict):
        async with self._session.post(
            self._base_url(),
            json=payload,
        ) as response:
            response.raise_for_status()
            text = await response.text()
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text