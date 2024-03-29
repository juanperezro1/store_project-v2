   
  $(function () {
    $('#dataTable').DataTable({
        responsive: true,
        autoWidth: false,
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
            { "data": "id" },
            { "data": "first_name" },
            { "data": "last_name" },
            { "data": "username" },
            { "data": "date_joined" },
            { "data": "botones" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var botones = '<a href="editar_producto/' + row.id_producto + '/" class="btn btn-warning btn-circle"><i class="fas fa-edit"></i></a>';
                    botones += '<a href="#" class="btn btn-danger btn-circle"><i class="fas fa-trash"></i></a>'
                    return botones
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
});