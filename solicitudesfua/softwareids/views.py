
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import os
from .forms import CampoForm, NovedadFormTipo1, NovedadFormTipo2, NovedadFormTipo3, NovedadFormTipo4, NovedadFormTipo10,NovedadFormTipo11, NovedadFormTipo12, NovedadFormTipo13, NovedadFormTipo14,NovedadFormTipo15, NovedadFormTipo16, NovedadFormTipo18, NovedadFormTipo17, NovedadFormTipo19, NovedadFormTipo20, NovedadFormTipo21, NovedadFormTipo22, NovedadFormTipo23,  NovedadFormTipo5, NovedadFormTipo6, NovedadFormTipo7, NovedadFormTipo8, NovedadFormTipo9
from .utils import  obtener_access_token, sincronizar_con_sharepoint, fetch_personas_from_odoo_usuarios, fetch_zonas_from_odoo, fetch_personas_from_odoo
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import NovedadBase
from django.views.decorators.http import require_GET
from django.http import Http404, JsonResponse
from django.utils.safestring import mark_safe



logger = logging.getLogger(__name__)


def index(request):
    context = {
            'APP': os.getenv('APP', 'No definido'),
            # Agrega más variables según sea necesario
        }
    return render(request, 'home.html', context)

@login_required
def home(request):
    """correo = request.user.email
    personas = fetch_personas_from_odoo_usuarios(correo)
    zonas = fetch_zonas_from_odoo()
    return render(request, 'menuppal.html', {'personas': personas, 'zonas': zonas})"""
    correo = request.user.email
    personas = fetch_personas_from_odoo_usuarios(correo)
    zonas = fetch_zonas_from_odoo()

    if request.method == 'POST':
        campo_form = CampoForm(request.POST)
        if  campo_form.is_valid():
            campo = campo_form.save(commit=False)
            campo.save()
            return redirect('/azure_auth/novedades/')  # Define una URL de éxito

    else:
        campo_form = CampoForm()

    return render(request, 'menuppal.html', { 'campo_form': campo_form, 'personas': personas})


    # Usar print para depuración rápida o considerar logging.debug para producción
# views.py

@login_required
def novedad_view(request):
    tipos_novedad = NovedadBase._meta.get_field('tipo_novedad').choices
    return render(request, 'form.html', {'tipos_novedad': tipos_novedad})
"""# Renderiza la página principal
@login_required
def cargar_formulario_novedad(request, tipo_novedad):
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

    form = FormClass()
    return render(request, 'formulario_novedad.html', {'form': form, 'tipo_novedad': tipo_novedad})"""
# Renderiza la página principal
@login_required
def cargar_formulario_novedad(request, tipo_novedad):
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

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            logger.debug(f'Cedula recibida: {cedula}')

            # Obtener la fecha de ingreso desde Odoo solo para el formulario tipo 8
            if tipo_novedad == 'opcion8':
                personas = fetch_personas_from_odoo()
                fecha_ingreso = ''
                for persona in personas:
                    if persona[0] == cedula:
                        fecha_ingreso = persona[3]
                        break

                logger.debug(f'Fecha de ingreso obtenida: {fecha_ingreso}')

                # Guardar en la base de datos
                novedad = form.save(commit=False)
                novedad.fecha_ingreso = fecha_ingreso
                novedad.save()
            else:
                form.save()

            # Redirigir o mostrar un mensaje de éxito
            return redirect('url_de_exito')

    else:
        form = FormClass()
        personas_data = fetch_personas_from_odoo()
        personas_data_dict = {
            persona[0]: {
                'nombre': persona[1],
                'fecha_ingreso': persona[3]
            } for persona in personas_data
        }

    return render(request, 'formulario_novedad.html', {
        'form': form,
        'tipo_novedad': tipo_novedad,
        'personas_data_json': mark_safe(json.dumps(personas_data_dict))
    })



"""@login_required
def novedad_view(request):
    if request.method == 'POST':
        form = NovedadForm(request.POST)
        if form.is_valid():
            tipo_novedad = form.cleaned_data['tipo_novedad']
            if tipo_novedad == 'opcion1':
                novedad = NovedadTipo1.objects.create(
                    fecha=form.cleaned_data['fecha'],
                    persona=form.cleaned_data['persona'],
                    tipo_novedad=form.cleaned_data['tipo_novedad'],
                    detalle_opcion1=form.cleaned_data['detalle_opcion1'],
                    nombre=form.cleaned_data['nombre'],
                    zona=form.cleaned_data['zona']
                )
            elif tipo_novedad == 'opcion2':
                novedad = NovedadTipo2.objects.create(
                    fecha=form.cleaned_data['fecha'],
                    persona=form.cleaned_data['persona'],
                    tipo_novedad=form.cleaned_data['tipo_novedad'],
                    detalle_opcion2=form.cleaned_data['detalle_opcion2'],
                    nombre=form.cleaned_data['nombre'],
                    zona=form.cleaned_data['zona']
                )
            elif tipo_novedad == 'opcion3':
                novedad = NovedadTipo3.objects.create(
                    fecha=form.cleaned_data['fecha'],
                    persona=form.cleaned_data['persona'],
                    tipo_novedad=form.cleaned_data['tipo_novedad'],
                    detalle_opcion3=form.cleaned_data['detalle_opcion3'],
                    nombre=form.cleaned_data['nombre'],
                    zona=form.cleaned_data['zona']
                )
            return redirect('success_page')
    else:
        initial_data = request.GET.get('tipo_novedad', 'opcion1')
        form = NovedadForm(initial={'tipo_novedad': initial_data})

    return render(request, 'form.html', {'form': form})"""


@csrf_exempt
def enviar_a_sharepoint(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logging.info(f'info desde enviar a sharepoint {data}')
            access_token = obtener_access_token()
            if access_token:
                resultados = sincronizar_con_sharepoint(data, access_token)
                # Verificar si todos los resultados fueron exitosos
                if all("enviado exitosamente" in resultado for resultado in resultados):
                    return JsonResponse({'status': 'success'}, status=200)
                else:
                    return JsonResponse({'status': 'partial_success', 'details': resultados}, status=207)
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
