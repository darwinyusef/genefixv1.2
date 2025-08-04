/*
Estas funciones se encuentran deprecadas debido a que el cliente no las necesita
* y no se tiene claro si se se utilizarán en el futuro.
TODO se eliminan los API_KEY ya que lo que se pensaba inicialmente era cerrarlos por Back solo se uso en mvc
*/

// 🤓 Cuentas contables pasa a ser deprecado debido a solicitud del cliente ya que no es necesario

// const buscarCuenta = async () => {
//     const cuenta = document.getElementById('f_cuenta').value;
//     const nombre = document.getElementById('f_nombre').value;
//     // console.log(cuenta, nombre);
//     if (cuenta === "" && nombre === "") {
//         alert('Por favor, ingrese un valor para buscar');
//         return;
//     }

//     let url = `http://begranda.com/equilibrium2/public/api/account?eq-auxiliar=1&&key=${API_KEY}&`;

//     if (cuenta) {
//         url += `f-cuenta=${cuenta}&`;
//     }

//     if (nombre) {
//         url += `f-nombre=${nombre}`;
//     }

//     try {
//         const response = await fetch(url);
//         const data = await response.json();
//         if (data.status !== "success") {
//             alert('Error al buscar cuentas contables');
//             return;
//         }
//         mostrarResultadosCuenta(data.data);
//     } catch (error) {
//         console.error('Error en la búsqueda:', error);
//     }
// };

// const mostrarResultadosCuenta = (data) => {
//     const div = document.getElementById('resultadosCuenta');
//     div.innerHTML = '';

//     if (!data || Object.keys(data).length === 0) {
//         div.innerHTML = '<p>No se encontraron resultados.</p>';
//         return;
//     }

//     let tabla = '<table class="table table-hover">';
//     tabla += '<thead><tr><th>ID</th><th>Cuenta</th><th>Nombre</th><th>Acción</th></tr></thead><tbody>';

//     Object.values(data).forEach(item => {
//         console.log(item);
//         tabla += `
//             <tr>
//                 <td>${item.id}</td>
//                 <td>${item.cuenta}</td>
//                 <td class="infoCuenta">${item.nombre}</td>
//                 <td>
//                     <button class="btn btn-sm btn-primary" onclick="seleccionarCuenta(${item.id})">Agregar</button>
//                 </td>
//             </tr>
//         `;
//     });

//     tabla += '</tbody></table>';

//     div.innerHTML = tabla;
// };

// const seleccionarCuenta = (id) => {
//     document.getElementById('id_cuenta').value = id;
//     $('#modalBuscarCuenta').modal('hide');
// };


/**
 * 🤓 Debemos esperar a ver que es lo que sucede con la api de comprobantes pues ellos quieren poner solo cajas menores y aqui lo más parecido es egresos
 * @returns
 */



// const cargarComprobantes = async () => {
//     try {
//         const response = await fetch(`https://begranda.com/equilibrium2/public/api/proof?key=${API_KEY}`);
//         const result = await response.json();
//         // console.log(result);
//         const data = result.data; // Objeto con claves dinámicas "1", "2", "3"...

//         const select = document.getElementById('selectComprobantes');

//         // Limpiar select (por si vuelves a cargar)
//         select.innerHTML = '<option value="">Seleccione un comprobante</option>';

//         Object.keys(data).forEach(key => {
//             const item = data[key];

//             const option = document.createElement('option');
//             option.value = item.id;
//             option.text = `${item.codigo} - ${item.nombre}`;

//             select.appendChild(option);
//         });

//     } catch (error) {
//         console.error('Error al cargar comprobantes', error);
//     }
// }