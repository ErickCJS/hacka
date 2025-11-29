import cv2
import requests
import pymysql
import tempfile
import os
import time
import threading
from datetime import datetime

# ==========================================
# CONFIGURACIÓN
# ==========================================

PLATE_API_TOKEN = "e9a647ed3e7c27b05e6b391957164d01553b158f"

# DICCIONARIO DE CÁMARAS (id → URL)
# Usa shot.jpg porque IP Webcam responde más rápido
CAMARAS = {
    #1: "http://192.168.1.34:8080/shot.jpg",
    #2: "http://192.168.18.28:8080/shot.jpg",
    3: "http://192.168.1.34:8080/shot.jpg" ##cambian esto solo la parte de 192.168.1.34:8080 por el que les indica al instalar IP webcam 
}

RUNNING = True

ULTIMAS_PLACAS = {}
ANTI_DUP_SECONDS = 10

# ==========================================
# CONEXIÓN BD
# ==========================================

# def conectarbd():
#     try:
#         return pymysql.connect(
#             host='mysql-3e74c755-julonerick1-1f47.k.aivencloud.com',
#             user='avnadmin',
#             password='AVNS_sQSLY3fyNxJnuZ8zU_O',
#             database='hacka',
#             port=24299,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#     except Exception as e:
#         print("[ERROR BD]", e)
#         return None


# def guardar_captura(camara_id, placa):
#     try:
#         conn = conectarbd()
#         cursor = conn.cursor()

#         sql = """
#         INSERT INTO captura_placa (camara_id, placa_detectada, tiempo)
#         VALUES (%s, %s, NOW())
#         """

#         cursor.execute(sql, (camara_id, placa))
#         conn.commit()
#         conn.close()

#         print(f"[BD] Guardado: Camara {camara_id} - {placa}")

#     except Exception as e:
#         print("[ERROR al guardar captura]", e)

# ==========================================
# CAPTURA IMAGEN DESDE IP WEBCAM
# ==========================================

def capturar_imagen(camara_id, url):
    try:
        resp = requests.get(url, timeout=4)
        if resp.status_code != 200:
            print(f"[CAM {camara_id}] ERROR al obtener imagen")
            return None

        f = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        f.write(resp.content)
        f.close()
        return f.name

    except Exception as e:
        print(f"[CAM {camara_id}] Error conexión: {e}")
        return None

# ==========================================
# PROCESAR PLACA
# ==========================================


def procesar_placa(camara_id, img_path):
    global ULTIMAS_PLACAS

    url = "https://api.platerecognizer.com/v1/plate-reader/"

    with open(img_path, 'rb') as img:
        response = requests.post(
            url,
            files={"upload": img},
            headers={"Authorization": f"Token {PLATE_API_TOKEN}"},
            data={"camera_id": camara_id}
        )

    os.remove(img_path)
    data = response.json()

    if "results" not in data or not data["results"]:
        print(f"[CAM {camara_id}] No detectó placa")
        return

    placa = data["results"][0]["plate"].upper()
    confianza = data["results"][0]["score"] * 100

    if len(placa) != 6:
        print(f"[CAM {camara_id}] IGNORADO → {placa} ({confianza:.1f}%)")
        return

    ahora = time.time()
    key = (camara_id, placa)

    if key in ULTIMAS_PLACAS:
        if ahora - ULTIMAS_PLACAS[key] < ANTI_DUP_SECONDS:
            print(f"[CAM {camara_id}] Repetida → {placa} (ignorada)")
            return

    ULTIMAS_PLACAS[key] = ahora


    timestamp = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    
    print(f"[CAM {camara_id}] {timestamp} → PLACA DETECTADA: {placa} ({confianza:.1f}%)")
    #print(f"[CAM {camara_id}] PLACA DETECTADA: {placa} ({confianza:.1f}%)")

# ==========================================
# CICLO PARA CADA CÁMARA (HILO)
# ==========================================

def ciclo_camara(camara_id, url):
    print(f"[INICIO] Cámara {camara_id} activada → {url}")

    while RUNNING:
        img = capturar_imagen(camara_id, url)
        if img:
            procesar_placa(camara_id, img)
        time.sleep(1)

    print(f"[STOP] Cámara {camara_id} detenida.")

# ==========================================
# MULTICÁMARA – THREADS
# ==========================================

print("===== SISTEMA MULTICÁMARA ALPR =====")

hilos = []

for camara_id, url in CAMARAS.items():
    hilo = threading.Thread(target=ciclo_camara, args=(camara_id, url))
    hilo.start()
    hilos.append(hilo)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\n\n🛑 Deteniendo cámaras...")
    RUNNING = False

    for hilo in hilos:
        hilo.join()

    print("✔ Sistema detenido correctamente.")