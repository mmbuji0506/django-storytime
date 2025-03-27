from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from stories.views import story_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stories/', include('stories.urls')),
    path('', story_list, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)