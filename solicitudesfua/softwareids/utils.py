import os
import xmlrpc.client
from django.http import JsonResponse
from dotenv import load_dotenv
from django.http import JsonResponse
import requests
import json
import logging
from datetime import datetime

load_dotenv()
database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
client_id = os.getenv("CLIENT_ID_LIST")
tenant_id = os.getenv("TENANT_ID_LIST")
client_secret = os.getenv("CLIENT_SECRET_LIST")
scope = 'https://graph.microsoft.com/.default'
site_id = os.getenv("SITE_ID_LIST")
list_name = os.getenv("LIST_NAME_LIST")

def fetch_personas_from_odoo():
    
    try:
        
        common = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/common')
        uid = common.authenticate(database, user, password, {})
        models = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/object')
        logger.debug(f'Authenticated user ID: {uid}')
        
        personas = models.execute_kw(database, uid, password,
            'hr.employee', 'search_read',
            [[('company_id.name', '=', 'Programa de Gestión del Aseo de la Ciudad')]],
            {'fields': ['identification_id', 'name', 'x_studio_zona_proyecto_aseo']})#'job_title.name']})
        
        if personas:
            logger.debug(f'Retrieved {len(personas)} personas')
        else:
            logger.debug('No personas found')
        #return [(persona['identification_id'], persona['name']) for persona in personas if 'identification_id' in persona and 'name' in persona]
        return [(persona['identification_id'], persona['name'], persona.get('x_studio_zona_proyecto_aseo', '')) for persona in personas if 'identification_id' in persona and 'name' in persona]
        #return [(str(persona['identification_id']), persona['name']) for persona in personas if 'identification_id' in persona and 'name' in persona]

    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return []


def obtener_personas_ajax(request):
    try:
        personas = fetch_personas_from_odoo()
        return JsonResponse(personas, safe=False)
    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return JsonResponse({'error': 'Failed to fetch data', 'details': str(e)}, status=500)
    
    # views.py

def obtener_access_token():
    """Obtiene el token de acceso para SharePoint."""
    url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    data = {
        'client_id': client_id,
        'scope': scope,
        'client_secret': client_secret,
        'grant_type': 'client_credentials',
    }
    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    token_response = response.json()
    access_token = token_response.get('access_token')
    if access_token:
        print("Token de acceso obtenido exitosamente:", access_token)
        return access_token
    print("Error al obtener el token de acceso:", token_response)
    return None  # Esto lanzará un error si la solicitud falla

# views.py

"""def sincronizar_con_sharepoint(registros, access_token):
    results = []
    for registro in registros:
        try:
            logging.info(f'Procesando registro: {registro}')
            if not isinstance(registro, dict):
                logging.error("Registro recibido no es un diccionario: %s", type(registro))
                continue

            nombre = registro.get('nombre')
            persona = registro.get('persona')
            TipoNovedadText = registro.get('tipo_novedad_text')
            fecha = registro.get('fecha')
            zona = registro.get('zona')
            detalle = registro.get('detalle')
            
            logging.info(f'Registro a enviar: {registro}')

            data = {
                'fields': {
                    'Title': nombre,
                    'Nombre': persona,
                    'TipoNovedad': TipoNovedadText,
                    'Fecha': fecha,
                    'Zona': zona,
                    'Detalle': detalle
                }
            }
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_name}/items'
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                logging.info(f'Registro {nombre} enviado exitosamente a SharePoint.')
                logging.info(f'info enviada {TipoNovedadText}')
                results.append(f'Registro {nombre} enviado exitosamente.')
            else:
                error_message = response.json().get('error', {}).get('message', 'No error message provided')
                logging.error(f'Error al enviar registro {nombre} a SharePoint: {error_message}')
                results.append(f'Error al enviar registro {nombre}: {error_message}')
                
        except json.JSONDecodeError:
            logging.error("Error decoding registro from JSON.")
            results.append("Error decoding registro from JSON.")
        except KeyError as e:
            logging.error(f"Falta la clave {e} en los datos del registro.")
            results.append(f"Falta la clave {e} en los datos del registro.")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            results.append(f"An error occurred: {str(e)}")

    return results

"""
"""def sincronizar_con_sharepoint(registros, access_token):
    results = []
    for registro in registros:
        try:
            logging.info(f'Procesando registro: {registro}')
            if not isinstance(registro, dict):
                logging.error("Registro recibido no es un diccionario: %s", type(registro))
                continue

            nombre = registro.get('nombre')
            persona = registro.get('persona')
            tipo_novedad_text = registro.get('tipo_novedad_text')
            fecha = registro.get('fecha')
            zona = registro.get('zona') or ''  # Asegurarse de que zona no sea False o None
            detalle = registro.get('detalle') or ''  # Asegurarse de que detalle no sea None
            
            logging.info(f'Registro a enviar: {registro}')

            data = {
                'fields': {
                    'Title': nombre,
                    'Nombre': persona,
                    'TipoNovedad': tipo_novedad_text,
                    'Fecha': fecha,
                    'Zona': zona,
                    'Detalle': detalle
                }
            }
            logging.info(f'Datos a enviar: {data}')  # Añadimos un log para ver los datos antes de enviarlos
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_name}/items'
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                logging.info(f'Registro {nombre} enviado exitosamente a SharePoint.')
                results.append(f'Registro {nombre} enviado exitosamente.')
            else:
                error_message = response.json().get('error', {}).get('message', 'No error message provided')
                logging.error(f'Error al enviar registro {nombre} a SharePoint: {error_message}')
                logging.error(f'Response details: {response.json()}')  # Añadimos detalles de la respuesta
                results.append(f'Error al enviar registro {nombre}: {error_message}')
                
        except json.JSONDecodeError:
            logging.error("Error decoding registro from JSON.")
            results.append("Error decoding registro from JSON.")
        except KeyError as e:
            logging.error(f"Falta la clave {e} en los datos del registro.")
            results.append(f"Falta la clave {e} en los datos del registro.")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            results.append(f"An error occurred: {str(e)}")

    return results"""


def sincronizar_con_sharepoint(registros, access_token):
    results = []
    for registro in registros:
        try:
            logging.info(f'Procesando registro: {registro}')
            if not isinstance(registro, dict):
                logging.error("Registro recibido no es un diccionario: %s", type(registro))
                continue

            fields = registro.get('fields', {})
            if not fields:
                logging.error(f"El registro {registro} no contiene datos válidos para enviar.")
                results.append(f"El registro {registro} no contiene datos válidos para enviar.")
                continue

            logging.info(f'Registro a enviar: {fields}')

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            }
            url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/lists/{list_name}/items'
            response = requests.post(url, headers=headers, json={'fields': fields})
            
            if response.status_code == 201:
                logging.info(f'Registro {fields.get("Title")} enviado exitosamente a SharePoint.')
                results.append(f'Registro {fields.get("Title")} enviado exitosamente.')
            else:
                error_message = response.json().get('error', {}).get('message', 'No error message provided')
                logging.error(f'Error al enviar registro {fields.get("Title")} a SharePoint: {error_message}')
                logging.error(f'Response details: {response.json()}')
                results.append(f'Error al enviar registro {fields.get("Title")}: {error_message}')
                
        except json.JSONDecodeError:
            logging.error("Error decoding registro from JSON.")
            results.append("Error decoding registro from JSON.")
        except KeyError as e:
            logging.error(f"Falta la clave {e} en los datos del registro.")
            results.append(f"Falta la clave {e} en los datos del registro.")
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            results.append(f"An error occurred: {str(e)}")

    return results


logger = logging.getLogger(__name__)

def fetch_personas_from_odoo_usuarios(correo):
    try:
        common = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/common')
        uid = common.authenticate(database, user, password, {})
        models = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/object')
        logger.debug(f'Authenticated user ID: {uid}')
        
        personas = models.execute_kw(database, uid, password,
            'hr.employee', 'search_read',
            [[('work_email', '=', correo)]],
            {'fields': ['identification_id', 'name', 'x_studio_zona_proyecto_aseo', 'work_email']})

        if personas:
            logger.debug(f'Retrieved {len(personas)} personas')
        else:
            logger.debug('No personas found')

        return [(persona['identification_id'], persona['name'], persona.get('x_studio_zona_proyecto_aseo', ''), persona.get('work_email', '')) for persona in personas if 'identification_id' in persona and 'name' in persona]

    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return []
    
def fetch_zonas_from_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/common')
        uid = common.authenticate(database, user, password, {})
        models = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/object')
        logger.debug(f'Authenticated user ID: {uid}')
        
        # Obtener todas las zonas
        zonas = models.execute_kw(database, uid, password,
            'x_zonas_aseo', 'search_read',
            [[]],  # Filtrar si es necesario
            {'fields': ['x_name']})

        if zonas:
            logger.debug(f'Retrieved {len(zonas)} zonas')
        else:
            logger.debug('No zonas found')
        print("ZONAS", zonas)
        return [zona['x_name'] for zona in zonas if 'x_name' in zona]

    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return []
def fetch_rutas_from_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/common')
        uid = common.authenticate(database, user, password, {})
        models = xmlrpc.client.ServerProxy(f'{host}/xmlrpc/2/object')
        logger.debug(f'Authenticated user ID: {uid}')
        
        # Obtener todas las zonas
        rutas = models.execute_kw(database, uid, password,
            'x_rutas', 'search_read',
            [[]],  # Filtrar si es necesario
            {'fields': ['x_name']})

        if rutas:
            logger.debug(f'Retrieved {len(rutas)} zonas')
        else:
            logger.debug('No zonas found')
        print("RUTAS", rutas)
        return [ruta['x_name'] for ruta in rutas if 'x_name' in ruta]

    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return []
    
def rutas_json_view(request):
    try:
        rutas = fetch_rutas_from_odoo()
        print("RUTAS     API", rutas)
        return JsonResponse(rutas, safe=False)
    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return JsonResponse({'error': 'Failed to fetch data', 'details': str(e)}, status=500)    
def zonas_json_view(request):
    try:
        zonas = fetch_zonas_from_odoo()
        print("ZONAS API",zonas)
        return JsonResponse(zonas, safe=False)
    except Exception as e:
        logger.error('Failed to fetch data from Odoo', exc_info=True)
        return JsonResponse({'error': 'Failed to fetch data', 'details': str(e)}, status=500)
