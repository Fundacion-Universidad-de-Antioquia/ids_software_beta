from django import forms
from .models import  Usuario, Campo, NovedadBase
from datetime import date
import json
from .utils import fetch_zonas_from_odoo, fetch_personas_from_odoo, fetch_rutas_from_odoo,fetch_personas_from_odoo_usuarios


"""class NovedadFormBase(forms.Form):
    fecha = forms.DateField()
    Persona = forms.ChoiceField(choices=[], label='Persona')
    zona = forms.ChoiceField(choices=[], label='Zona')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        personas = fetch_personas_from_odoo()
        colaborador_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = colaborador_choices
        self.fields['zona'].choices = zona_choices"""
class NovedadFormBase(forms.Form):
    fecha = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial=date.today)
    Persona = forms.ChoiceField(choices=[], label='Persona')
    zona = forms.ChoiceField(choices=[], label='Zona')
    novedad_extemporanea = forms.ChoiceField(
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
        label='Novedad Extemporánea'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        personas = fetch_personas_from_odoo()
        colaborador_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['zona'].choices = zona_choices
        self.fields['Persona'].choices = colaborador_choices
        self.personas_data = {persona[0]: persona for persona in personas}  # Almacena los datos de las personas

    def get_persona_data(self, identification_id):
        return self.personas_data.get(identification_id)
class NovedadFormTipo1(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']

class NovedadFormTipo2(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['tipo_permisos']


class NovedadFormTipo3(NovedadFormBase, forms.ModelForm):
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    horasextra = forms.ChoiceField(choices=[('Si', 'Sí'), ('No', 'No')], label='Horas Extra')
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')

    class Meta:
        model = Campo
        fields = ['rutas', 'reemplaza', 'zona_reemplazo', 'horasextra', 'hora_inicio', 'hora_fin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Obtener las personas desde Odoo
        personas = fetch_personas_from_odoo()
        colaborador_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        self.fields['zona_reemplazo'].choices = zona_choices  
        self.fields['colaborador'].choices = colaborador_choices


 
class TiposNovedades(forms.ModelForm):
    class Meta:
        model = NovedadBase
        fields = ['tipo_novedad']

        

class NovedadFormTipo4(NovedadFormBase, forms.ModelForm):
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    zona_inicial = forms.ChoiceField(choices=[], label='Zona Inicial')
    class Meta:
        model = Campo
        fields = ['reemplaza']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zona_inicial = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_inicial]
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        personas = fetch_personas_from_odoo()
        colaborador_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['colaborador'].choices = colaborador_choices
        self.fields['zona_reemplazo'].choices = zona_choices  
        self.fields['zona_inicial'].choices = zona_choices 

class NovedadFormTipo5(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['hora_llegada']

class NovedadFormTipo6(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['hora_inicio', 'hora_fin']

class NovedadFormTipo7(NovedadFormBase, forms.ModelForm):
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    class Meta:
        model = Campo
        fields = ['tipo_incapacidad','rutas', 'reemplaza','horasextra','hora_inicio', 'hora_fin']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        personas = fetch_personas_from_odoo()
        colaborador_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices
        self.fields['colaborador'].choices = colaborador_choices
        self.fields['zona_reemplazo'].choices = zona_choices    

class NovedadFormTipo8(NovedadFormBase, forms.ModelForm):
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Fecha de Ingreso')

    class Meta:
        model = Campo
        fields = ['fecha_ingreso']  # Añadir los campos necesarios

    def __init__(self, *args, **kwargs):
        super(NovedadFormTipo8, self).__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].widget.attrs['readonly'] = True


class NovedadFormTipo9(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['fecha_inicial', 'fecha_final','tipos_licencia']

"""class NovedadFormTipo10(forms.ModelForm):
    zona = forms.ChoiceField(choices=[], label='Zona')
    class Meta:
            model = NovedadBase
            fields = ['fecha', 'persona', 'zona']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona'].choices = zona_choices"""
class NovedadFormTipo10(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']        
    

class NovedadFormTipo11(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['fecha_inicial', 'fecha_final']

class NovedadFormTipo12(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']

class NovedadFormTipo13(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']
class NovedadFormTipo14(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']

class NovedadFormTipo15(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']

class NovedadFormTipo16(NovedadFormBase, forms.ModelForm):
    zona_inicial = forms.ChoiceField(choices=[], label='Zona Inicial')
    class Meta:
        model = Campo
        fields = ['control', 'nuevo_control']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona_inicial'].choices = zona_choices    

class NovedadFormTipo17(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']

class NovedadFormTipo18(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['motivo_renuncia']

class NovedadFormTipo19(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    class Meta:
        model = Campo
        fields = ['hora_inicio', 'hora_fin']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices        

class NovedadFormTipo20(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['tipo_servicio', 'hora_inicio', 'hora_fin','horasextra']

class NovedadFormTipo21(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    class Meta:
        model = Campo
        fields = [ 'hora_inicio', 'hora_fin','horasextra','zona_reemplazo', 'hora_inicio', 'hora_fin','horasextra']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices          

class NovedadFormTipo22(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    class Meta:
        model = Campo
        fields = ['observaciones']  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices          

class NovedadFormTipo23(forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    class Meta:
        model = Campo
        fields = ['observaciones']  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['cedula', 'nombre', 'correo']

class CampoForm(forms.ModelForm):
    class Meta:
        model = NovedadBase
        fields = ['fecha','zona']
    

    zona = forms.ChoiceField(choices=[], label='Zona')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las zonas desde Odoo
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona'].choices = zona_choices