from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from photos.views import ProfilePhotoUploadView, GalleryPhotoUploadView

urlpatterns = [
    path('profile-photo/upload/', ProfilePhotoUploadView.as_view(), name='upload_profile'),
    path('galery-photo/upload/', GalleryPhotoUploadView.as_view(), name='upload_galery'),
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)