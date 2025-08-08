class PhotoUtils:
    @staticmethod
    def get_photo_url_by_type(photos_queryset, type_photo):
        photo = photos_queryset.filter(type_photo=type_photo).first()
        return photo.image.url if photo and photo.image else None

    @staticmethod
    def get_multiple_photo_urls_by_types(photos_queryset, types):
        photos = photos_queryset.filter(type_photo__in=types)
        return [photo.image.url for photo in photos if photo.image]
    
    def get_product_photos(self, obj):
        photos = obj.photos.filter(type_photo='product')
        return [photo.image.url for photo in photos if photo.image]
