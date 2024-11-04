let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [0, 5, 6] }
    ],
    pageLength: 4,
    destroy: true
};

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listarproductos();

    dataTable = $("#datatable-productos").DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listarproductos = async () => {
    try {
        const response = await fetch("http://127.0.0.1:8000/productos/listar/");
        const data = await response.json();

        let content = ``;
        data.productos.forEach((productos, index) => {
            content += `
                <tr>
                    <td>${productos.Fecha  }</td>
                    <td>${productos.codigo_qr }</td>
                    <td>${productos.Creador }</td>
                    <td>${productos.Precio }</td>
                    <td>${productos.Stock }</td>
                    <td>${productos.Marca }</td>
                    <td>${productos.Categoría }</td>
                    <td>${productos.Imagen }</td>
                    
                    <td>${productos.score >= 10
                        ? "<i class='fa-solid fa-check' style='color: green;'></i>" 
                        : "<i class='fa-solid fa-xmark' style='color: red;'></i>"}
                    </td>
                    <td>
                        <button class='btn btn-sm btn-primary'><i class='fa-solid fa-pencil'></i></button>
                        <button class='btn btn-sm btn-danger'><i class='fa-solid fa-trash-can'></i></button>
                    </td>
                </tr>`;
        });
        tableBody_productos.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener("load", async () => {
    await initDataTable();
});