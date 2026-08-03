from src.main.api.models.base_model import BaseModel


class ErrorResponse(BaseModel):
    error: str
