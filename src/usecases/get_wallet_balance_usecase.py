from database.dao.wallet_dao import WalletDAO
from exceptions import WalletNotFoundError


class GetWalletBalanceUseCase:
    def __init__(self, dao: WalletDAO):
        self.dao = dao

    async def execute(self, wallet_uuid: str) -> float:
        try:
            return await self.dao.get_balance(wallet_uuid)
        except WalletNotFoundError:
            raise
