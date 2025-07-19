from abc import ABC, abstractmethod
from typing import Any, Dict

from loguru import logger

class BaseNode(ABC):
    """
    Abstract base class for a node in a processing pipeline (PocketFlow).
    Each node takes a payload and returns a modified payload.
    """
    node_name: str = "BaseNode"

    @abstractmethod
    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        The main processing method for the node.
        Must be implemented by subclasses.
        """
        pass

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Wrapper to execute the node's logic with logging.
        """
        logger.info(f"Executing node: {self.node_name}")
        try:
            result = await self.process(payload)
            logger.success(f"Node execution successful: {self.node_name}")
            return result
        except Exception as e:
            logger.error(f"Error during node execution '{self.node_name}': {e}")
            # Re-raise the exception to be handled by the main endpoint
            raise