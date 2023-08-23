import aiohttp
import asyncio

from pyyardian.async_client import AsyncYardianClient

async def main():
    async with aiohttp.ClientSession() as session:
        cli = AsyncYardianClient(session, "host", "access_token")
        print(await cli.fetch_device_state())

if __name__ == "__main__":
    asyncio.run(main())