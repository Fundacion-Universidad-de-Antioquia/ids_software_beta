$(document).ready(function() {
    const params = new URLSearchParams(window.location.search);
    const nombre = params.get('nombre');
    const zona = params.get('zona');

    var personasDataElement = document.getElementById('personas-data');
    var personasData = JSON.parse(personasDataElement ? personasDataElement.textContent : '{}');

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

    function buscarFechaIngreso(personaId) {
        $.ajax({
            url: '/api/fecha/',
            type: 'GET',
            data: { persona_id: personaId },
            success: function(data) {
                if (data.fecha_ingreso) {
                    $('#id_fecha_ingreso').val(data.fecha_ingreso);
                } else {
                    alert('Fecha de ingreso no encontrada.');
                }
            },
            error: function(error) {
                console.error('Error al buscar la fecha de ingreso: ', error);
                alert('Error al buscar la fecha de ingreso. Por favor, intente nuevamente.');
            }
        });
    }

    function cargarFormularioNovedad(tipoNovedad, novedad = null, index = null) {
        $.ajax({
            url: `/azure_auth/novedades/formulario/${tipoNovedad}/`,
            type: 'GET',
            success: function(data) {
                $('#novedadModal .modal-body').html(data);
                $('#novedadModalLabel').text('Nueva Novedad - ' + $('#tipoNovedadSelect option:selected').text());
                $('#novedadModal').modal('show');

                if (novedad) {
                    $('#novedadModal').data('edit-index', index);
                    cargarValoresFormulario(novedad);
                }

                $('#id_Persona').change(function() {
                    var personaId = $(this).val().split(' - ')[0];
                    if (personaId) {
                        buscarFechaIngreso(personaId);
                    }
                });

                $('#id_novedad_extemporanea').change(function() {
                    var novedadExtemporanea = $(this).val();
                    
                    if (novedadExtemporanea === 'opcion1') { // 'Sí' seleccionado
                        $('#id_fecha').val('');
                        $('#id_fecha').attr('readonly', false);
                        $('#id_fecha').attr('required', true);
                        $('#id_fecha').attr('max', new Date().toISOString().split("T")[0]);
                    } else { // 'No' seleccionado
                        $('#id_fecha').val(new Date().toISOString().split('T')[0]);
                        $('#id_fecha').attr('readonly', true);
                        $('#id_fecha').removeAttr('required');
                        $('#id_fecha').removeAttr('max');
                    }
                });

                $('#id_horasextra').change(function() {
                    var horasextra = $(this).val();
                    if (horasextra === 'opcion1') {
                        $('#id_hora_inicio, #id_hora_fin').parent().show();
                        $('#id_hora_inicio, #id_hora_fin').attr('required', true);
                    } else {
                        $('#id_hora_inicio, #id_hora_fin').parent().hide();
                        $('#id_hora_inicio, #id_hora_fin').removeAttr('required').val('');
                    }
                });

                $('#novedadForm').off('submit').on('submit', function(event) {
                    var novedadExtemporanea = $('#id_novedad_extemporanea').val();
                    var fechaNovedad = $('#id_fecha').val();
                    var hoy = new Date();
                    hoy.setHours(0, 0, 0, 0); // Asegurar que se compara solo la fecha sin la hora
                
                    if (novedadExtemporanea === 'opcion1' && (!fechaNovedad || new Date(fechaNovedad) >= hoy)) {
                        event.preventDefault();
                        alert('Por favor, ingrese una fecha válida anterior a la fecha actual.');
                    } else {
                        guardarNovedad();
                    }
                });
                
            },
            error: function(error) {
                console.error('Error al cargar el formulario: ', error);
                alert('Error al cargar el formulario. Por favor, intente nuevamente.');
            }
        });
    }

    function guardarNovedad() {
        var form = $('#novedadForm');
        var tipoNovedad = $('#tipoNovedadSelect').val();
        var index = $('#novedadModal').data('edit-index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];

        var selectedOption = form.find('#id_Persona option:selected');
        var selectedId = selectedOption.val();
        var selectedText = selectedOption.text();
        var selectedPersona = selectedText.split(' - ');

        if (!selectedId || selectedPersona.length < 2) {
            alert('Por favor, seleccione una persona.');
            return;
        }

        var novedad = {
            nombre: selectedPersona[1],
            cedula: selectedPersona[0],
            tipoNovedad: tipoNovedad,
            tipoNovedadText: $('#tipoNovedadSelect option:selected').text(),
            fecha: form.find('#id_fecha').val(),
            zona: zona,
            fecha_ingreso: form.find('#id_fecha_ingreso').val(),
            novedad_extemporanea: form.find('#id_novedad_extemporanea').val()
        };

        form.find(':input').each(function() {
            var input = $(this);
            var inputId = input.attr('id');
            if (inputId && inputId.startsWith('id_') && input.val()) {
                var fieldName = inputId.replace('id_', '');
                if (input.is('select')) {
                    var optionSelected = form.find(`#${inputId} option:selected`);
                    var optionText = optionSelected.text();
                    novedad[fieldName] = optionText;
                } else {
                    novedad[fieldName] = input.val();
                }
            }
        });

        var tableId;
        var validTypesAusencias = ['opcion1', 'opcion2', 'opcion7', 'opcion9', 'opcion10', 'opcion11', 'opcion21', 'opcion22'];
        var validTypesIngresosRetiros = ['opcion8', 'opcion12', 'opcion17', 'opcion18'];
        var validTypesOperativos = ['opcion3', 'opcion4', 'opcion6', 'opcion16', 'opcion19', 'opcion20'];
        var validTypesPersonal = ['opcion5', 'opcion13', 'opcion14', 'opcion15'];

        if (validTypesAusencias.includes(tipoNovedad)) {
            tableId = '#novedadesTableAusencias';
        } else if (validTypesIngresosRetiros.includes(tipoNovedad)) {
            tableId = '#novedadesTableIngresosRetiros';
        } else if (validTypesOperativos.includes(tipoNovedad)) {
            tableId = '#novedadesTableOperativos';
        } else if (validTypesPersonal.includes(tipoNovedad)) {
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
    }

    function cargarValoresFormulario(novedad) {
        $('#id_Persona').val(novedad.cedula).trigger('change');
        $('#id_fecha').val(novedad.fecha);
        $('#id_fecha_ingreso').val(novedad.fecha_ingreso);
        $('#id_novedad_extemporanea').val(novedad.novedad_extemporanea).trigger('change');

        $('#tipoNovedadSelect').val(novedad.tipoNovedad).trigger('change');

        $('#novedadForm').find(':input').each(function() {
            var input = $(this);
            var inputId = input.attr('id');
            if (inputId && inputId.startsWith('id_')) {
                var fieldName = inputId.replace('id_', '');
                if (novedad[fieldName]) {
                    if (input.is('select')) {
                        input.find('option').each(function() {
                            if ($(this).text() === novedad[fieldName] || $(this).val() === novedad[fieldName]) {
                                $(this).prop('selected', true);
                                input.trigger('change');
                            }
                        });
                    } else {
                        input.val(novedad[fieldName]);
                    }
                }
            }
        });

        // Llamar el change handler para horasextra después de cargar los valores del formulario
        $('#id_horasextra').trigger('change');
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
        var tipoNovedad = novedad.tipoNovedad;
        cargarFormularioNovedad(tipoNovedad, novedad, index);
    });

    $('#guardarBtn').click(function() {
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        console.log(registros);
        enviarDatosASharePoint(registros);
    });

    function enviarDatosASharePoint(registros) {
        var data = registros.map(function(novedad) {
            var fields = {
                Title: novedad.nombre,
                Nombre: novedad.cedula,
                TipoNovedad: novedad.tipoNovedadText,
                Fecha: formatDate(novedad.fecha),
                Zona: novedad.zona || '',
                Detalle: novedad.observaciones || '',
                Ruta: novedad.ruta || '',
                Fecha_ingreso_Odoo: formatDate(novedad.fecha_ingreso),
                Reemplaza: novedad.reemplaza || '',
                Hora_llegada: novedad.hora_llegada || '',
                Fecha_inicio: formatDate(novedad.fecha_inicio),
                Fecha_fin: formatDate(novedad.fecha_fin),
                Colaborador: novedad.colaborador || '',
                Zona_reemplaza: novedad.zona_reemplaza || '',
                Motivo: novedad.motivo || '',
                Horas_extra: novedad.horasextra || '',
                Hora_inicio: novedad.hora_inicio || '',
                Hora_fin: novedad.hora_fin || '',
                Fecha_inicial: formatDate(novedad.fecha_inicial),
                Fecha_final: formatDate(novedad.fecha_final),
                Tipo_licencia: novedad.tipo_licencia || '',
                Tipo_permiso: novedad.tipo_permiso || '',
                Tipo_incapacidad: novedad.tipo_incapacidad || '',
                Control: novedad.control || '',
                Nuevo_control: novedad.nuevo_control || '',
                Tipo_servicio: novedad.tipo_servicio || '',
                Zona_inicial: novedad.zona_inicial || '',
                Novedad_extratemporanea: novedad.novedad_extemporanea || '',
                Consecutivo_servicio_Adcional: novedad.consecutivo || ''
            };

            Object.keys(fields).forEach(key => {
                if (fields[key] === '' || fields[key] === null) {
                    delete fields[key];
                }
            });

            return { fields };
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

    function formatDate(dateStr) {
        if (!dateStr) return '';
        var date = new Date(dateStr);
        return date.toISOString();
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
            var validTypesAusencias = ['opcion1', 'opcion2', 'opcion7', 'opcion9', 'opcion10', 'opcion11', 'opcion21', 'opcion22'];
            var validTypesIngresosRetiros = ['opcion8', 'opcion12', 'opcion17', 'opcion18'];
            var validTypesOperativos = ['opcion3', 'opcion4', 'opcion6', 'opcion16', 'opcion19', 'opcion20'];
            var validTypesPersonal = ['opcion5', 'opcion13', 'opcion14', 'opcion15'];

            if (validTypesAusencias.includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableAusencias';
            } else if (validTypesIngresosRetiros.includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableIngresosRetiros';
            } else if (validTypesOperativos.includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTableOperativos';
            } else if (validTypesPersonal.includes(novedad.tipoNovedad)) {
                tableId = '#novedadesTablePersonal';
            }

            agregarRegistroATabla(novedad, index, tableId);
        });
    }

    function agregarRegistroATabla(novedad, index, tableId) {
        var newRow = '<tr data-index="' + index + '">';

        newRow += '<td>' + (novedad.nombre || '') + '</td>';
        newRow += '<td>' + (novedad.cedula || '') + '</td>';
        newRow += '<td>' + (novedad.observaciones || '') + '</td>';
        newRow += '<td>' + (novedad.zona || '') + '</td>';
        newRow += '<td>' + (novedad.tipoNovedadText || '') + '</td>';
        newRow += '<td>' + (novedad.novedad_extemporanea || '') + '</td>';

        if (tableId === '#novedadesTableAusencias') {
            newRow += '<td>' + (novedad.rutas || '') + '</td>';
            newRow += '<td>' + (novedad.reemplaza || '') + '</td>';
            newRow += '<td>' + (novedad.colaborador || '') + '</td>';
            newRow += '<td>' + (novedad.horasextra || '') + '</td>';
            newRow += '<td>' + (novedad.hora_inicio || '') + '</td>';
            newRow += '<td>' + (novedad.hora_fin || '') + '</td>';
            newRow += '<td>' + (novedad.fecha_inicial || '') + '</td>';
            newRow += '<td>' + (novedad.fecha_final || '') + '</td>';
            newRow += '<td>' + (novedad.fecha || '') + '</td>';
            newRow += '<td>' + (novedad.tipos_licencia || '') + '</td>';
            newRow += '<td>' + (novedad.tipo_permisos || '') + '</td>';
            newRow += '<td>' + (novedad.tipo_incapacidad || '') + '</td>';
        } else if (tableId === '#novedadesTableIngresosRetiros') {
            newRow += '<td>' + (novedad.fecha_ingreso || '') + '</td>';
            newRow += '<td>' + (novedad.fecha_inicio || '') + '</td>';
            newRow += '<td>' + (novedad.fecha_fin || '') + '</td>';
            newRow += '<td>' + (novedad.motivo || '') + '</td>';
            newRow += '<td>' + (novedad.fecha || '') + '</td>';
            newRow += '<td>' + (novedad.rutas || '') + '</td>';
            newRow += '<td>' + (novedad.horasextra || '') + '</td>';
            newRow += '<td>' + (novedad.hora_inicio || '') + '</td>';
            newRow += '<td>' + (novedad.hora_fin || '') + '</td>';
            newRow += '<td>' + (novedad.zona_reemplaza || '') + '</td>';
        } else if (tableId === '#novedadesTableOperativos') {
            newRow += '<td>' + (novedad.consecutivo || '') + '</td>';
            newRow += '<td>' + (novedad.reemplaza || '') + '</td>';
            newRow += '<td>' + (novedad.colaborador || '') + '</td>';
            newRow += '<td>' + (novedad.zona_reemplaza || '') + '</td>';
            newRow += '<td>' + (novedad.horasextra || '') + '</td>';
            newRow += '<td>' + (novedad.hora_inicio || '') + '</td>';
            newRow += '<td>' + (novedad.hora_fin || '') + '</td>';
            newRow += '<td>' + (novedad.ruta || '') + '</td>';
            newRow += '<td>' + (novedad.zona_inicial || '') + '</td>';
            newRow += '<td>' + (novedad.control || '') + '</td>';
            newRow += '<td>' + (novedad.nuevo_control || '') + '</td>';
            newRow += '<td>' + (novedad.tipo_servicio || '') + '</td>';
            newRow += '<td>' + (novedad.fecha || '') + '</td>';
        } else if (tableId === '#novedadesTablePersonal') {
            newRow += '<td>' + (novedad.hora_llegada || '') + '</td>';
            newRow += '<td>' + (novedad.fecha || '') + '</td>';
        }

        newRow += '<td><button class="btn btn-warning btn-sm edit">Editar</button><button class="btn btn-danger btn-sm delete">Eliminar</button></td>';
        newRow += '</tr>';

        $(tableId).append(newRow);
    }

    cargarRegistrosLocales();
});
