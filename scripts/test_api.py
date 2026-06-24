# scripts/test_api.py

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "config")
)

import asyncio
import aiohttp

from custom_components.orei_matrix.orei_client import OreiHttpClient
from custom_components.orei_matrix.api import OreiApi


async def main():
    async with aiohttp.ClientSession() as session:

        client = OreiHttpClient(
            host="192.168.1.124",
            session=session
        )

        api = OreiApi(client)

        inputs = await api.get_inputs()
        outputs = await api.get_outputs()

        print(inputs)
        print(outputs)

        await api.set_output_source(4,4)

        print((await api.get_outputs())[3])


asyncio.run(main())