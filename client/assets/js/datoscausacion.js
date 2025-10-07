
const user_fin = JSON.parse(localStorage.getItem("user"))
const API_URL = `https://begranda.com/equilibrium2/public/api/account?eq-auxiliar=1&key=${user_fin.begranda_app}`;

let finalCajas = [];

const cajas = [
    { "codigo": "11051001", "nombre": "CAJA MENOR VALLEDUPAR" },
    { "codigo": "11051002", "nombre": "CAJA MENOR BOYACA" },
    { "codigo": "11051003", "nombre": "CAJA MENOR MEDELLIN" },
    { "codigo": "11051004", "nombre": "CAJA MENOR SUCRE" },
    { "codigo": "11051005", "nombre": "CAJA MENOR BUCARAMANGA" },
    { "codigo": "11051006", "nombre": "CAJA MENOR VILLAVICENCIO" }
];

async function cargarCuentasCache() {
    const cache = localStorage.getItem("cuentas_cache");
    if (cache) {
        try {
            return JSON.parse(cache);
        } catch (err) {
            console.warn("⚠️ Cache corrupto, recargando...", err);
            localStorage.removeItem("cuentas_cache");
        }
    }

    try {
        const response = await fetch(API_URL);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();

        const cuentas = Array.isArray(data.data) ? data.data : Object.values(data.data);
        localStorage.setItem("cuentas_cache", JSON.stringify(cuentas));

        return cuentas;
    } catch (error) {
        console.error("❌ Error al cargar cuentas:", error);
        return [];
    }
}

async function validarCajas(cajas, cuentas) {
    const cuentasSet = new Set(cuentas.map(c => c.cuenta)); // búsqueda rápida
    const resultado = cajas.map(caja => {
        const existe = cuentasSet.has(caja.codigo);
        if (!existe) {
            console.log(`⚠️ El código ${caja.codigo} (${caja.nombre}) no existe en el sistema.`);
        }
        return { ...caja, existe };
    });

    return resultado;
}

(async () => {
    const cuentas = await cargarCuentasCache();
    finalCajas = await validarCajas(cajas, cuentas);

    // CÓDIGO CON console.table()
    console.warn("✅ Resultado final:");
    console.table(finalCajas);
})();
