from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from .forms import CampoForm, NovedadFormTipo1, NovedadFormTipo2, NovedadFormTipo3, NovedadFormTipo4, NovedadFormTipo10,NovedadFormTipo11, NovedadFormTipo12, NovedadFormTipo13, NovedadFormTipo14,NovedadFormTipo15, NovedadFormTipo16, NovedadFormTipo18, NovedadFormTipo17, NovedadFormTipo19, NovedadFormTipo20, NovedadFormTipo21, NovedadFormTipo22, NovedadFormTipo23,  NovedadFormTipo5, NovedadFormTipo6, NovedadFormTipo7, NovedadFormTipo8, NovedadFormTipo9
from .utils import  obtener_access_token, sincronizar_con_sharepoint, fetch_personas_from_odoo_usuarios, fetch_zonas_from_odoo, fetch_personas_from_odoo
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import NovedadBase
from django.http import Http404, JsonResponse
from django.utils.safestring import mark_safe
import requests
from datetime import datetime, timedelta
from django.http import HttpResponse


logger = logging.getLogger(__name__)

#
def index(request):
    correo = request.user.email  # Correo obtenido del login de Microsoft
    request.session['correo'] = correo
    logger.warning('CORREO INDEX', correo) 
    context = {
            'APP': os.getenv('APP', 'No definido'),
            # Agrega más variables según sea necesario
        }
    return render(request, 'home.html', context)

@login_required
def home(request):
    correo = request.session.get('correo')
    personas = fetch_personas_from_odoo_usuarios(correo)
    zonas = fetch_zonas_from_odoo()
    # Guardar el correo en la sesión
    
    if not correo:
            # Maneja el caso en que no hay correo en la sesión
        logger.warning("El correo no está presente en la sesión")
    
    # Limpiar la justificación almacenada en la sesión al ingresar a home
    if 'justificacion' in request.session:
        del request.session['justificacion']
   
    if 'fecha' in request.session:
            del request.session['fecha']

    if request.method == 'POST':
        campo_form = CampoForm(request.POST)        
        
        if campo_form.is_valid():
            campo = campo_form.save(commit=False)
            campo.save()
            # Guardar la fecha en la sesión
            return redirect('/azure_auth/novedades/')  
        else:
            logger.error("Formulario no válido en la vista home")# Define una URL de éxito
    else:
        campo_form = CampoForm()

    return render(request, 'menuppal.html', { 'campo_form': campo_form, 'personas': personas, 'zonas': zonas, 'correo': correo })

@login_required
def novedad_view(request):
    
    correo = request.session.get('correo')  # Obtener el correo de la sesión 
    tipos_novedad = NovedadBase._meta.get_field('tipo_novedad').choices
    return render(request, 'form.html', {'tipos_novedad': tipos_novedad,'correo': correo})

@login_required
def cargar_formulario_novedad(request, tipo_novedad):
    
    # Obtener la fecha y justificación de la sesión
    fecha = request.session.get('fecha', None)
    justificacion = request.session.get('justificacion', None)
    correo = request.session.get('correo')  # Obtener el correo de la sesión 
    form_classes = {
        'opcion1': NovedadFormTipo1,
        'opcion2': NovedadFormTipo2,
        'opcion3': NovedadFormTipo3,
        'opcion4': NovedadFormTipo4,
        'opcion5': NovedadFormTipo5,
        'opcion6': NovedadFormTipo6,
        'opcion7': NovedadFormTipo7,
        'opcion8': NovedadFormTipo8,
        'opcion9': NovedadFormTipo9,
        'opcion10': NovedadFormTipo10,
        'opcion11': NovedadFormTipo11,
        'opcion12': NovedadFormTipo12,
        'opcion13': NovedadFormTipo13,
        'opcion14': NovedadFormTipo14,
        'opcion15': NovedadFormTipo15,
        'opcion16': NovedadFormTipo16,
        'opcion17': NovedadFormTipo17,
        'opcion18': NovedadFormTipo18,
        'opcion19': NovedadFormTipo19,
        'opcion20': NovedadFormTipo20,
        'opcion21': NovedadFormTipo21,
        'opcion22': NovedadFormTipo22,
        'opcion23': NovedadFormTipo23,
    }
    FormClass = form_classes.get(tipo_novedad)

    if not FormClass:
        raise Http404("Tipo de novedad no válido")

    departamento = request.GET.get('departamento')

    if request.method == 'POST':
        form = FormClass(request.POST, departamento=departamento,initial={'fecha': fecha})
        if form.is_valid():
            if tipo_novedad == 'opcion8':
                personas = fetch_personas_from_odoo()
                cedula = form.cleaned_data['cedula']
                fecha_ingreso = ''
                for persona in personas:
                    if persona[0] == cedula:
                        fecha_ingreso = persona[3]
                        break

                novedad = form.save(commit=False)
                novedad.fecha_ingreso = fecha_ingreso
                novedad.cantidad_horas = novedad.cantidad_horas 
                # Calcular y asignar cantidad_horas
                novedad.justificacion = justificacion  # Agregar la justificación
                novedad.correo = correo  # Agregar la justificación
            
                novedad.save()
            else:
                form.save()

            return redirect('url_de_exito')

    else:
        form = FormClass(departamento=departamento, initial={'fecha': fecha, 'justificacion': justificacion})
        personas_data = fetch_personas_from_odoo(departamento)
        personas_data_dict = {
            persona[0]: {
                'nombre': persona[1],
                'fecha_ingreso': persona[3]
            } for persona in personas_data
        }

    return render(request, 'formulario_novedad.html', {
        'form': form,
        'tipo_novedad': tipo_novedad,
        'personas_data_json': mark_safe(json.dumps(personas_data_dict)),
        'departamento': departamento,  # Asegurando que el departamento se pasa al template
        'fecha': fecha , # Pasar la fecha al contexto
        'justificacion': justificacion, # Pasar la justificación al contexto
        'correo': correo,
    
    })
@csrf_exempt
def enviar_a_sharepoint(request):# Obtener el correo de la sesión 
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            access_token = obtener_access_token()
            if access_token:
                correo = request.user.email if request.user.is_authenticated else "anonimo@example.com"
                
                # Extraer la fecha del primer registro
                if data and isinstance(data, list) and 'fields' in data[0] and 'Fecha' in data[0]['fields']:
                    fecha_registro = data[0]['fields']['Fecha']
                else:
                    logging.error("No se encontró la fecha en los datos enviados")
                    return JsonResponse({'error': 'No se encontró la fecha en los datos enviados'}, status=400)
                
                log_status, general_observacion = sincronizar_con_sharepoint(data, access_token)

                # Registrar el log general
                log_data = {
                    'correo': correo,
                    'tipo_evento': log_status,
                    'fecha': fecha_registro,  # Usa la fecha proporcionada en el data
                    'observacion': general_observacion,
                    'nombre_aplicacion': 'IDS-ASEO',
                    'tipo': 'Registro',
                }

                try:
                    logging_response = requests.post('https://app-conexionerp-prod-001.azurewebsites.net/logs/registrar/', json=log_data)
                    logging_response.raise_for_status()
                except requests.RequestException as e:
                    logging.error(f'Error al registrar el log: {e}')
                
                if log_status == 'SUCCESS':
                    return JsonResponse({'status': 'success'}, status=200)
                else:
                    return JsonResponse({'status': 'partial_success', 'details': general_observacion}, status=207)
            else:
                return JsonResponse({'error': 'Error al obtener el token de acceso'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)






@csrf_exempt
def obtener_fecha_ingreso(request):
    persona_id = request.GET.get('persona_id')
    logger.debug(f'Persona ID recibida: {persona_id}')
    if persona_id:
        personas = fetch_personas_from_odoo()
        for persona in personas:
            if persona[0] == persona_id:
                logger.debug(f'Fecha de ingreso encontrada: {persona[3]}')
                return JsonResponse({'fecha_ingreso': persona[3]})  # La fecha de ingreso es el cuarto elemento de la tupla
    logger.debug('Persona no encontrada')
    return JsonResponse({'error': 'Persona no encontrada'}, status=404)




@login_required
def calcular_cantidad_horas(request):
    hora_inicio = request.GET.get('hora_inicio')
    hora_fin = request.GET.get('hora_fin')
    if hora_inicio and hora_fin:
        try:
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin, '%H:%M').time()
            inicio = timedelta(hours=hora_inicio.hour, minutes=hora_inicio.minute, seconds=hora_inicio.second)
            fin = timedelta(hours=hora_fin.hour, minutes=hora_fin.minute, seconds=hora_fin.second)
            cantidad_horas = (fin - inicio).total_seconds() / 3600  # Convertir segundos a horas
            return JsonResponse({'cantidad_horas': cantidad_horas})
        except ValueError:
            return JsonResponse({'error': 'Formato de hora inválido'}, status=400)
    return JsonResponse({'cantidad_horas': 0})
@login_required
def calcular_cantidad_dias(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    if fecha_inicio and fecha_fin:
        try:# Agregar log
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            cantidad_dias = (fecha_fin - fecha_inicio).days
            return JsonResponse({'cantidad_dias': cantidad_dias})
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
    return JsonResponse({'cantidad_dias': 0})

@csrf_exempt
def guardar_fecha(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        justificacion = request.POST.get('justificacion', '')
        correo = request.POST.get('correo')  # Capturar el correo

        if fecha:
            request.session['fecha'] = fecha
            if justificacion:
                request.session['justificacion'] = justificacion
            if correo:
                request.session['correo'] = correo  # Guardar el correo en la sesión
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Fecha no proporcionada'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)



def test_view(request):
    return HttpResponse("Hello, Azure!")