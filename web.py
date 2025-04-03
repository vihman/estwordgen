# SlingAcademy.com
# main.py
import json
from pathlib import Path

from aiohttp import web

# Create an instance of the web application
app = web.Application()


# Define a handler for the root path
async def root_handler(request):
    return web.FileResponse("html/index.html")
    #return web.Response(
    #    text=f"<h1>Welcome to Sling Academy!</h1><p>{request}</p>", content_type="text/html"
    #)


# Define a handler for the /api path
async def api_handler(request):
    return web.json_response(
        {"status": 200, "message": str(request)}
    )

async def handle_file(request):
    p = Path(f"./html/{request.path}")
    if p.is_file():
        return web.FileResponse(p)
    return web.Response(status=403)

# Add the /api route and its handler to the app

async def api_call(request, *args):
    return web.Response(json.dumps(args))

app.add_routes([
    web.get("/", root_handler),
    web.post("/", api_handler),
    web.get('/{filepath:.*}', handle_file),
    # web.post('/{filepath:.*}', api_call)
    ])

# Run the app
web.run_app(app, host="localhost", port=8080)