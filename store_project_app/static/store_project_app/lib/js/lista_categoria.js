$(function () {
    $('#dataTable').DataTable({
        responsive: true,
        autoWidth: false,
        language: {
            url: '/static/store_project_app/vendor/datatables/spanish.txt'  
        },
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            { "data": "id_categoria" },
            { "data": "nombre" },
            { "data": "descripcion" },
            { "data": "botones" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var botones = '<a href="editar_categoria/' + row.id_categoria + '/" class="btn btn-warning btn-circle"><i class="fas fa-edit"></i></a> ';
                    botones += '<a href="eliminar_categoria/' + row.id_categoria + '/" class="btn btn-danger btn-circle"><i class="fas fa-trash"></i></a> ';
                    return botones
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});