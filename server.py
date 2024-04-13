from aiohttp import web
import aiohttp_cors
async def handler(request):
    print("Here")
    return web.Response(text="Hello world")


async def enhance(request: web.Request) -> web.Response:
    data = await request.post()
    username = data.get('username')
    print(username)

    return web.Response(text=f"OK")



app = web.Application()
app.add_routes([web.get('/', handler)])
app.add_routes([web.post('/enhance', enhance)])

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
        allow_credentials=True,
        expose_headers="*",
        allow_headers="*"
    )
})

for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app)

