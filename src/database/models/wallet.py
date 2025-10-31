from sqlalchemy import (
    Table,
    Column,
    String,
    Numeric,
)

from ..models.base import metadata

wallets = Table(
    "wallet",
    metadata,
    Column("uuid", String, primary_key=True),
    Column("balance", Numeric(18, 2), default=0),
)
