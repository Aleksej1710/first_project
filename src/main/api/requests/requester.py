from abc import ABC, abstractmethod
from typing import Dict, Callable
from src.main.api.configs.config import Config
from src.main.api.models.base_model import BaseModel


class Requester(ABC):
    def __init__(self, request_spec: Dict[str, str], response_spec: Callable):
        self.headers = request_spec
        self.base_url = Config.fetch("backendUrl")
        self.response_spec = response_spec

    @abstractmethod
    def post(self, model: BaseModel): ...