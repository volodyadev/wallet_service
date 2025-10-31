from database.dao.wallet_dao import WalletDAO
import uuid


class CreateWalletUseCase:
    def __init__(self, dao: WalletDAO):
        self.dao = dao

    async def execute(self) -> str:
        wallet_uuid = str(uuid.uuid4())  # Генерация нового UUID v4
        await self.dao.create_wallet(wallet_uuid)
        return wallet_uuid
