from aiohttp import web

async def handler(request):
    return web.Response(text="Hello world")


async def enhance(request: web.Request) -> web.Response:
    data = await request.post()
    username = data.get('username')
    print(username)

    return web.Response(text=f"OK")



app = web.Application()
app.add_routes([web.get('/', handler)])
app.add_routes([web.post('/enhance', enhance)])

web.run_app(app)

