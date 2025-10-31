from pydantic import BaseModel, condecimal, constr
from database.models.withdraw import OperationType


class OperationRequest(BaseModel):
    operation_type: OperationType
    amount: condecimal(gt=0)


class BalanceResponse(BaseModel):
    balance: float


class OperationResponse(BaseModel):
    new_balance: float


class CreateWalletResponse(BaseModel):
    wallet_uuid: str
