class ExceptionBase(Exception):
    """Base class for all custom exceptions."""
    pass

class AccountNotFoundException(ExceptionBase):
    """Raised when an account is not found."""
    pass

class InsufficientFundsException(ExceptionBase):
    """Raised when an account has insufficient funds for a withdrawal or transfer."""
    pass

class InvalidAccountStatusException(ExceptionBase):
    """Raised when an operation is attempted on an account with an invalid status."""
    pass

class NoFieldsToUpdateException(ExceptionBase):
    """Raised when an update operation is attempted with no fields to update."""
    pass
