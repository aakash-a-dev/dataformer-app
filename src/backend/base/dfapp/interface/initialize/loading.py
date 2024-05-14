import inspect
import json
from typing import TYPE_CHECKING, Any, Callable, Dict, Sequence, Type


import orjson
from loguru import logger
from pydantic import ValidationError

from dfapp.interface.custom.eval import eval_custom_component_code
from dfapp.interface.importing.utils import import_by_type
from dfapp.interface.initialize.llm import initialize_vertexai
# from dfapp.interface.initialize.utils import handle_format_kwargs, handle_node_type, handle_partial_variables
# from dfapp.interface.initialize.vector_store import vecstore_initializer
# from dfapp.interface.output_parsers.base import output_parser_creator
# from dfapp.interface.utils import load_file_into_dict
# from dfapp.interface.wrappers.base import wrapper_creator
from dfapp.schema.schema import Record
# from dfapp.utils import validate
# from dfapp.utils.util import unescape_string

if TYPE_CHECKING:
    from dfapp.custom import CustomComponent
    from dfapp.graph.vertex.base import Vertex


async def instantiate_class(
    vertex: "Vertex",
    user_id=None,
) -> Any:
    """Instantiate class from module type and key, and params"""
    from dfapp.interface.custom_lists import CUSTOM_NODES

    vertex_type = vertex.vertex_type
    base_type = vertex.base_type
    params = vertex.params
    params = convert_params_to_sets(params)
    params = convert_kwargs(params)

    if vertex_type in CUSTOM_NODES:
        if custom_node := CUSTOM_NODES.get(vertex_type):
            if hasattr(custom_node, "initialize"):
                return custom_node.initialize(**params)
            if callable(custom_node):
                return custom_node(**params)
            raise ValueError(f"Custom node {vertex_type} is not callable")
    logger.debug(f"Instantiating {vertex_type} of type {base_type}")
    if not base_type:
        raise ValueError("No base type provided for vertex")
    if base_type == "custom_components":
        return await instantiate_custom_component(params, user_id, vertex)
    class_object = import_by_type(_type=base_type, name=vertex_type)
    return await instantiate_based_on_type(
        class_object=class_object,
        base_type=base_type,
        node_type=vertex_type,
        params=params,
        user_id=user_id,
        vertex=vertex,
    )


def convert_params_to_sets(params):
    """Convert certain params to sets"""
    if "allowed_special" in params:
        params["allowed_special"] = set(params["allowed_special"])
    if "disallowed_special" in params:
        params["disallowed_special"] = set(params["disallowed_special"])
    return params


def convert_kwargs(params):
    # if *kwargs are passed as a string, convert to dict
    # first find any key that has kwargs or config in it
    kwargs_keys = [key for key in params.keys() if "kwargs" in key or "config" in key]
    for key in kwargs_keys:
        if isinstance(params[key], str):
            try:
                params[key] = orjson.loads(params[key])
            except json.JSONDecodeError:
                # if the string is not a valid json string, we will
                # remove the key from the params
                params.pop(key, None)
    return params


async def instantiate_based_on_type(
    class_object,
    base_type,
    node_type,
    params,
    user_id,
    vertex,
):
    # if base_type == "agents":
    #     return instantiate_agent(node_type, class_object, params)
    if base_type == "prompts":
        return instantiate_prompt(node_type, class_object, params)
    # elif base_type == "tools":
    #     tool = instantiate_tool(node_type, class_object, params)
    #     if hasattr(tool, "name") and isinstance(tool, BaseTool):
    #         # tool name shouldn't contain spaces
    #         tool.name = tool.name.replace(" ", "_")
    #     return tool
    # elif base_type == "toolkits":
    #     return instantiate_toolkit(node_type, class_object, params)
    # elif base_type == "embeddings":
    #     return instantiate_embedding(node_type, class_object, params)
    # elif base_type == "vectorstores":
    #     return instantiate_vectorstore(class_object, params)
    # elif base_type == "documentloaders":
    #     return instantiate_documentloader(node_type, class_object, params)
    # elif base_type == "textsplitters":
    #     return instantiate_textsplitter(class_object, params)
    # elif base_type == "utilities":
    #     return instantiate_utility(node_type, class_object, params)
    # elif base_type == "chains":
    #     return instantiate_chains(node_type, class_object, params)
    # elif base_type == "output_parsers":
    #     return instantiate_output_parser(node_type, class_object, params)
    elif base_type == "models":
        return instantiate_llm(node_type, class_object, params)
    # elif base_type == "retrievers":
    #     return instantiate_retriever(node_type, class_object, params)
    elif base_type == "memory":
        return instantiate_memory(node_type, class_object, params)
    elif base_type == "custom_components":
        return await instantiate_custom_component(
            params,
            user_id,
            vertex,
        )
    # elif base_type == "wrappers":
    #     return instantiate_wrapper(node_type, class_object, params)
    else:
        return class_object(**params)


def update_params_with_load_from_db_fields(custom_component: "CustomComponent", params, load_from_db_fields):
    # For each field in load_from_db_fields, we will check if it's in the params
    # and if it is, we will get the value from the custom_component.keys(name)
    # and update the params with the value
    for field in load_from_db_fields:
        if field in params:
            try:
                key = custom_component.variables(params[field])
                params[field] = key if key else params[field]
            except Exception as exc:
                logger.error(f"Failed to get value for {field} from custom component. Error: {exc}")
                pass
    return params


async def instantiate_custom_component(params, user_id, vertex):
    params_copy = params.copy()
    class_object: Type["CustomComponent"] = eval_custom_component_code(params_copy.pop("code"))
    custom_component: "CustomComponent" = class_object(
        user_id=user_id,
        parameters=params_copy,
        vertex=vertex,
        selected_output_type=vertex.selected_output_type,
    )
    params_copy = update_params_with_load_from_db_fields(custom_component, params_copy, vertex.load_from_db_fields)

    if "retriever" in params_copy and hasattr(params_copy["retriever"], "as_retriever"):
        params_copy["retriever"] = params_copy["retriever"].as_retriever()

    # Determine if the build method is asynchronous
    is_async = inspect.iscoroutinefunction(custom_component.build)

    if is_async:
        # Await the build method directly if it's async
        build_result = await custom_component.build(**params_copy)
    else:
        # Call the build method directly if it's sync
        build_result = custom_component.build(**params_copy)
    custom_repr = custom_component.custom_repr()
    if custom_repr is None and isinstance(build_result, (dict, Record, str)):
        custom_repr = build_result
    if not isinstance(custom_repr, str):
        custom_repr = str(custom_repr)
    return custom_component, build_result, {"repr": custom_repr}


# def instantiate_wrapper(node_type, class_object, params):
#     if node_type in wrapper_creator.from_method_nodes:
#         method = wrapper_creator.from_method_nodes[node_type]
#         if class_method := getattr(class_object, method, None):
#             return class_method(**params)
#         raise ValueError(f"Method {method} not found in {class_object}")
#     return class_object(**params)


# def instantiate_output_parser(node_type, class_object, params):
#     if node_type in output_parser_creator.from_method_nodes:
#         method = output_parser_creator.from_method_nodes[node_type]
#         if class_method := getattr(class_object, method, None):
#             return class_method(**params)
#         raise ValueError(f"Method {method} not found in {class_object}")
#     return class_object(**params)


def instantiate_llm(node_type, class_object, params: Dict):
    # This is a workaround so JinaChat works until streaming is implemented
    # if "openai_api_base" in params and "jina" in params["openai_api_base"]:
    # False if condition is True
    if "VertexAI" in node_type:
        return initialize_vertexai(class_object=class_object, params=params)
    # max_tokens sometimes is a string and should be an int
    if "max_tokens" in params:
        if isinstance(params["max_tokens"], str) and params["max_tokens"].isdigit():
            params["max_tokens"] = int(params["max_tokens"])
        elif not isinstance(params.get("max_tokens"), int):
            params.pop("max_tokens", None)
    return class_object(**params)


def instantiate_memory(node_type, class_object, params):
    # process input_key and output_key to remove them if
    # they are empty strings
    if node_type == "ConversationEntityMemory":
        params.pop("memory_key", None)

    for key in ["input_key", "output_key"]:
        if key in params and (params[key] == "" or not params[key]):
            params.pop(key)

    try:
        if "retriever" in params and hasattr(params["retriever"], "as_retriever"):
            params["retriever"] = params["retriever"].as_retriever()
        return class_object(**params)
    # I want to catch a specific attribute error that happens
    # when the object does not have a cursor attribute
    except Exception as exc:
        if "object has no attribute 'cursor'" in str(exc) or 'object has no field "conn"' in str(exc):
            raise AttributeError(
                (
                    "Failed to build connection to database."
                    f" Please check your connection string and try again. Error: {exc}"
                )
            ) from exc
        raise exc


# def instantiate_prompt(node_type, class_object, params: Dict):
#     params, prompt = handle_node_type(node_type, class_object, params)
#     format_kwargs = handle_format_kwargs(prompt, params)
#     # Now we'll use partial_format to format the prompt
#     if format_kwargs:
#         prompt = handle_partial_variables(prompt, format_kwargs)
#     return prompt, format_kwargs


def replace_zero_shot_prompt_with_prompt_template(nodes):
    """Replace ZeroShotPrompt with PromptTemplate"""
    for node in nodes:
        if node["data"]["type"] == "ZeroShotPrompt":
            # Build Prompt Template
            tools = [
                tool
                for tool in nodes
                if tool["type"] != "chatOutputNode" and "Tool" in tool["data"]["node"]["base_classes"]
            ]
            node["data"] = build_prompt_template(prompt=node["data"], tools=tools)
            break
    return nodes

def build_prompt_template(prompt, tools):
    """Build PromptTemplate from ZeroShotPrompt"""
    prefix = prompt["node"]["template"]["prefix"]["value"]
    suffix = prompt["node"]["template"]["suffix"]["value"]
    format_instructions = prompt["node"]["template"]["format_instructions"]["value"]

    tool_strings = "\n".join(
        [f"{tool['data']['node']['name']}: {tool['data']['node']['description']}" for tool in tools]
    )
    tool_names = ", ".join([tool["data"]["node"]["name"] for tool in tools])
    format_instructions = format_instructions.format(tool_names=tool_names)
    value = "\n\n".join([prefix, tool_strings, format_instructions, suffix])

    prompt["type"] = "PromptTemplate"

    prompt["node"] = {
        "template": {
            "_type": "prompt",
            "input_variables": {
                "type": "str",
                "required": True,
                "placeholder": "",
                "list": True,
                "show": False,
                "multiline": False,
            },
            "output_parser": {
                "type": "BaseOutputParser",
                "required": False,
                "placeholder": "",
                "list": False,
                "show": False,
                "multline": False,
                "value": None,
            },
            "template": {
                "type": "str",
                "required": True,
                "placeholder": "",
                "list": False,
                "show": True,
                "multiline": True,
                "value": value,
            },
            "template_format": {
                "type": "str",
                "required": False,
                "placeholder": "",
                "list": False,
                "show": False,
                "multline": False,
                "value": "f-string",
            },
            "validate_template": {
                "type": "bool",
                "required": False,
                "placeholder": "",
                "list": False,
                "show": False,
                "multline": False,
                "value": True,
            },
        },
        "description": "Schema to represent a prompt for an LLM.",
        "base_classes": ["BasePromptTemplate"],
    }

    return prompt
