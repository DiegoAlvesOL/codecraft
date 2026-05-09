from abc import ABC, abstractmethod
from backend.domain.code_request import CodeRequest


class CodeGenerator(ABC):
    """
    Abstract base class that defines the contract for all code generators.

    Any generator that inherits from this class must implement the
    generate method, which receives a CodeRequest and returns a
    base64-encoded PNG image string.
    """

    @abstractmethod
    def generate(self, request: CodeRequest) -> str:

        """
        Generates a visual code image from the given CodeRequest.

        :param request: A validated CodeRequest instance.
        :returns: A base64-encoded string representing the PNG image.
        :raises NotImplementedError: If the subclass does not implement this method.
        """

        pass