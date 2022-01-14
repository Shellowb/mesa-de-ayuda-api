from abc import ABC, abstractmethod

class Handler(ABC):
    """Handles an action to be perform
    when a especifici type is recognized in
    parse
    """

    @abstractmethod
    def handle(expression: str, for_id: int) -> None:
        """Handles a expression

        Args:
            expresion (str): a expression to be handled
        """
        pass

