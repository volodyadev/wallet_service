from database.dao.wallet_dao import WalletDAO
from database.models.withdraw import OperationType
from exceptions import WalletNotFoundError, InsufficientFundsError


class ProcessWalletOperationUseCase:
    def __init__(self, dao: WalletDAO):
        self.dao = dao

    async def execute(
        self, wallet_uuid: str, operation_type: str, amount: float
    ) -> float:
        try:
            op_type = OperationType(operation_type)
        except ValueError:
            raise ValueError("Invalid operation_type. Allowed: DEPOSIT, WITHDRAW")

        try:
            return await self.dao.process_operation(wallet_uuid, op_type, amount)
        except (WalletNotFoundError, InsufficientFundsError):
            raise
