function cargarZonas() {
    $.ajax({
        url: '/api/zonas/',
        type: 'GET',
        success: function(data) {
            console.log('Zonas:', data); // Verificar datos en la consola
            var $select = $('#id_zona');
            $select.empty(); // Limpiar el select antes de agregar nuevas opciones
            $select.append($('<option>', {
                value: '',
                text: 'Seleccione una zona'
            })); // Opción por defecto
            data.forEach(function(zona) {
                if (zona) { // Verificar que la zona no esté vacía
                    $select.append($('<option>', { 
                        value: zona, 
                        text: zona 
                    }));
                }
            });
        },
        error: function() {
            console.error('Error al cargar los datos de las zonas');
        }
    });
}

function validarZona() {
    const selectedZona = document.getElementById('id_zona').value;
    const selectedRow = document.querySelector('tbody tr');
    const selectedNombre = selectedRow ? selectedRow.cells[1].innerText : ''; // Asumiendo que el nombre está en la segunda columna

    if (!selectedZona || !selectedNombre) {
        alert('Por favor, seleccione una zona y asegúrese de que el nombre esté disponible.');
        return;
    }
    // Validar si la zona seleccionada es diferente a la zona capturada en la tabla
    const capturedZona = selectedRow ? selectedRow.cells[2].innerText : ''; // La zona está en la tercera columna

    if (selectedZona !== capturedZona) {
        if (!confirm('La zona seleccionada es diferente a la zona capturada. ¿Está seguro que desea continuar?')) {
            return;
        }
    }

    // Redirigir con parámetros
    window.location.href = `/azure_auth/novedades/?zona=${selectedZona}&nombre=${selectedNombre}`;
}

$(document).ready(function() {
    cargarZonas();

    // Añadir evento click al botón
    $('#validarZonaBtn').click(validarZona);
});
