from django.db import models
from django.db import models
from datetime import timedelta


class NovedadBase(models.Model):
    fecha = models.DateField(default='')
    persona = models.CharField(max_length=200)
    tipo_novedad = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Ausencias injustificadas'),
            ('opcion2', 'Permisos'),
            ('opcion3', 'Cambios de turno'),
            ('opcion4', 'Cambios de zona'),
            ('opcion5', 'Circular 014 de 2018'),
            ('opcion6', 'Horas extras eventos/operativos'),
            ('opcion7', 'Incapacidad'),
            ('opcion8', 'Ingreso de operarios nuevos'),
            ('opcion9', 'Licencias'),
            ('opcion10', 'Emepleado hospitalizados'),
            ('opcion11', 'Continúan en vacaciones por incapacidades o calamidades dentro del periodo'),
            ('opcion12', 'Ingresa después de incapacidades largas.'),
            ('opcion13', 'No laboran por procesos disciplinarios'),
            ('opcion14', 'Stand by FUA restringidos.'),
            ('opcion15', 'Pruebas de alcoholemia positiva'),
            ('opcion16', 'Reemplazos de vehículos'),
            ('opcion17', 'Renuncias a calamidades'),
            ('opcion18', 'Retiros'),
            ('opcion19', 'Salidas tarde'),
            ('opcion20', 'Servicios adicionales'),
            ('opcion21', 'Suspensiones'),
            ('opcion22', 'Urgencias médicas EPS/ ARL'),
            

        ],
    )
    zona = models.CharField(max_length=200)
    novedad_extemporanea = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
    )

    def __str__(self):
        return f'{self.fecha} - {self.persona}'

class Usuario(models.Model):
    cedula = models.CharField(max_length=200, unique=True)
    nombre = models.CharField(max_length=200)
    correo = models.EmailField(unique=True)
    departamento = models.EmailField(unique=True)
    def __str__(self):
        return self.nombre

class Campo(models.Model):
    observaciones = models.CharField(max_length=200)
    horallegada = models.TextField()
    tipo_incapacidad = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'EPS'),
            ('opcion2', 'ARL'),
            ('opcion3', 'SOAT'),
        ],
    )
    tipo_permisos = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Calamidades'),
            ('opcion2', 'Permisos no remunerados/remunerados'),
            ('opcion3', 'Día de la familia'),
        ],
    )
    rutas= models.CharField(max_length=200)
    reemplaza = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
    )
    colaborador = models.CharField(max_length=200)
    horasextra =  models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Si'),
            ('opcion2', 'No'),
        ],
        default='opcion2'
    )
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    zona_inicial = models.CharField(max_length=200)
    zona_reemplazo = models.CharField(max_length=200)
    hora_llegada = models.TimeField()
    fecha_ingreso = models.DateField(default='')
    fecha_inicial= models.DateField(default='')
    fecha_final = models.DateField(default='')
    tipos_licencia = models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Maternidad'),
            ('opcion2', 'Paternidad'),
            ('opcion3', 'Luto'),
            ('opcion4', 'pre-parto'),
        ],
    )
    control= models.CharField(max_length=200)
    consecutivo= models.CharField(max_length=200)
    nuevo_control = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_terminacion = models.DateField()
    motivo_renuncia= models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Renuncia'),
            ('opcion2', 'Terminación en periodo de prueba'),
            ('opcion3', 'Terminación con justa causa'),
            ('opcion4', 'Terminación sin justa causa'),
            ('opcion5', 'Pension'),
            ('opcion6', 'Fallecido'),            
        ],
    )
    tipo_servicio= models.CharField(
        max_length=50,
        choices=[
            ('opcion1', 'Compactador'),
            ('opcion2', 'Barredora'),            
        ],
    )
    
    cantidad_horas_extra = models.FloatField(null=True, blank=True)
    justificacion = models.TextField(null=True, blank=True)
    
    
    @property
    def cantidad_horas(self):
        if self.horasextra == 'opcion1' and self.hora_inicio and self.hora_fin:
            inicio = timedelta(hours=self.hora_inicio.hour, minutes=self.hora_inicio.minute, seconds=self.hora_inicio.second)
            fin = timedelta(hours=self.hora_fin.hour, minutes=self.hora_fin.minute, seconds=self.hora_fin.second)
            cantidad_horas = (fin - inicio).total_seconds() / 3600  # Convertir segundos a horas
            return cantidad_horas
        return 0
    
    @property
    def cantidad_dias(self):
        delta = self.fecha_fin - self.fecha_inicio
        return delta.days

    def __str__(self):
        return self.tipo_incapacidad - self.observaciones