import os

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers
import aiohttp_cors
import logging



def run() -> None:
    """
    Entry point of the application.
    """

    app = register_graphql_handlers(
        app=web.Application(),
        engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
        engine_modules=[
            "server.query_resolvers",
        ],
        executor_http_endpoint="/graphql/",
        executor_http_methods=["POST"],
        graphiql_enabled=False,
    )

    # `aiohttp_cors.setup` returns `aiohttp_cors.CorsConfig` instance.
    # The `cors` instance will store CORS configuration for the
    # application.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["POST", "OPTIONS"]
        )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    logging.basicConfig(level=logging.INFO)

    web.run_app(
        app,
        host="0.0.0.0",
        port=4000,
    )
