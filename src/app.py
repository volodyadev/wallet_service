import logging
import os
import time

import fastapi_jsonrpc as jsonrpc
from fastapi import APIRouter, FastAPI, Request, Response
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from baseapp import App
from exceptions import (
    ElementNotFoundError,
    WalletNotFoundError,
    InsufficientFundsError,
    ComponentIdError,
)
from lifespan import lifespan
from routers import wallet
from settings import print_modes, settings


def register_offline_docs(app: FastAPI) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    static_files_abs_path = os.path.join(current_dir, "./static/docs")

    app.mount(
        "/static",
        StaticFiles(directory=static_files_abs_path),
        name="static",
    )

    docs_router = APIRouter()

    @docs_router.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        logging.debug("Swagger UI route accessed")
        return get_swagger_ui_html(
            openapi_url=app.openapi_url or "",
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/static/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @docs_router.get(
        app.swagger_ui_oauth2_redirect_url or "/oauth2-redirect/",
        include_in_schema=False,
    )
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @docs_router.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url or "",
            title=app.title + " - ReDoc",
            redoc_js_url="/static/redoc.standalone.js",
        )

    app.include_router(router=docs_router, prefix=settings.APP_URL)


def register_logging_middleware(app: FastAPI) -> None:

    @app.middleware("http")
    async def log_request_and_timing(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time()
        logging.debug(
            f"Method: {request.method}, URL: {request.url}, Time: {end_time - start_time:=.2f} sec",  # noqa E501
        )
        return response


def register_global_responses(app: FastAPI) -> None:

    @app.middleware("http")
    async def global_response_middleware(request, call_next):
        response: Response = await call_next(request)

        # Handling global responses
        if response.status_code == 404:
            response.body = b"Page not found"
        elif response.status_code == 500:
            response.body = b"Internal server error"

        return response


def register_cors_middleware(app: FastAPI) -> None:

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ElementNotFoundError)
    async def element_not_found_error_exception(
        request: Request, exc: ElementNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"message": exc.message},
        )

    @app.exception_handler(WalletNotFoundError)
    async def wallet_not_found_error_exception(
        request: Request, exc: WalletNotFoundError
    ):
        return JSONResponse(
            status_code=404,
            content={"message": exc.message},
        )

    @app.exception_handler(InsufficientFundsError)
    async def insufficient_funds_error_exception(
        request: Request, exc: InsufficientFundsError
    ):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message},
        )

    @app.exception_handler(ComponentIdError)
    async def component_id_error_exception(request: Request, exc: ComponentIdError):
        return JSONResponse(
            status_code=400,
            content={"message": exc.message},
        )


def create_app() -> App:
    app = jsonrpc.API(lifespan=lifespan, openapi_url="/openapi.json")
    app.include_router(
        router=wallet.router, prefix=settings.APP_URL + "/wallet", tags=["Кошелек"]
    )

    app.openapi_version = "3.0.0"

    app.title = "wallet-service"
    app.description = ""
    app.version = settings.VERSION

    register_exception_handlers(app)
    register_logging_middleware(app)
    register_cors_middleware(app)
    register_global_responses(app)
    register_offline_docs(app)

    print_modes()

    return app


app = create_app()
