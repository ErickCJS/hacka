from utils.database import obtenerconexion as obtener_conexion

# ==========================================

def crear_denuncia_carro(id_incidencia, placa, color, tipo_vehiculo, descripcion, fecha_registro, estado):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
        INSERT INTO denuncia_vehiculo (id_incidencia, placa, color, tipo_vehiculo, descripcion, fecha_registro, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (id_incidencia, placa, color, tipo_vehiculo, descripcion, fecha_registro, estado))
        conexion.commit()
        conexion.close()

        print(f"[BD] Denuncia de carro creada: {id_incidencia} - {placa}")

    except Exception as e:
        print("[ERROR al crear denuncia de carro]", e)

def validar_id_denuncia(id_denuncia):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Ajusta la consulta para verificar si el ID existe
        sql = "SELECT id_denuncia from incidencia WHERE id_incidencia = %s"
        cursor.execute(sql, (id_denuncia,))
        resultado = cursor.fetchone()
        conexion.close()
        
        # Si se encuentra el resultado, devuelve el id_denuncia
        return resultado['id_denuncia'] if resultado else None  # Retorna el id_denuncia o None
    
    except Exception as e:
        print("[ERROR al validar id_denuncia]", e)
        return None

    
def obtener_denuncia_carro(id_denuncia):
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT * FROM denuncia_vehiculo WHERE id_incidencia = %s"
        cursor.execute(sql, (id_denuncia,))
        resultado = cursor.fetchone()
        conexion.close()
        
        return resultado
    
    except Exception as e:
        print("[ERROR al obtener denuncia de carro]", e)
        return None