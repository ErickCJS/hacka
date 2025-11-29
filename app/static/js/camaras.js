
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
    btn_txt.textContent = "Registrar"
    document.getElementById('estado_activo').checked = true;
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
        console.log("No se encontró dirección.");
        return 'no hay';
    }
}

const camaras = [
  {
    nombre: "Cámara Plaza",
    lat: -6.762009988475043,
    lng: -79.85986840700068,
    url : 'asdasd',
    calle: "asdkasdasd"
  },
  {
    nombre: "Cámara Elías Aguirre",
    lat: -6.7711,
    lng: -79.8402,
    url: "sdasdasd",
    calle : "adasdasd"
  },
  {
    nombre: "Cámara Real Plaza",
    lat: -6.7765,
    lng: -79.8644,
    url: "asdknasd",
    calle: "adasdasd"
  }
];

function crearMarkerCamara(cam) {
  const el = document.createElement("div");
  el.innerHTML = `<i class="bi bi-camera-video-fill"></i>`;
  el.style.fontSize = "30px";
  el.style.color = "#007bff";
  el.style.cursor = "pointer";

  // Evento si quieres mostrar info o abrir modal
  el.addEventListener("click", (event) => {
    event.stopPropagation();
    modal_registro.show();
    camNombre.value = cam.nombre;
    camUrl.value = cam.url;
    camLat.value = cam.lat;
    camLng.value = cam.lng;
    nomCalle.value = cam.calle;
    tituloModal.textContent = "Modificar cámara";
    btn_cam.classList.remove('btn-primary');
    btn_cam.classList.add('btn-warning');
    btn_txt.textContent = "Modificar";

  });

  new mapboxgl.Marker({ element: el })
    .setLngLat([cam.lng, cam.lat])
    .addTo(map);
}
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
    const ruta = "";
    const resp = await fetch(ruta);
    const data = resp.json();
    
}


const modificar_camara = () => {
    


}

