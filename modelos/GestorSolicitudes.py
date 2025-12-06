from TDAs.ColaPrioridad import ColaPrioridad
from modelos.Solicitud import Solicitud

class GestorSolicitudes:
    def __init__(self):
        self.cola_solicitudes = ColaPrioridad()
        self.historial = None

    def agregar_solicitud(self, id_solicitud, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo_estimado):
        if tipo not in ("Deploy", "Backup"):
            return False, f"Tipo de solicitud invalido: {tipo}. Debe ser 'Deploy' o 'Backup'"
        
        prioridad_num = int(prioridad)
        if prioridad_num < 1 or prioridad_num > 10:
            return False, f"Prioridad invalida: {prioridad}. Debe estar entre 1 y 10"
        
        nueva_solicitud = Solicitud(id_solicitud, cliente, tipo, prioridad_num, cpu, ram, almacenamiento, tiempo_estimado)
        self.cola_solicitudes.encolar(nueva_solicitud)
        
        return True, f"Solicitud {id_solicitud} agregada a la cola con prioridad {prioridad_num}"

    def procesar_siguiente_solicitud(self, lista_centros):
        if self.cola_solicitudes.esta_vacia():
            return False, "No hay solicitudes pendientes en la cola"
        
        solicitud = self.cola_solicitudes.desencolar()
        
        if solicitud.tipo == "Deploy":
            return self.procesar_deploy(solicitud, lista_centros)
        elif solicitud.tipo == "Backup":
            return self.procesar_backup(solicitud, lista_centros)
        
        return False, f"Tipo de solicitud desconocido: {solicitud.tipo}"

    def procesar_deploy(self, solicitud, lista_centros):
        centro_seleccionado = self.encontrar_centro_con_mas_recursos(lista_centros, solicitud.cpu, solicitud.ram, solicitud.almacenamiento)
        
        if centro_seleccionado is None:
            solicitud.estado = "Rechazada - Sin recursos"
            return False, f"Solicitud {solicitud.id_solicitud} rechazada. No hay centros con recursos suficientes"
        
        exito, mensaje = centro_seleccionado.crear_vm(
            solicitud.id_solicitud,
            "Sistema Automatico",
            "Auto-asignada",
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento
        )
        
        if exito:
            solicitud.estado = "Completada - Deploy"
            return True, f"Deploy exitoso: VM {solicitud.id_solicitud} creada en {centro_seleccionado.nombre}. Cliente: {solicitud.cliente}"
        else:
            solicitud.estado = "Rechazada - Error al crear VM"
            return False, f"Error en Deploy: {mensaje}"

    def procesar_backup(self, solicitud, lista_centros):
        centro_seleccionado = self.encontrar_centro_con_mas_recursos(lista_centros, solicitud.cpu, solicitud.ram, solicitud.almacenamiento)
        
        if centro_seleccionado is None:
            solicitud.estado = "Rechazada - Sin recursos"
            return False, f"Solicitud {solicitud.id_solicitud} rechazada. No hay centros con recursos suficientes"
        
        exito, mensaje = centro_seleccionado.crear_vm(
            f"{solicitud.id_solicitud}_BKP",
            "Sistema Backup - Suspendida",
            "Auto-asignada",
            solicitud.cpu,
            solicitud.ram,
            solicitud.almacenamiento
        )
        
        if exito:
            solicitud.estado = "Completada - Backup"
            return True, f"Backup exitoso: VM {solicitud.id_solicitud}_BKP creada en estado suspendido en {centro_seleccionado.nombre}. Cliente: {solicitud.cliente}"
        else:
            solicitud.estado = "Rechazada - Error al crear VM"
            return False, f"Error en Backup: {mensaje}"

    def encontrar_centro_con_mas_recursos(self, lista_centros, cpu_req, ram_req, alm_req):
        if lista_centros.primero is None:
            return None
        
        mejor_centro = None
        mejor_puntuacion = -1
        
        nodo_actual = lista_centros.primero
        while nodo_actual:
            centro = nodo_actual.dato
            
            cpu_disponible = centro.recursos.obtener_cpu_disponible()
            ram_disponible = centro.recursos.obtener_ram_disponible()
            alm_disponible = centro.recursos.obtener_almacenamiento_disponible()
            
            if cpu_disponible >= cpu_req and ram_disponible >= ram_req and alm_disponible >= alm_req:
                puntuacion = cpu_disponible + ram_disponible + alm_disponible
                
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    mejor_centro = centro
            
            nodo_actual = nodo_actual.siguiente
        
        return mejor_centro

    def ver_cola_solicitudes(self):
        if self.cola_solicitudes.esta_vacia():
            return "No hay solicitudes en la cola"
        
        return self.cola_solicitudes.mostrar_todas()

    def obtener_cantidad_pendientes(self):
        return self.cola_solicitudes.size
