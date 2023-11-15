import os
import aiohttp
import random

from aiohttp import web

from gidgethub import routing, sansio
from gidgethub import aiohttp as gh_aiohttp

routes = web.RouteTableDef()

router = routing.Router()

@router.register("issues", action="opened")
async def issue_opened_event(event, gh, *args, **kwargs):
    """
    Whenever an issue is opened, greet the author and say thanks.
    """
    url = event.data["issue"]["comments_url"]
    author = event.data["issue"]["user"]["login"]

    message = f"Thanks for the report @{author}! I will look into it ASAP! (I'm a bot)."
    await gh.post(url, data={"body": message})

@routes.post("/")
async def main(request):
    body = await request.read()

    secret = os.getenv("GH_SECRET")
    oauth_token = os.getenv("GH_AUTH")

    print("secret", secret)
    print("oauth_token", oauth_token)

    event = sansio.Event.from_http(request.headers, body, secret=secret)
    async with aiohttp.ClientSession() as session:
        gh = gh_aiohttp.GitHubAPI(session, "Hatim001",
                                  oauth_token=oauth_token)
        await router.dispatch(event, gh)
    return web.Response(status=200)


if __name__ == "__main__":
    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)

    key0 = [] 
    while len(key0)<10: 
        while True: 
            candidate = random.randint(0, 9) 
            if candidate in key0: 
                continue 
            key0.append(candidate) 
    
    key1 = [] 
    while len(key1)<10: 
        while True: 
            candidate = random.randint(10,19) 
            if candidate in key1: 
                continue 
            key1.append(candidate) 

    web.run_app(app, port=port)