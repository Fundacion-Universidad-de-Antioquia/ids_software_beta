from django.urls import path
from .views import index, test_view,home, guardar_fecha, novedad_view, enviar_a_sharepoint, cargar_formulario_novedad, obtener_fecha_ingreso, calcular_cantidad_horas, calcular_cantidad_dias
from .utils import obtener_personas_ajax, zonas_json_view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', index, name='index'),
    path('home/', home, name='home'),
    path('novedades/formulario/<str:tipo_novedad>/', cargar_formulario_novedad, name='cargar_formulario_novedad'),
    path('novedades/', novedad_view, name='novedad_form'),
    path('api/personas/', obtener_personas_ajax, name='api_personas'),
    path('api/sharepoint/', enviar_a_sharepoint, name='enviar_a_sharepoint'),
    path('api/zonas/', zonas_json_view, name='zonas_json'),
    path('api/fecha/', obtener_fecha_ingreso, name='obtener_fecha_ingreso'),
    path('calcular_cantidad_horas/', calcular_cantidad_horas, name='calcular_cantidad_horas'),
    path('calcular_cantidad_dias/', calcular_cantidad_dias, name='calcular_cantidad_dias'),
    path('guardar_fecha/', guardar_fecha, name='guardar_fecha'),
    path('test/', test_view, name='test_view'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
