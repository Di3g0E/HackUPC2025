let vuelosOriginales = [];

// 1) Cargo el JSON inicial
fetch("data/flights.json")
  .then(r => r.json())
  .then(data => {
    vuelosOriginales = data;
    mostrarVuelos(vuelosOriginales);
  })
  .catch(console.error);

// Función que pinta una lista de vuelos en la tabla
function mostrarVuelos(vuelos) {
  const table = document.getElementById("flights_table");
  table.innerHTML = "";
  vuelos.forEach(flight => {
    const row = document.createElement("tr");
    ["destination","departure","flight","terminal","status"].forEach(col => {
      const td = document.createElement("td");
      td.textContent = flight[col] || "---";
      row.appendChild(td);
    });
    table.appendChild(row);
  });
}

// 2) Buscador
document.getElementById("buscador").addEventListener("input", e => {
  const txt = e.target.value.toLowerCase();
  const filtrados = vuelosOriginales.filter(v =>
    Object.values(v).some(val =>
      typeof val === "string" && val.toLowerCase().includes(txt)
    )
  );
  mostrarVuelos(filtrados);
});

// 3) Al pulsar "receiver", traemos flights2.json y rellenamos huecos
document.getElementById("receiver").addEventListener("click", () => {
  fetch("data/flights2.json")
    .then(r => r.json())
    .then(completos => {
      // Creamos un mapa rápido de flight → objeto completo
      const mapaCompleto = completos.reduce((m, v) => {
        m[v.flight] = v;
        return m;
      }, {});
      // Para cada vuelo original, completamos los campos vacíos
      vuelosOriginales = vuelosOriginales.map(orig => ({
        ...orig,
        ...mapaCompleto[orig.flight]  // rellena sólo donde falte
      }));
      mostrarVuelos(vuelosOriginales);
    })
    .catch(err => console.error("No se cargaron flights2.json:", err));
});
