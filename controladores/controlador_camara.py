from utils.database import obtenerconexion as obtener_conexion

# ==========================================
def crear_camara(id_camara, nombre_camara, url_camara, latitud, longitud, calle, 
                 estado ):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO camara (id_camara, nombre_camara, url_camara, latitud, longitud, calle, 
                             estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (id_camara, nombre_camara, url_camara, latitud, longitud, calle, 
                             estado))
        conexion.commit()
        conexion.close()

        print(f"[BD] Cámara creada: {id_camara} - {nombre_camara}")

    except Exception as e:
        print("[ERROR al crear cámara]", e)
        
# ==========================================

def listar_camara():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT * FROM camara"
        cursor.execute(sql)

        camara = cursor.fetchall()
        conexion.close()

        return camara

    except Exception as e:
        print("[ERROR al listar cámaras]", e)
        return []
# ==========================================

def actualizar_estado_camara(id_camara, nuevo_estado):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "UPDATE camara SET estado = %s WHERE id_camara = %s"
        cursor.execute(sql, (nuevo_estado, id_camara))

        conexion.commit()
        conexion.close()

        print(f"[BD] Cámara {id_camara} actualizada a estado: {nuevo_estado}")

    except Exception as e:
        print("[ERROR al actualizar estado de cámara]", e)
        


# ==========================================

def actualizar_camara(id_camara, nombre_camara, url_camara, latitud, longitud, calle, 
                     estado):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        UPDATE camara
        SET nombre_camara = %s,
            url_camara = %s,
            latitud = %s,
            longitud = %s,
            calle = %s,
            estado = %s
        WHERE id_camara = %s
        """

        cursor.execute(sql, (nombre_camara, url_camara, latitud, longitud, calle, 
                             estado, id_camara))
        conexion.commit()
        conexion.close()

        print(f"[BD] Cámara actualizada: {id_camara} - {nombre_camara}")

    except Exception as e:
        print("[ERROR al actualizar cámara]", e
                )