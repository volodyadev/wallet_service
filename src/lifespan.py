import logging
from contextlib import asynccontextmanager

import rasterio
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
