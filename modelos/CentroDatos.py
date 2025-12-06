from TDAs.ListaEnlazada import ListaEnlazada
from modelos.Recursos import Recursos

class CentroDatos:
    def __init__(self, id_centro, nombre, pais, ciudad, capacidad, cpu, ram, almacenamiento):
        self.id_centro = id_centro
        self.nombre = nombre
        self.pais = pais
        self.ciudad = ciudad
        self.capacidad = int(capacidad)
        self.recursos = Recursos(cpu, ram, almacenamiento)
        self.maquinas_virtuales = ListaEnlazada()

    def crear_vm(self, id_vm, sistema_operativo, ip, cpu_requerido, ram_requerido, almacenamiento_requerido):
        from modelos.MaquinaVirtual import MaquinaVirtual
        
        cpu_req = int(cpu_requerido)
        ram_req = int(ram_requerido)
        alm_req = int(almacenamiento_requerido)
        
        if cpu_req > self.recursos.obtener_cpu_disponible():
            return False, f"CPU insuficiente. Disponible: {self.recursos.obtener_cpu_disponible()} nucleos, Requerido: {cpu_req} nucleos"
        
        if ram_req > self.recursos.obtener_ram_disponible():
            return False, f"RAM insuficiente. Disponible: {self.recursos.obtener_ram_disponible()} GB, Requerido: {ram_req} GB"
        
        if alm_req > self.recursos.obtener_almacenamiento_disponible():
            return False, f"Almacenamiento insuficiente. Disponible: {self.recursos.obtener_almacenamiento_disponible()} GB, Requerido: {alm_req} GB"
        
        nueva_vm = MaquinaVirtual(id_vm, self.id_centro, sistema_operativo, ip, cpu_req, ram_req, alm_req)
        self.maquinas_virtuales.insertar(nueva_vm)
        
        self.recursos.asignar_recursos(cpu_req, ram_req, alm_req)
        
        return True, f"VM {id_vm} creada exitosamente en {self.nombre}"

    def __str__(self):
        return f"{self.id_centro} - {self.nombre} - {self.pais}, {self.ciudad} - Capacidad: {self.capacidad} VMs - {self.recursos}"