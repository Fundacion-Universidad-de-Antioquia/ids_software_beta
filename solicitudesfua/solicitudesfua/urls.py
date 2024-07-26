from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from softwareids.views import index, home, novedad_view, enviar_a_sharepoint, cargar_formulario_novedad, obtener_fecha_ingreso
from softwareids.utils import obtener_personas_ajax, zonas_json_view



urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('azure_auth/config/', admin.site.urls),
    path('', TemplateView.as_view(template_name="home.html")),
    path('logout/', TemplateView.as_view(template_name="home.html")),
    path("azure_auth/", include("azure_auth.urls"),),
    path('azure_auth/home/', home, name="home"),
    path('azure_auth/novedades/formulario/<str:tipo_novedad>/', cargar_formulario_novedad, name='cargar_formulario_novedad'),
    path('azure_auth/novedades/', novedad_view, name='novedad_form'),
    path('api/personas/', obtener_personas_ajax, name='api_personas'),
    path('api/sharepoint/', enviar_a_sharepoint, name='enviar_a_sharepoint'),
    path('api/zonas/', zonas_json_view, name='zonas_json'),
    path('api/fecha/', obtener_fecha_ingreso, name='obtener_fecha_ingreso'),

    # model departmend views
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
