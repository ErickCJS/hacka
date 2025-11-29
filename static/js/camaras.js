
const token ="pk.eyJ1IjoiZXJpY2tqcyIsImEiOiJjbWlqZ211anIwZ3MwM2ZxM2pweTNqNmNzIn0.vvgiQfkQ74kQMtkjOxfNQg"; 
mapboxgl.accessToken = token;

mapboxgl.config.API_URL = 'https://api.mapbox.com';
mapboxgl.config.FETCH_WITH_CREDENTIALS = false;
mapboxgl.config.DISABLE_TELEMETRY = true;

//modal
const modal_registro = new bootstrap.Modal(document.getElementById('modalCamara'));
const camNombre = document.getElementById('camNombre');
const camUrl = document.getElementById('camUrl');
const camLat = document.getElementById('camLat');
const camLng = document.getElementById('camLng');
const nomCalle = document.getElementById('nomCalle');
const btn_cam = document.getElementById('guardarCamara');
const tituloModal = document.getElementById('titl_md');
const btn_txt = document.getElementById('btn_txt');
const camiId = document.getElementById('camiId');
// Crear mapa centrado en Chiclayo
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v12',
    center: [-79.8387, -6.7714], // Chiclayo
    zoom: 13
});



map.on('click', async (e) => {
    const lng = e.lngLat.lng;
    const lat = e.lngLat.lat;
    limpiar_campos_form();
    modal_registro.show();
    camLat.value = lat;
    camLng.value = lng;
    tituloModal.textContent = "Registrar cámara";
    btn_cam.classList.remove('btn-warning');
    btn_cam.classList.add('btn-primary');
    btn_txt.textContent = "Registrar";
    btn_cam.onclick = registrar_camara;
    document.getElementById('estado_activo').checked = true;
    camiId.disabled = false;
    nomCalle.value = await obtener_sector(lng, lat);
});


const limpiar_campos_form = () =>{
    camNombre.value = "";
    camUrl.value = "";
    camLat.value = "";
    camLng.value = "";
    nomCalle.value = "";
    camiId.value = "";
}

map.on("load", () => {

  const capas = map.getStyle().layers;

  capas.forEach(layer => {
    // Oculta Puntos de Interés generales (tiendas, negocios, etc.)
    if (layer.id.includes("poi")) {
      map.setLayoutProperty(layer.id, "visibility", "none");
    }

    // Oculta gasolineras y estaciones (fuel)
    if (layer.id.includes("fuel")) {
      map.setLayoutProperty(layer.id, "visibility", "none");
    }

    // Oculta restaurantes, cafés, comida
    if (layer.id.includes("food")) {
      map.setLayoutProperty(layer.id, "visibility", "none");
    }

    // Oculta comercio (shopping)
    if (layer.id.includes("shop")) {
      map.setLayoutProperty(layer.id, "visibility", "none");
    }

    // Oculta transporte (si no lo quieres)
    if (layer.id.includes("transit")) {
      map.setLayoutProperty(layer.id, "visibility", "none");
    }
  });

});


const obtener_sector = async(longitud, latitud) =>{
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${longitud},${latitud}.json?access_token=${token}`;
    const res = await fetch(url);
    const data = await res.json();
    if (data.features.length > 0) {
        const direccion = data.features[0].place_name;
        return direccion;
    } else {
        return 'no hay';
    }
}



function crearMarkerCamara(cam) {
  const el = document.createElement("div");
  el.innerHTML = `<i class="bi bi-camera-video-fill"></i>`;
  el.style.fontSize = "30px";
  el.style.color = cam.estado === 'A' ? "#007bff" : "#dc3545";
  el.style.cursor = "pointer";

  // Evento si quieres mostrar info o abrir modal
  el.addEventListener("click", (event) => {
    event.stopPropagation();
    modal_registro.show();
    camNombre.value = cam.nombre_camara;
    camUrl.value = cam.url_camara;
    camLat.value = cam.latitud;
    camLng.value = cam.longitud;
    nomCalle.value = cam.calle;
    camiId.value = cam.id_camara;
    document.getElementById('estado_activo').checked = cam.estado === 'A';
    document.getElementById('estado_inactivo').checked = cam.estado !== 'A';
    tituloModal.textContent = "Modificar cámara";
    btn_cam.classList.remove('btn-primary');
    btn_cam.classList.add('btn-warning');
    btn_txt.textContent = "Modificar";
    camiId.disabled = true;
    btn_cam.onclick = modificar_camara;
  });

  new mapboxgl.Marker({ element: el })
    .setLngLat([cam.longitud, cam.latitud])
    .addTo(map);
}

console.log("CAMARAS:", camaras);
console.log("TIPO:", typeof camaras);

camaras.forEach(cam => crearMarkerCamara(cam));




const validar_registro = () => {
    const nombre = camNombre.value.trim();
    const url = camUrl.value.trim();
    const id = camiId.value.trim();
    const lat = camLat.value.trim();
    const lng = camLng.value.trim();
    
    const errores = [];
    
    if (nombre.length < 5) {
        errores.push("El nombre debe tener al menos 5 caracteres");
    }
    if (url.length < 12) {
        errores.push("La URL debe tener al menos 12 caracteres");
    }
    if (id.length < 3) {
        errores.push("El ID debe tener al menos 3 caracteres");
    }
    if (!lat || !lng) {
        errores.push("Debes seleccionar una ubicación en el mapa");
    }
    
    if (errores.length > 0) {
        alert(errores.join("\n"));
        return false;
    }
    
    return true;
};
const registrar_camara = async() =>{
  const estado = validar_registro();
  if(!estado){
    return;
  }
  const datos = {
    id_camara: camiId.value,
    nombre_camara: camNombre.value,
    url_camara: camUrl.value,
    latitud: camLat.value,
    longitud: camLng.value,
    calle: nomCalle.value,
    estado: document.getElementById('estado_activo').checked
  }
  const ruta = "http://127.0.0.1:5000/api/camaras/crear";
  const resp = await fetch(ruta, {
    method: 'POST',
    headers: {
    'Content-Type': 'application/json'
    },
    body: JSON.stringify(datos)
  });
  const data = await resp.json(); 
  if(data.code == 1){
    window.location.reload();
  } else {
    alert(data.error);
  }
}


const modificar_camara = async() => {
  const estado = validar_registro();
  if(!estado){
    return;
  }
  const datos = {
    nombre_camara: camNombre.value,
    url_camara: camUrl.value,
    latitud: camLat.value,
    longitud: camLng.value,
    calle: nomCalle.value,
    estado: document.getElementById('estado_activo').checked
  }
  const ruta = `http://127.0.0.1:5000/api/camaras/actualizar/${camiId.value}`;
  const resp = await fetch(ruta, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(datos)
  });
  const data = await resp.json(); 
  if(data.code == 1){
    window.location.reload();
  } else {
    alert(data.error);
  }

}

const seleccionar_camara = (longitud, latitud) => {
  map.flyTo({
    center: [longitud, latitud],
    zoom: 17
  });
}

document.getElementById('buscar').addEventListener('input', function(e){
  const q = e.target.value.trim().toLowerCase();
  const tarjetas = document.querySelectorAll('.lista_camaras .card');
  let visibleCount = 0;

  tarjetas.forEach(card => {
    const nombre_ca = (card.querySelector('.n_camar')?.textContent || '').toLowerCase();
    const nom_calle = (card.querySelector('.n_call')?.textContent || '').toLowerCase();
    const match = q === '' || nombre_ca.includes(q) || nom_calle.includes(q);

    card.style.display = match ? '' : 'none';
    if (match) visibleCount++;
  });

  if (visibleCount === 1) {
    const card = Array.from(tarjetas).find(c => c.style.display !== 'none');
    if (card && card.dataset.lat && card.dataset.lng) {
      seleccionar_camara(parseFloat(card.dataset.lng), parseFloat(card.dataset.lat));
    }
  }
});

