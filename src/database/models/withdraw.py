from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Numeric,
    Enum,
    ForeignKey,
)
import enum

from database.models.wallet import wallets

from database.models.base import metadata


class OperationType(enum.Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


operations = Table(
    "operation",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("wallet_uuid", String, ForeignKey(wallets.c.uuid)),
    Column("operation_type", Enum(OperationType)),
    Column("amount", Numeric(18, 2)),
)
