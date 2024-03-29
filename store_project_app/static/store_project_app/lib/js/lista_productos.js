
$(function () {
    var tblproductos = $('#dataTable').DataTable({
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
            { "data": "id_producto" },
            { "data": "nombre" },
            { "data": "categoria.nombre" },
            { "data": "stock" },
            { "data": "precio" },
            { "data": "fecha_vencimiento" },
            { "data": "botones" },
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var botones = '<a href="editar_producto/' + row.id_producto + '/" class="btn btn-warning btn-circle"><i class="fas fa-edit"></i></a> ';
                    botones += '<a href="eliminar_producto/' + row.id_producto + '/" class="btn btn-danger btn-circle"><i class="fas fa-trash"></i></a> ';
                    return botones
                },
            },

            // {
            //     targets: [-2],
            //     class: 'text-center',
            //     orderable: false,
            //     render: function (data, type, row) {
            //         var now = moment().format('YYYY-MM-DD');
            //         var date = moment(data).format('YYYY-MM-DD');
                    
            //         console.log(typeof(now));
            //         console.log(typeof(date));
                    
            //         // console.log("otra");
            //         // console.log(typeof(date));
            //         // console.log(date);
            //         // console.log("ope")
            //         // console.log(date - now)
                   
            //         // var operacion = now -parseDate
            //         // var dias = (Math.round(operacion/ (1000*60*60*24)))
                   
            //         return now
            //     }, 
            // },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var now = moment().format('YYYY-MM-DD');
                   
                    return '$' + parseFloat(data).toFixed(0);
                }, 
            },

            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (data > 10) {
                        return '<span class="badge badge-success">' + data + '</span>'
                    }
                    if (data > 5 && data <= 10) {
                        return '<span class="badge badge-warning">' + data + '</span>'
                    }
                    return '<span class="badge badge-danger">' + data + '</span>'

                },
            },


        ],
        initComplete: function (settings, json) {
        }
    });
});