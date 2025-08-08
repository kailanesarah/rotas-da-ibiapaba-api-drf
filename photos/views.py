from django.db import IntegrityError
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import Establishment
from photos.models import Photo
from photos.serializers import PhotoSerializer


class ProfilePhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            establishment = Establishment.objects.get(user=request.user)
            data = request.data.copy()

            serializer = PhotoSerializer(data=data)

            if serializer.is_valid():
                if data.get("type_photo") == "profile":
                    Photo.objects.filter(
                        establishment=establishment, type_photo="profile"
                    ).delete()

                photo = serializer.save(establishment=establishment)

                return Response(
                    {
                        "message": "Foto de perfil enviada com sucesso.",
                        "type": photo.type_photo,
                        "url_img": photo.image.url,
                    },
                    status=status.HTTP_201_CREATED,
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Establishment.DoesNotExist:
            return Response(
                {"error": "Estabelecimento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except IntegrityError:
            return Response(
                {"error": "Já existe uma foto de perfil para este estabelecimento."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro inesperado: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GalleryPhotoUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            establishment = Establishment.objects.get(user=request.user)
            data = request.data.copy()
            images = request.FILES.getlist("images")

            photos_created = []
            url_photos = []

            for image in images:
                data = {"image": image, "type_photo": data["type_photo"]}

                serializer = PhotoSerializer(data=data)

                if serializer.is_valid():
                    photo = serializer.save(establishment=establishment)
                    photos_created.append(photo.id)
                    url_photos.append(photo.image.url)
                else:
                    return Response(
                        {
                            "error": "Erro ao validar imagem.",
                            "details": serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {
                    "message": f"{len(photos_created)} fotos da galeria enviadas com sucesso.",
                    "type": "gallery",
                    "url_photos": url_photos,
                },
                status=status.HTTP_201_CREATED,
            )

        except Establishment.DoesNotExist:
            return Response(
                {"error": "Estabelecimento não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response(
                {"error": f"Ocorreu um erro inesperado: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
