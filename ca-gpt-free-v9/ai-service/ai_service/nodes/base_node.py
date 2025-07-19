from abc import ABC, abstractmethod
from typing import Any, Dict
from loguru import logger

class BaseNode(ABC):
    node_name: str = "BaseNode"

    @abstractmethod
    async def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Executing node: {self.node_name}")
        try:
            result = await self.process(payload)
            logger.success(f"Node execution successful: {self.node_name}")
            return result
        except Exception as e:
            logger.error(f"Error during node execution '{self.node_name}': {e}")
            raise
