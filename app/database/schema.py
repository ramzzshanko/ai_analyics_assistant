from pydantic import BaseModel

class LLMResponse(BaseModel):
    model: str
    prompt: str
    response: str
    created_at: str  # ISO format date string
    updated_at: str  # ISO format date string
    status: str  # e.g., "success", "error"
    error_message: str = None  # Optional field for error messages
    metadata: dict = {}  # Optional field for additional metadata