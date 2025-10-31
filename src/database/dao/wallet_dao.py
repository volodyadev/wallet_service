from typing import Optional
from sqlalchemy import select, update, insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database.models.wallet import wallets
from database.models.withdraw import operations, OperationType
from exceptions import WalletNotFoundError, InsufficientFundsError
from decimal import Decimal


class WalletDAO:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self.session_factory = session_factory

    async def get_balance(self, wallet_uuid: str) -> Optional[float]:
        async with self.session_factory() as session:
            stmt = select(wallets.c.balance).where(wallets.c.uuid == wallet_uuid)
            result = await session.execute(stmt)
            balance = result.scalar_one_or_none()
            if balance is None:
                raise WalletNotFoundError()
            return float(balance)

    async def process_operation(
        self,
        wallet_uuid: str,
        operation_type: OperationType,
        amount: float,
    ) -> float:
        amount_decimal = Decimal(str(amount))  

        async with self.session_factory() as session:
            async with session.begin():  
                stmt = (
                    select(wallets)
                    .where(wallets.c.uuid == wallet_uuid)
                    .with_for_update()
                )
                result = await session.execute(stmt)
                wallet_row = result.mappings().first()  

                if wallet_row is None:
                    raise WalletNotFoundError()

                current_balance: Decimal = wallet_row["balance"]

                new_balance = current_balance

                if operation_type == OperationType.DEPOSIT:
                    new_balance += amount_decimal
                elif operation_type == OperationType.WITHDRAW:
                    if current_balance < amount_decimal:
                        raise InsufficientFundsError()
                    new_balance -= amount_decimal

                await session.execute(
                    insert(operations).values(
                        wallet_uuid=wallet_uuid,
                        operation_type=operation_type,
                        amount=amount_decimal,
                    )
                )

                await session.execute(
                    update(wallets)
                    .where(wallets.c.uuid == wallet_uuid)
                    .values(balance=new_balance)
                )

        return float(new_balance) 

    async def create_wallet(self, wallet_uuid: str, initial_balance: float = 0) -> str:
        async with self.session_factory() as session:
            stmt = select(wallets.c.uuid).where(wallets.c.uuid == wallet_uuid)
            result = await session.execute(stmt)
            exists = result.scalar_one_or_none()
            if exists is not None:
                raise Exception(f"Wallet with UUID {wallet_uuid} already exists")

            await session.execute(
                insert(wallets).values(
                    uuid=wallet_uuid,
                    balance=initial_balance,
                )
            )
            await session.commit()
            return wallet_uuid
