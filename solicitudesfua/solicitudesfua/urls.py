from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="prueba.html"), name='inicio'),
    path('azure_auth/config/', admin.site.urls),
    path('logout/', TemplateView.as_view(template_name="home.html")),
    path("azure_auth/", include("azure_auth.urls")),
    path('azure_auth/', include('softwareids.urls')),  # Incluye las URLs de la app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
