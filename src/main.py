import uvicorn

from settings import settings

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        workers=settings.WORKERS_COUNT,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.APP_RELOAD,
    )
