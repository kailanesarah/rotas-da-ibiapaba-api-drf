import uuid


class IDGenerator:
    """Gera identificadores únicos para objetos com prefixo."""

    @staticmethod
    def generate(prefix: str, length: int = 6) -> str:
        """
        Gera um ID curto combinando um prefixo e UUID.
        Ex: U-1a2b3c, E-4d5e6f
        """
        return f"{prefix}-{uuid.uuid4().hex[:length]}"
