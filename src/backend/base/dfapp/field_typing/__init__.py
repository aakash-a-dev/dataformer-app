from typing import Any

from .constants import (
    # BaseLanguageModel,
    # BaseLLM,
    # BaseOutputParser,
    # BasePromptTemplate,
    # BaseRetriever,
    # Callable,
    # ChatPromptTemplate,
    # Code,
    Data,
    NestedDict,
    # Object,
    Prompt,
    # PromptTemplate,
    Text,
)
from .range_spec import RangeSpec


def _import_template_field():
    from dfapp.template.field.base import TemplateField

    return TemplateField


def __getattr__(name: str) -> Any:
    # This is to avoid circular imports
    if name == "TemplateField":
        return _import_template_field()
    elif name == "RangeSpec":
        return RangeSpec
    # The other names should work as if they were imported from constants
    # Import the constants module dfapp.field_typing.constants
    from . import constants

    return getattr(constants, name)


__all__ = [
    "NestedDict",
    "Data",
    # "Tool",
    # "PromptTemplate",
    # "Chain",
    # "BaseChatMemory",
    # "BaseLLM",
    # "BaseLanguageModel",
    # "BaseLoader",
    # "BaseMemory",
    # "BaseOutputParser",
    # "BaseRetriever",
    # "VectorStore",
    # "Embeddings",
    # "TextSplitter",
    # "Document",
    # "AgentExecutor",
    "Text",
    # "Object",
    # "Callable",
    # "BasePromptTemplate",
    # "ChatPromptTemplate",
    "Prompt",
    "RangeSpec",
    "TemplateField",
    # "Code",
]
