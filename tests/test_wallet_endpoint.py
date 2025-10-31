from fastapi.testclient import TestClient
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Path, Body
from pydantic import BaseModel
from enum import Enum


class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: float

class BalanceResponse(BaseModel):
    balance: float

class OperationResponse(BaseModel):
    new_balance: float

class CreateWalletResponse(BaseModel):
    wallet_uuid: str


class GetWalletBalanceUseCase:
    async def execute(self, wallet_uuid: str):
        if wallet_uuid == "notfound":
            raise HTTPException(status_code=404, detail="Wallet not found")
        return 1000.0

class ProcessWalletOperationUseCase:
    async def execute(self, wallet_uuid: str, operation_type: str, amount: float):
        if wallet_uuid == "notfound":
            raise HTTPException(status_code=404, detail="Wallet not found")
        if amount > 1000:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        return 500.0

class CreateWalletUseCase:
    async def execute(self):
        return "generated-uuid-1234"


router = APIRouter(prefix="/api/v1/wallets")

@router.get("/{wallet_uuid}", response_model=BalanceResponse)
async def get_balance(
    wallet_uuid: str,
    usecase: GetWalletBalanceUseCase = Depends(GetWalletBalanceUseCase),
):
    balance = await usecase.execute(wallet_uuid)
    return BalanceResponse(balance=balance)

@router.post("/{wallet_uuid}/operation", response_model=OperationResponse)
async def process_wallet_operation(
    wallet_uuid: str,
    operation: OperationRequest,
    usecase: ProcessWalletOperationUseCase = Depends(ProcessWalletOperationUseCase),
):
    new_balance = await usecase.execute(wallet_uuid, operation.operation_type.value, operation.amount)
    return OperationResponse(new_balance=new_balance)

@router.post("/", response_model=CreateWalletResponse)
async def create_wallet(
    usecase: CreateWalletUseCase = Depends(CreateWalletUseCase),
):
    wallet_uuid = await usecase.execute()
    return CreateWalletResponse(wallet_uuid=wallet_uuid)


app = FastAPI()
app.include_router(router)

client = TestClient(app)

# tests

def test_get_balance_success():
    response = client.get("/api/v1/wallets/existing-wallet")
    assert response.status_code == 200
    assert response.json() == {"balance": 1000.0}

def test_get_balance_not_found():
    response = client.get("/api/v1/wallets/notfound")
    assert response.status_code == 404

def test_process_operation_success():
    response = client.post("/api/v1/wallets/existing-wallet/operation", json={
        "operation_type": "DEPOSIT",
        "amount": 100,
    })
    assert response.status_code == 200
    assert response.json() == {"new_balance": 500.0}

def test_process_operation_insufficient_funds():
    response = client.post("/api/v1/wallets/existing-wallet/operation", json={
        "operation_type": "WITHDRAW",
        "amount": 5000,
    })
    assert response.status_code == 400

def test_create_wallet():
    response = client.post("/api/v1/wallets/")
    assert response.status_code == 200
    assert "wallet_uuid" in response.json()
