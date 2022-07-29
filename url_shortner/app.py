import logging
from argparse import Namespace

from aiohttp import web
from aiohttp.web_app import Application
from aiohttp_apispec import setup_aiohttp_apispec, validation_middleware
from dotenv import load_dotenv

from url_shortner.api.middlewares import error_middleware
from url_shortner.api.views import VIEWS


def setup_logging(application: web.Application) -> None:
    logging.basicConfig(level=logging.DEBUG)
    application.logger = logging.getLogger(__name__)


def create_app(args: Namespace) -> Application:
    if args.env_file:
        load_dotenv(dotenv_path=args.env_file)
    application = web.Application()

    setup_logging(application)

    for view in VIEWS:
        application.logger.debug('Registering handler %r as %r', view, view.URL_PATH)
        application.router.add_view(view.URL_PATH, view)

    application.middlewares.append(validation_middleware)
    application.middlewares.append(error_middleware)

    setup_aiohttp_apispec(
        app=application,
        title="API REFERENCE",
        version="v1",
        url="/swagger.json",
        swagger_path="/swagger"
    )

    return application
