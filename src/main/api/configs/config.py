import os
from pathlib import Path
from typing import Any


class Config:
    _isinstance = None
    _dictionary = {}

    @staticmethod
    def _read_properties(path: Path) -> dict:
        """Читает файл вида key=value. Пустые строки и комментарии пропускает."""
        result = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                result[key.strip()] = value.strip()
        return result

    def __new__(cls):
        if cls._isinstance is None:
            cls._isinstance = super(Config, cls).__new__(cls)

            project_root = Path(__file__).parents[4]

            config_path = project_root / 'resources' / 'urls.properties'
            if not config_path.exists():
                raise FileNotFoundError(f"Config path not found: {config_path}")
            cls._dictionary.update(cls._read_properties(config_path))

            # Секреты: локально берутся из .env, в CI — из переменных окружения.
            # Файл .env не коммитится, поэтому его может не быть.
            env_path = project_root / '.env'
            if env_path.exists():
                cls._dictionary.update(cls._read_properties(env_path))

        return cls._isinstance

    @staticmethod
    def fetch(key: str, default_value: Any = None) -> Any:
        """Приоритет: переменная окружения → .env / urls.properties → значение по умолчанию."""
        if key in os.environ:
            return os.environ[key]
        return Config()._dictionary.get(key, default_value)
