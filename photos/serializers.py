from rest_framework import serializers
from photos.models import Photo
from PIL import Image
from PIL import UnidentifiedImageError


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Photo
        fields = ['id', 'establishment', 'image', 'alt_text', 'type_photo']
        read_only_fields = ['id', 'establishment']

    def validate_image(self, value):

        try:
            img = Image.open(value)
            img.verify()
            value.seek(0)
        except UnidentifiedImageError:
            raise serializers.ValidationError(
                "O arquivo enviado não é uma imagem válida.")
        except Exception:
            raise serializers.ValidationError("Erro ao processar a imagem.")

        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError(
                "O tamanho da imagem não pode exceder 5MB. Por favor, escolha um arquivo menor."
            )

        return value

    def validate_type_photo(self, value):
        allowed = ['profile', 'gallery', 'product']
        if value not in allowed:
            raise serializers.ValidationError(
                f"Tipo de foto inválido. Deve ser um dos: {allowed}")
        return value
