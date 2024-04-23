import asyncio

import aiohttp


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    url = "http://127.0.0.1:8000/moderation/labels"

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for i in range(5000)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
