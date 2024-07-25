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

                // Adjuntar evento submit al nuevo formulario cargado
                $('#novedadForm').off('submit').on('submit', function(event) {
                    event.preventDefault();
                    guardarNovedad();
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
        var tipoNovedad = $('#tipoNovedadSelect').val(); // Obtener tipo de novedad del select
        var index = $('#novedadModal').data('edit-index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];

        // Obtener la persona seleccionada
        var selectedOption = form.find('#id_Persona option:selected');
        var selectedId = selectedOption.val();
        var selectedText = selectedOption.text();
        var selectedPersona = selectedText.split(' - ');

        console.log('Selected ID:', selectedId);
        console.log('Selected Persona:', selectedPersona);

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
            zona: zona
        };

        // Agrega solo los campos relevantes según el tipo de novedad
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

        // Validar y agregar a la tabla correspondiente
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

        // Cargar el tipo de novedad en el select
        $('#tipoNovedadSelect').val(novedad.tipoNovedad).trigger('change');

        // Cargar los valores específicos según el tipo de novedad
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
                TipoNovedad: novedad.tipoNovedadText || '',
                Detalle: novedad.observaciones || '',
                Zona: novedad.zona || '',
                Ruta: novedad.ruta || '',
                Fecha_ingreso_Odoo: formatDate(novedad.fecha_ingreso_odoo),
                Reemplaza: novedad.reemplaza || '',
                Hora_llegada: novedad.hora_llegada || '',
                Fecha_inicio: formatDate(novedad.fecha_inicio),
                Fecha_fin: formatDate(novedad.fecha_fin),
                Colaborador: novedad.colaborador || '',
                Zona_reemplaza: novedad.zona_reemplaza || '',
                Motivo: novedad.motivo || '',
                Horas_extra: novedad.horas_extra || '',
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
                Fecha: formatDate(novedad.fecha),
                Zona_inicial: novedad.zona_inicial || ''
            };
    
            // Eliminar campos vacíos
            Object.keys(fields).forEach(key => {
                if (fields[key] === '') {
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
    
        // Campos comunes para todas las tablas
        newRow += '<td>' + (novedad.nombre || '') + '</td>';
        newRow += '<td>' + (novedad.cedula || '') + '</td>';
        newRow += '<td>' + (novedad.observaciones || '') + '</td>';
        newRow += '<td>' + (novedad.zona || '') + '</td>';
        newRow += '<td>' + (novedad.tipoNovedadText || '') + '</td>';
    
        // Campos específicos para cada tipo de novedad
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
            newRow += '<td>' + (novedad.fecha_ingreso_odoo || '') + '</td>';
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
        }
    
        newRow += '<td class="actions-btns"><button class="edit"><i class="bi bi-pencil-square"></i></button><button class="delete"><i class="bi bi-trash"></i></button></td>';
        newRow += '</tr>';
    
        $(tableId).append(newRow);
    }

    cargarRegistrosLocales();
});
