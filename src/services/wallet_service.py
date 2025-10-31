from database.dao.wallet_dao import WalletDAO
from database.models.withdraw import OperationType
from exceptions import WalletNotFoundError, InsufficientFundsError


class WalletService:
    def __init__(self, dao: WalletDAO):
        self.dao = dao

    async def get_balance(self, wallet_uuid: str) -> float:
        return await self.dao.get_balance(wallet_uuid)

    async def process_operation(
        self,
        wallet_uuid: str,
        operation_type: OperationType,
        amount: float,
    ) -> float:
        try:
            return await self.dao.process_operation(wallet_uuid, operation_type, amount)
        except (WalletNotFoundError, InsufficientFundsError):
            raise

    async def create_wallet(self, wallet_uuid: str, initial_balance: float = 0) -> str:
        return await self.dao.create_wallet(wallet_uuid, initial_balance)
