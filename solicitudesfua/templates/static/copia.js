$(document).ready(function() {
    cargarRegistrosLocales();
    $('#abrirModal').on('click', function() {
        $('#novedadModal').modal('show');
    });

    var personasData = [];  // Variable global para almacenar los datos de las personas

    $('#novedadModal').on('shown.bs.modal', function () {
        $.ajax({
            url: '/api/personas/',
            type: 'GET',
            success: function(data) {
                personasData = data;  // Almacena los datos en la variable global
                var $select = $('#id_persona');
                $select.empty();
                data.forEach(function(persona) {
                    $select.append(new Option(persona.id, persona.nombre));  // Asegúrate de que 'nombre' e 'id' son correctos
                });
                $select.select2({
                    dropdownParent: $('#novedadModal'),
                    placeholder: "Seleccione una persona",
                    allowClear: true,
                    width: '100%'
                });
            },
            error: function() {
                alert('Error al cargar datos');
            }
        });
    });


    $(document).on('click', '.delete', function() {
        var index = $(this).closest('tr').data('index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        registros.splice(index, 1);
        guardarRegistrosLocales(registros); 
        $('#novedadesTable').empty();
        cargarRegistrosLocales();  // Recargar la tabla completa para reflejar los cambios
    });

    $(document).on('click', '.edit', function() {
        var index = $(this).closest('tr').data('index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        var novedad = registros[index];

        if (novedad) {
            $('#id_persona').val(novedad.persona).trigger('change');
            $('#id_tipo_novedad').val(novedad.tipoNovedad);
            $('#id_fecha').val(novedad.fecha);
            $('#novedadModal').data('edit-index', index).modal('show');
        }
    });

    function guardarRegistrosLocales(registros) {
        localStorage.setItem('registros', JSON.stringify(registros));
    }

    function cargarRegistrosLocales() {
        var registros = JSON.parse(localStorage.getItem('registros')) || [];
        $('#novedadesTable').empty();
        registros.forEach(function(novedad, index) {
            agregarRegistroATabla(novedad, index);
        });
    }

    function agregarRegistroATabla(novedad, index) {
        var newRow = `<tr data-index="${index}">
                        <td>${novedad.nombre}</td>
                        <td>${novedad.persona}</td>
                        <td>${novedad.tipoNovedad}</td>
                        <td>${novedad.fecha}</td>
                        <td>${novedad.zona}</td>
                        <td>
                            <button class="btn btn-warning btn-sm edit">Editar</button>
                            <button class="btn btn-danger btn-sm delete">Eliminar</button>
                        </td>
                    </tr>`;
        $('#novedadesTable').append(newRow);
    }

    $('#novedadForm').submit(function(event) {
        event.preventDefault();
        var index = $('#novedadModal').data('edit-index');
        var registros = JSON.parse(localStorage.getItem('registros')) || [];

        var selectedId = $('#id_persona').val();
        var selectedPersona = personasData.find(p => p.id === selectedId);
        if (!selectedPersona) {
            alert('Por favor, seleccione una persona.');
            return;
        }

        var tipoNovedad = $('#id_tipo_novedad').val();
        var fecha = $('#id_fecha').val();
        if (!fecha) {
            alert('Por favor, introduzca la fecha.');
            return;
        }

        var novedad = {
            nombre: selectedPersona.nombre,
            persona: selectedPersona.id,
            tipoNovedad: tipoNovedad,
            fecha: fecha,
            zona: selectedPersona.zona
        };

        if (index >= 0) {
            registros[index] = novedad;
        } else {
            registros.push(novedad);
        }

        guardarRegistrosLocales(registros);
        $('#novedadesTable').empty();
        cargarRegistrosLocales();
        $('#novedadModal').modal('hide').removeData('edit-index');
    });
});