class RelatedFieldExtractorAdmin:
    """Extrai campos relacionados para exibição no Django Admin."""

    @staticmethod
    def get_field(obj, name_field: str) -> str:
        related_manager = getattr(obj, name_field, None)
        if related_manager and hasattr(related_manager, "all"):
            return ", ".join([str(item) for item in related_manager.all()])
        return ""
