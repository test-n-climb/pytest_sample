from typing import Any, Optional

from pydantic import BaseModel, Json


class ResponseContent(BaseModel):
    success: bool
    errors: Optional[str] = None
    data: Optional[Json[dict[str, Any]]] = {}
