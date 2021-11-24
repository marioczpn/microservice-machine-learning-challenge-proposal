from abc import abstractmethod

from loguru import logger

from api.common.invoker import BaseInvoker

from api.common.validation import BaseValidator, ValidationException


class FaceDetectionInvoker(BaseInvoker):
    """[FaceDetectionInvoker]
      This class allows to create abstract invoke's functionality that subclasses can implement or override.

    Args:
        ABC ([ABSTRACT BASE CLASS]): [This will be the class that will implement/override the method validate]

    Raises:
        ValidationException: [description]
    """

    @abstractmethod
    async def invoke(self, image_files):
        pass


class FaceDetectionNumberFilesValidation(BaseValidator):
    """[FaceDetectionNumberFilesValidation]
    This class is responsible for define the request validation, and it is implementing the abstract 
    defined into BaseValidator class method validate.

    Args:
        BaseValidator ([ABC]): [Its a custom abstract base classes and it makes the validate method as abstract]

    Raises:
        ValidationException: [description]
    """

    def validate(self, request):
        if not isinstance(request, list) or len(request) == 0:
            msg = "The request must provide a list of files containing at least one element"
            logger.error(msg)
            raise ValidationException(msg)
