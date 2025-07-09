from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from photos.models import Photo, upload_to_path
from accounts.models import Establishment


class ProfilePhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            image = request.FILES.get('photo')

            alt_text = request.data.get('alt_text', '')
            is_profile = request.data.get('is_profile') == 'true'
            is_gallery = request.data.get('is_gallery') == 'true'
            is_product = request.data.get('is_product') == 'true'

            if not image:
                return Response({'error': 'Nenhuma imagem enviada.'}, status=status.HTTP_400_BAD_REQUEST)

            # checa quantos itens foram marcados ao mesmo tempo
            flags = [is_profile, is_gallery, is_product]
            if flags.count(True) > 1:
                return Response({'error': 'Apenas um tipo de foto pode ser marcado por vez.'}, status=status.HTTP_400_BAD_REQUEST)
            if flags.count(True) == 0:
                return Response({'error': 'Você deve informar um tipo de foto.'}, status=status.HTTP_400_BAD_REQUEST)

            establishment = Establishment.objects.get(user=request.user)

            if is_profile:
                Photo.objects.filter(establishment=establishment, is_profile_pic=True).update(
                    is_profile_pic=False)

            photo = Photo.objects.create(
                establishment=establishment,
                image=image,
                alt_text=alt_text,
                is_profile_pic=is_profile,
                is_gallery_pic=is_gallery,
                is_product_pic=is_product
            )

            tipo = 'perfil' if is_profile else 'galeria' if is_gallery else 'produto'
            url = photo.image.url

            return Response({
                'message': 'Foto enviada com sucesso.',
                'photo_id': photo.id,
                'type': tipo,
                'url_img': url
            }, status=status.HTTP_201_CREATED)

        except Establishment.DoesNotExist:
            return Response({'error': 'Estabelecimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GalleryPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            # getlist para múltiplos arquivos
            images = request.FILES.getlist('photos')
            alt_text = request.data.get('alt_text', '')

            if not images:
                return Response({'error': 'Nenhuma imagem enviada.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                establishment = Establishment.objects.get(user=request.user)
            except Establishment.DoesNotExist:
                return Response({'error': 'Estabelecimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

            photos_created = []
            url_photos = []

            for image in images:
                photo = Photo.objects.create(
                    establishment=establishment,
                    image=image,
                    alt_text=alt_text,
                    is_gallery_pic=True,
                    is_profile_pic=False,
                    is_product_pic=False
                )
                photos_created.append(photo.id)
                url_photos.append(photo.image.url)

            return Response({
                'message': f'{len(photos_created)} fotos enviadas com sucesso.',
                'photo_ids': photos_created,
                'url_photos': url_photos,
                'type': 'galeria'

            }, status=status.HTTP_201_CREATED)
        except Establishment.DoesNotExist:
            return Response({'error': 'Estabelecimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
