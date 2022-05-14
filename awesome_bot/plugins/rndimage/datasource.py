import aiohttp

async def fetch2(session, url):
    async with session.get(url) as response:
        return await response.read()

async def download_image(url):
    async with aiohttp.ClientSession() as session:
        try:
            image = await fetch2(session, url)
            if len(image) > 200:
                return image
            else:
                return None
        except:
            return None