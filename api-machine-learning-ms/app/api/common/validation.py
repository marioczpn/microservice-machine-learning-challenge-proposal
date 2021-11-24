from abc import ABC, abstractmethod
from loguru import logger


class BaseValidator(ABC):
    """
    [BaseValidator]
    
    This class allows to create abstract validate functionality that subclasses can implement or override.

    Args:
        ABC ([ABSTRACT BASE CLASS]): [This will be the class that will implement/override the method validate]
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def validate(self, request):
        pass


class RequestValidator:
    """
    [RequestValidator]

    This class is responsable to handle the validate method that will be implemented by the concrete class.
    """""
    def __init__(self, validators):
        self.validators = validators

    def validate(self, request):
        logger.info(f"Validating request with {request.__class__.__name__}")
        for validator in self.validators:
            validator.validate(request)


class ValidationException(Exception):
    """Raised when a validation exception happens"""""
    def __init__(self, message):
        self.message = message
