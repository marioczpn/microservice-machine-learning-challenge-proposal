from abc import ABC, abstractmethod


class BaseInvoker(ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    async def invoke(self, payload):
        pass
