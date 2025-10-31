from fastapi import APIRouter, Depends, HTTPException, Path, Body
from exceptions import WalletNotFoundError, InsufficientFundsError
from usecases.get_wallet_balance_usecase import GetWalletBalanceUseCase
from usecases.process_wallet_operation_usecase import ProcessWalletOperationUseCase
from usecases.create_waller_usecase import CreateWalletUseCase
from schema import (
    OperationRequest,
    BalanceResponse,
    OperationResponse,
    CreateWalletResponse,
)
from dependencies import (
    get_wallet_balance_usecase,
    get_process_wallet_operation_usecase,
    get_create_wallet_usecase,
)


router = APIRouter()


@router.get(
    "/{wallet_uuid}",
    response_model=BalanceResponse,
    summary="Получить баланс кошелька",
)
async def get_balance(
    wallet_uuid: str = Path(..., description="UUID кошелька"),
    usecase: GetWalletBalanceUseCase = Depends(get_wallet_balance_usecase),
):
    try:
        balance = await usecase.execute(wallet_uuid)
        return BalanceResponse(balance=balance)
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail="Wallet not found")


@router.post(
    "/{wallet_uuid}/operation",
    response_model=OperationResponse,
    summary="Выполнить операцию с кошельком",
)
async def process_wallet_operation(
    wallet_uuid: str = Path(..., description="UUID кошелька"),
    operation: OperationRequest = Body(...),
    usecase: ProcessWalletOperationUseCase = Depends(
        get_process_wallet_operation_usecase
    ),
):
    try:
        new_balance = await usecase.execute(
            wallet_uuid,
            operation.operation_type.value,
            float(operation.amount),
        )
        return OperationResponse(new_balance=new_balance)
    except WalletNotFoundError:
        raise HTTPException(status_code=404, detail="Wallet not found")
    except InsufficientFundsError:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/",
    response_model=CreateWalletResponse,
    summary="Создать новый кошелек",
)
async def create_wallet(
    usecase: CreateWalletUseCase = Depends(get_create_wallet_usecase),
):
    try:
        wallet_uuid = await usecase.execute()
        return CreateWalletResponse(wallet_uuid=wallet_uuid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
