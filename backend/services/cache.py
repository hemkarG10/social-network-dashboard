from typing import Dict, Any, Optional

class EvaluationCache:
    _instance = None
    _store: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EvaluationCache, cls).__new__(cls)
            cls._store = {}
        return cls._instance

    def get(self, key: str) -> Optional[Any]:
        return self._store.get(key)

    def set(self, key: str, value: Any):
        self._store[key] = value

    def clear(self):
        self._store = {}

cache = EvaluationCache()
