$(document).ready(function() {
    const params = new URLSearchParams(window.location.search);
    const nombre = params.get('nombre');
    const zona = params.get('zona');
    var personasData = [];

    if (nombre && zona) {
        $('#userInfo').text(`Reportando: ${nombre} en la zona ${zona}`);
    } else {
        console.error('Nombre o zona no recibidos correctamente');
    }

    $('#tipoNovedadSelect').select2();

    $('#agregarNovedadBtn').click(function() {
        var tipoNovedad = $('#tipoNovedadSelect').val();
        if (tipoNovedad) {
            cargarFormularioNovedad(tipoNovedad);
        } else {
            alert('Por favor, seleccione un tipo de novedad.');
        }
    });

    function cargarFormularioNovedad(tipoNovedad) {
        $.ajax({
            url: `/azure_auth/novedades/formulario/${tipoNovedad}/`,
            type: 'GET',
            success: function(data) {
                $('#novedadModal .modal-body').html(data);
                $('#novedadModalLabel').text('Nueva Novedad - ' + $('#tipoNovedadSelect option:selected').text());
                $('#novedadModal').modal('show');

                // Adjuntar evento submit al nuevo formulario cargado
                $('#novedadForm').on('submit', function(event) {
                    event.preventDefault();
                    var form = $(this);
                    var tipoNovedad = form.attr('id').split('_')[1];
                    var index = $('#novedadModal').data('edit-index');
                    var registros = JSON.parse(localStorage.getItem('registros')) || [];

                    var selectedId = form.find('#id_persona').val();
                    var selectedPersona = personasData.find(p => p[0] === selectedId);

                    if (!selectedPersona) {
                        alert('Por favor, seleccione una persona.');
                        return;
                    }

                    var novedad = {
                        nombre: selectedPersona[1],
                        cedula: selectedPersona[0],
                        tipoNovedad: tipoNovedad,
                        tipoNovedadText: $('#tipoNovedadSelect option:selected').text(),
                        fecha: form.find('#id_fecha').val(),
                        zona: selectedPersona[2]
                    };

                    // Agrega solo los campos relevantes según el tipo de novedad
                    form.find(':input').each(function() {
                        var input = $(this);
                        if (input.attr('id').startsWith('id_') && input.val()) {
                            var fieldName = input.attr('id').replace('id_', '');
                            novedad[fieldName] = input.val();
                        }
                    });

                    // Validar y agregar a la tabla correspondiente
                    var tableId;
                    if (['opcion1', 'opcion2', 'opcion3', 'opcion4', 'opcion5', 'opcion6', 'opcion7'].includes(tipoNovedad)) {
                        tableId = '#novedadesTableAusencias';
                    } else if (['opcion8', 'opcion9', 'opcion10', 'opcion11', 'opcion12'].includes(tipoNovedad)) {
                        tableId = '#novedadesTableIngresosRetiros';
                    } else if (['opcion13', 'opcion14', 'opcion15', 'opcion16', 'opcion17'].includes(tipoNovedad)) {
                        tableId = '#novedadesTableOperativos';
                    } else if (['opcion18', 'opcion19', 'opcion20', 'opcion21'].includes(tipoNovedad)) {
                        tableId = '#novedadesTablePersonal';
                    } else {
                        alert('Tipo de novedad no válido');
                        return;
                    }

                    if (index >= 0) {
                        registros[index] = novedad;
                    } else {
                        registros.push(novedad);
                    }

                    guardarRegistrosLocales(registros);
                    $(tableId).empty();
                    cargarRegistrosLocales();
                    $('#novedadModal').modal('hide').removeData('edit-index');
                });
            },
            error: function(error) {
                console.error('Error al cargar el formulario: ', error);
                alert('Error al cargar el formulario. Por favor, intente nuevamente.');
            }
        });
    }

    function guardarRegistrosLocales(registros) {
        localStorage.setItem('registros', JSON.stringify(registros));
    }

    function cargarRegistrosLocales() {
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        $('#novedadesTableAusencias').empty();
        $('#novedadesTableIngresosRetiros').empty();
        $('#novedadesTableOperativos').empty();
        $('#novedadesTablePersonal').empty();
        registros.forEach(function(novedad, index) {
            var tableId;
            if (['opcion1', 'opcion2', 'opcion3', 'opcion4', 'opcion5', 'opcion6', 'opcion7'].includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableAusencias';
            } else if (['opcion8', 'opcion9', 'opcion10', 'opcion11', 'opcion12'].includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableIngresosRetiros';
            } else if (['opcion13', 'opcion14', 'opcion15', 'opcion16', 'opcion17'].includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableOperativos';
            } else if (['opcion18', 'opcion19', 'opcion20', 'opcion21'].includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTablePersonal';
            }

            agregarRegistroATabla(novedad, index, tableId);
        });
    }

    function agregarRegistroATabla(novedad, index, tableId) {
        var newRow = `<tr data-index="${index}">
                        <td>${novedad.nombre}</td>
                        <td>${novedad.cedula}</td>
                        <td>${novedad.observaciones || ''}</td>
                        <td>${novedad.zona || ''}</td>
                        <td>${novedad.reemplaza || ''}</td>
                        <td>${novedad.colaborador || ''}</td>
                        <td>${novedad.horas_extra || ''}</td>
                        <td>${novedad.hora_inicio || ''}</td>
                        <td>${novedad.hora_fin || ''}</td>
                        <td>${novedad.fecha_inicial || ''}</td>
                        <td>${novedad.fecha_final || ''}</td>
                        <td>${novedad.tipo_licencia || ''}</td>
                        <td>${novedad.fecha_ingreso_odoo || ''}</td>
                        <td>${novedad.fecha_inicio || ''}</td>
                        <td>${novedad.fecha_fin || ''}</td>
                        <td>${novedad.motivo || ''}</td>
                        <td>${novedad.ruta || ''}</td>
                        <td>${novedad.zona_inicial || ''}</td>
                        <td>${novedad.control || ''}</td>
                        <td>${novedad.nuevo_control || ''}</td>
                        <td>${novedad.tipo_servicio || ''}</td>
                        <td>${novedad.cantidad_horas || ''}</td>
                        <td>${novedad.novedad_extemporanea || ''}</td>
                        <td>${novedad.cantidad_dias || ''}</td>
                        <td>
                            <button class="btn btn-warning btn-sm edit">Editar</button>
                            <button class="btn btn-danger btn-sm delete">Eliminar</button>
                        </td>
                    </tr>`;
        $(tableId).append(newRow);
    }

    $(document).on('click', '.delete', function() {
        var index = $(this).closest('tr').data('index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        registros.splice(index, 1);
        guardarRegistrosLocales(registros);
        cargarRegistrosLocales();
    });

    $(document).on('click', '.edit', function() {
        var index = $(this).closest('tr').data('index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        var novedad = registros[index];

        if (novedad) {
            $('#id_persona').val(novedad.cedula).trigger('change');
            $('#id_tipo_novedad').val(novedad.tipoNovedad).trigger('change');
            $('#id_fecha').val(novedad.fecha);
            if (novedad.tipoNovedad === 'opcion1') {
                $('#id_observaciones').val(novedad.observaciones).show();
            } else if (novedad.tipoNovedad === 'opcion2') {
                $('#id_tipo_permisos').val(novedad.tipo_permisos).show();
            } else if (novedad.tipoNovedad === 'opcion3') {
                $('#id_rutas').val(novedad.rutas).show();
                $('#id_reemplaza').val(novedad.reemplaza).show();
                $('#id_zona_reemplazo').val(novedad.zona_reemplazo).show();
                $('#id_horasextra').val(novedad.horasextra).show();
                $('#id_hora_inicio').val(novedad.hora_inicio).show();
                $('#id_hora_fin').val(novedad.hora_fin).show();
            } else if (novedad.tipoNovedad === 'opcion4') {
                $('#id_zona_inicial').val(novedad.zona_inicial).show();
                $('#id_reemplaza').val(novedad.reemplaza).show();
                $('#id_zona_reemplazo').val(novedad.zona_reemplazo).show();
            }
            $('#novedadModal').data('edit-index', index).modal('show');
        }
    });

    $('#guardarBtn').click(function() {
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        console.log(registros);
        enviarDatosASharePoint(registros);
    });

    function enviarDatosASharePoint(registros) {
        var data = registros.map(function(novedad) {
            return {
                nombre: novedad.nombre,
                persona: novedad.cedula,
                tipo_novedad: novedad.tipoNovedad,
                tipo_novedad_text: novedad.tipoNovedadText,
                fecha: novedad.fecha,
                zona: novedad.zona,
                detalle: novedad.observaciones
            };
        });
    
        $.ajax({
            url: '/api/sharepoint/',
            type: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            success: function(response) {
                if (response.status === 'success') {
                    console.log('Datos enviados correctamente a SharePoint');
                    localStorage.removeItem('registros');
                    cargarRegistrosLocales();
                    alert('Datos guardados y almacenamiento local limpiado.');
                } else if (response.status === 'partial_success') {
                    console.error('Error parcial al enviar datos a SharePoint', response.details);
                    alert('Algunos datos no se pudieron enviar. Verifique los detalles.');
                }
            },
            error: function(error) {
                console.error('Error al enviar datos a SharePoint', error);
                alert('Error al enviar datos a SharePoint. Por favor, intente nuevamente.');
            }
        });
    }

    cargarRegistrosLocales();
});
