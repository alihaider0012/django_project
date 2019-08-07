from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nucircle.urls')),
    path(r'chat/',include('chat.urls',namespace='chat')),
    path(r'forums/',include('forum.urls',namespace='forum')),
] 
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
