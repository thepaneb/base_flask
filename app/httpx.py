import asyncio
import time
import httpx

client = httpx.AsyncClient()


async def download_site(url):
    global client
    response = await client.get(url)
    print("Read {0} from {1}".format(len(response.content), url))


async def download_all_sites(sites):
    tasks = []
    for url in sites:
        tasks.append(download_site(url))
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    sites = [
        "https://www.jython.org",
        "http://olympus.realpython.org/dice",
    ] * 12
    start_time = time.time()
    asyncio.run(download_all_sites(sites))
    duration = time.time() - start_time
    print(f"{len(sites)} async i/o calls in {duration} seconds")