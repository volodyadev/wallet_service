import fastapi_jsonrpc as jsonrpc


class BaseSystemException(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(message)


class ElementNotFoundError(BaseSystemException):
    def __init__(self):
        super().__init__("Element not found error")


class WalletNotFoundError(BaseSystemException):
    def __init__(self):
        super().__init__("Wallet not found")


class InsufficientFundsError(BaseSystemException):
    def __init__(self):
        super().__init__("Insufficient funds")


class ComponentIdError(BaseSystemException):
    def __init__(self):
        super().__init__("Invalid component id")
