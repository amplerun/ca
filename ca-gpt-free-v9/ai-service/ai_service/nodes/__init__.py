from .base_node import BaseNode
from .yaml_clean_node import YamlCleanNode
from .explain_node import ExplainNode
from .chat_node import ChatNode

nodes = {
    "clean_yaml": YamlCleanNode(),
    "explain": ExplainNode(),
    "chat": ChatNode(),
}

def get_node(node_name: str) -> BaseNode:
    node = nodes.get(node_name)
    if not node:
        raise ValueError(f"Node '{node_name}' not found.")
    return node
