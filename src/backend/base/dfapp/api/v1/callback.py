from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import UUID

from loguru import logger

from dfapp.api.v1.schemas import ChatResponse, PromptResponse
from dfapp.services.deps import get_chat_service, get_socket_service
from dfapp.utils.util import remove_ansi_escape_codes

if TYPE_CHECKING:
    from dfapp.services.socket.service import SocketIOService
