from typing import Any, Optional

from pydantic import BaseModel, Json


class ResponseContent(BaseModel):
    success: bool
    errors: Optional[list[dict[str, Any]]] = None
    data: Optional[Json[dict[str, Any]]] = None
