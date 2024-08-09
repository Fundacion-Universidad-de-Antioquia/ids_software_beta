from django import forms
from .models import  Usuario, Campo, NovedadBase
from datetime import date
from .utils import fetch_zonas_from_odoo, fetch_personas_from_odoo, fetch_rutas_from_odoo,fetch_personas_from_odoo_usuarios

class NovedadFormBase(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','readonly': 'readonly'}))
    justificacion = forms.CharField(widget=forms.HiddenInput(), required=False)  # Ocultar el campo con CSS
    #fecha = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    #fecha = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), initial=date.today)
    Persona = forms.ChoiceField(choices=[], label='Persona')
    zona = forms.ChoiceField(choices=[], label='Zona')
    novedad_extemporanea = forms.ChoiceField(
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
        label='Novedad Extemporánea',
        initial='opcion2'  # Establecer valor predeterminado a "No"
    )

    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        initial = kwargs.get('initial', {})
        initial.setdefault('fecha', date.today().isoformat())  # Establecer la fecha predeterminada
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)
        
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['zona'].choices = zona_choices
        self.fields['Persona'].choices = persona_choices
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
    
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    horasextra = forms.ChoiceField(
        choices=[('opcion1', 'Si'), ('opcion2', 'No')],
        label='Horas Extra',
        initial='opcion2'
    )
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')

    class Meta:
        model = Campo
        fields = ['rutas', 'reemplaza', 'zona_reemplazo', 'horasextra', 'hora_inicio', 'hora_fin', 'cantidad_horas']

    def __init__(self, *args, **kwargs):
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        self.fields['hora_inicio'].required = False
        self.fields['hora_fin'].required = False
        
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices

        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona_reemplazo'].choices = zona_choices

        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
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
        
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        zona_inicial = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_inicial]
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        self.fields['zona_reemplazo'].choices = zona_choices  
        self.fields['zona_inicial'].choices = zona_choices 

class NovedadFormTipo5(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['hora_llegada']

class NovedadFormTipo6(NovedadFormBase, forms.ModelForm):
    horasextra = forms.ChoiceField(
        choices=[('opcion1', 'Si'), ('opcion2', 'No')],
        label='Horas Extra',
        initial='opcion1'
    )
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['hora_inicio', 'hora_fin','cantidad_horas']

class NovedadFormTipo7(NovedadFormBase, forms.ModelForm):
    zona_reemplazo = forms.ChoiceField(choices=[], label='Zona Reemplazo')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    colaborador = forms.ChoiceField(choices=[], label='Colaborador Reemplazo')
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['tipo_incapacidad','rutas', 'reemplaza','horasextra','hora_inicio', 'hora_fin','cantidad_horas']
    def __init__(self, *args, **kwargs):
        
        departamento = kwargs.pop('departamento', None) 
        super().__init__(*args, **kwargs)
        zona_reemplazo = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zona_reemplazo]
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        personas = fetch_personas_from_odoo(departamento)
        persona_choices = [(persona[0], f"{persona[0]} - {persona[1]}") for persona in personas]
        self.fields['Persona'].choices = persona_choices
        
        # Aquí, colaborador_choices se puede inicializar igual que persona_choices 
        # ya que se está filtrando por el mismo departamento.
        colaborador_choices = persona_choices
        self.fields['colaborador'].choices = colaborador_choices
        
        self.fields['rutas'].choices = ruta_choices
        self.fields['zona_reemplazo'].choices = zona_choices    

class NovedadFormTipo8(NovedadFormBase, forms.ModelForm):
    fecha_ingreso = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Fecha de Ingreso')

    class Meta:
        model = Campo
        fields = ['fecha_ingreso']  # Añadir los campos necesarios

    def __init__(self, *args, **kwargs):
        super(NovedadFormTipo8, self).__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].widget.attrs['readonly'] = True


class DateInput(forms.DateInput):
    input_type = 'date'

class NovedadFormTipo9(NovedadFormBase, forms.ModelForm):
    cantidad_dias = forms.IntegerField(label='Cantidad de Días', required=False)

    class Meta:
        model = Campo
        fields = ['fecha_inicial', 'fecha_final', 'tipos_licencia']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True


class NovedadFormTipo10(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['observaciones']        
    

class NovedadFormTipo11(NovedadFormBase, forms.ModelForm):
    
    cantidad_dias = forms.IntegerField(label='Cantidad de Días', required=False)
    class Meta:
        model = Campo
        fields = ['fecha_inicial', 'fecha_final']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True

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
    cantidad_dias = forms.IntegerField(label='Cantidad de Días', required=False)
    class Meta:
        model = Campo
        fields = ['fecha_inicio', 'fecha_fin', 'observaciones']
        widgets = {
            'fecha_inicial': DateInput(attrs={'class': 'form-control'}),
            'fecha_final': DateInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cantidad_dias'].widget.attrs['readonly'] = True

class NovedadFormTipo18(NovedadFormBase, forms.ModelForm):
    class Meta:
        model = Campo
        fields = ['motivo_renuncia']

class NovedadFormTipo19(NovedadFormBase, forms.ModelForm):
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    rutas = forms.ChoiceField(choices=[], label='Ruta')
    
    class Meta:
        model = Campo
        fields = ['hora_inicio', 'hora_fin','cantidad_horas']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rutas = fetch_rutas_from_odoo()
        ruta_choices = [(ruta, ruta) for ruta in rutas]
        self.fields['rutas'].choices = ruta_choices

class NovedadFormTipo20(NovedadFormBase, forms.ModelForm):
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = ['consecutivo','tipo_servicio', 'hora_inicio', 'hora_fin','horasextra', 'cantidad_horas']

class NovedadFormTipo21(NovedadFormBase, forms.ModelForm):
    rutas = forms.ChoiceField(choices=[], label='Ruta')   
    cantidad_horas = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=False, label='Cantidad de Horas')
    class Meta:
        model = Campo
        fields = [ 'hora_inicio', 'hora_fin','horasextra','zona_reemplazo', 'hora_inicio', 'hora_fin','horasextra','cantidad_horas']
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
        fields = ['cedula', 'nombre', 'correo','departamento']

class CampoForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',  # Esto utiliza el selector de fecha HTML5
                'class': 'form-control',  # Clase CSS para Bootstrap
                'readonly': 'readonly',  # Bloquear el campo de fecha
                'placeholder': 'Seleccione una fecha'  # Texto de marcador de posición
            }
        ),
        input_formats=['%Y-%m-%d'],  # Formato de entrada esperado
    )

    zona = forms.ChoiceField(choices=[], label='Zona')

    justificacion = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Asegurarse de que tenga la clase form-control para el estilo
                'placeholder': 'Justifique por qué no realizó el reporte del día anterior en el horario establecido',
                'rows': 3,
                'id': 'justificacion-textarea'  # Identificador único
            }
        ),
        required=False,
        label='Justificación'
    )

    class Meta:
        model = NovedadBase
        fields = ['fecha', 'zona', 'justificacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener las zonas desde Odoo
        zonas = fetch_zonas_from_odoo()
        zona_choices = [(zona, zona) for zona in zonas]
        self.fields['zona'].choices = zona_choices