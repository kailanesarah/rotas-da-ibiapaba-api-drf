class RelatedFieldExtractorAdmin:
    def get_field(self, obj, name_field):
        related_manager = getattr(obj, name_field)
        if hasattr(related_manager, 'all'):
            return ", ".join([str(item) for item in related_manager.all()])