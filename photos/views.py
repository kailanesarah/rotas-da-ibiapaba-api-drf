from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from photos.models import Photo
from accounts.models import Establishment
from django.db import IntegrityError


class ProfilePhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            image = request.FILES.get('photo')
            alt_text = request.data.get('alt_text', '')
            type_photo = request.data.get('type_photo')

            if not image:
                return Response({'error': 'Nenhuma imagem enviada.'}, status=status.HTTP_400_BAD_REQUEST)

            if type_photo not in ['profile', 'gallery', 'product']:
                return Response({'error': 'Tipo de foto inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            establishment = Establishment.objects.get(user=request.user)

            if type_photo == 'profile':
                # Apaga a foto anterior de perfil
                Photo.objects.filter(
                    establishment=establishment, type_photo='profile').delete()

            photo = Photo.objects.create(
                establishment=establishment,
                image=image,
                alt_text=alt_text,
                type_photo=type_photo
            )

            return Response({
                'message': 'Foto de perfil enviada com sucesso.',
                'type': type_photo,
                'url_img': photo.image.url
            }, status=status.HTTP_201_CREATED)

        except IntegrityError:
            return Response({'error': 'Já existe uma foto de perfil para este estabelecimento.'}, status=status.HTTP_400_BAD_REQUEST)
        except Establishment.DoesNotExist:
            return Response({'error': 'Estabelecimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GalleryPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            images = request.FILES.getlist('photos')
            alt_text = request.data.get('alt_text', '')
            type_photo = request.data.get('type_photo')

            if not images:
                return Response({'error': 'Nenhuma imagem enviada.'}, status=status.HTTP_400_BAD_REQUEST)

            if type_photo not in ['profile', 'gallery', 'product']:
                return Response({'error': 'Tipo de foto inválido.'}, status=status.HTTP_400_BAD_REQUEST)

            establishment = Establishment.objects.get(user=request.user)

            photos_created = []
            url_photos = []

            for image in images:
                photo = Photo.objects.create(
                    establishment=establishment,
                    image=image,
                    alt_text=alt_text,
                    type_photo='gallery'
                )
                photos_created.append(photo.id)
                url_photos.append(photo.image.url)

            return Response({
                'message': f'{len(photos_created)} fotos enviadas com sucesso.',
                'type': 'gallery',
                'url_photos': url_photos,
                
            }, status=status.HTTP_201_CREATED)

        except Establishment.DoesNotExist:
            return Response({'error': 'Estabelecimento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Ocorreu um erro inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
