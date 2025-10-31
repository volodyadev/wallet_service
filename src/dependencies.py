from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database.core import async_session_maker
from database.dao.wallet_dao import WalletDAO
from services.wallet_service import WalletService
from usecases.get_wallet_balance_usecase import GetWalletBalanceUseCase
from usecases.process_wallet_operation_usecase import ProcessWalletOperationUseCase
from usecases.create_waller_usecase import CreateWalletUseCase


async def get_session_factory() -> async_sessionmaker[AsyncSession]:
    yield async_session_maker


def get_wallet_dao(
    session_factory: async_sessionmaker[AsyncSession] = Depends(get_session_factory),
) -> WalletDAO:
    return WalletDAO(session_factory)


def get_wallet_service(
    dao: WalletDAO = Depends(get_wallet_dao),
) -> WalletService:
    return WalletService(dao)


def get_wallet_balance_usecase(
    service: WalletService = Depends(get_wallet_service),
) -> GetWalletBalanceUseCase:
    return GetWalletBalanceUseCase(service)


def get_process_wallet_operation_usecase(
    service: WalletService = Depends(get_wallet_service),
) -> ProcessWalletOperationUseCase:
    return ProcessWalletOperationUseCase(service)


def get_create_wallet_usecase(
    service: WalletService = Depends(get_wallet_service),
) -> CreateWalletUseCase:
    return CreateWalletUseCase(service)
