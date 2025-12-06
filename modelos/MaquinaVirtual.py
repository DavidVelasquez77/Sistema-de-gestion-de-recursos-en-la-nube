from modelos.Recursos import Recursos
from TDAs.ListaEnlazada import ListaEnlazada

class MaquinaVirtual:
    def __init__(self, id_vm, centro_asignado, sistema_operativo, ip, cpu, ram, almacenamiento):
        self.id_vm = id_vm
        self.centro_asignado = centro_asignado
        self.sistema_operativo = sistema_operativo
        self.ip = ip
        self.recursos = Recursos(cpu, ram, almacenamiento)
        self.contenedores = ListaEnlazada()
        self.cpu_porcentaje_usado = 0.0
        self.ram_mb_usado = 0

    def obtener_cpu_disponible_porcentaje(self):
        return 100.0 - self.cpu_porcentaje_usado

    def obtener_ram_disponible_mb(self):
        ram_total_mb = self.recursos.ram_total * 1024
        return ram_total_mb - self.ram_mb_usado

    def agregar_contenedor(self, id_contenedor, nombre, imagen, puerto, cpu_porcentaje, ram_mb):
        from modelos.Contenedor import Contenedor
        
        cpu_porc = float(cpu_porcentaje)
        ram_megabytes = int(ram_mb)
        
        if cpu_porc > self.obtener_cpu_disponible_porcentaje():
            return False, f"CPU insuficiente. Disponible: {self.obtener_cpu_disponible_porcentaje():.2f}%, Requerido: {cpu_porc}%"
        
        if ram_megabytes > self.obtener_ram_disponible_mb():
            return False, f"RAM insuficiente. Disponible: {self.obtener_ram_disponible_mb()} MB, Requerido: {ram_megabytes} MB"
        
        nuevo_contenedor = Contenedor(id_contenedor, nombre, imagen, puerto, cpu_porc, ram_megabytes)
        self.contenedores.insertar(nuevo_contenedor)
        
        self.cpu_porcentaje_usado += cpu_porc
        self.ram_mb_usado += ram_megabytes
        
        return True, f"Contenedor {id_contenedor} agregado exitosamente a VM {self.id_vm}"

    def eliminar_contenedor(self, id_contenedor):
        nodo_actual = self.contenedores.primero
        nodo_anterior = None
        
        while nodo_actual:
            if nodo_actual.dato.id_contenedor == id_contenedor:
                contenedor = nodo_actual.dato
                
                self.cpu_porcentaje_usado -= contenedor.cpu_porcentaje
                self.ram_mb_usado -= contenedor.ram_mb
                
                if self.cpu_porcentaje_usado < 0:
                    self.cpu_porcentaje_usado = 0.0
                if self.ram_mb_usado < 0:
                    self.ram_mb_usado = 0
                
                if nodo_anterior is None:
                    self.contenedores.primero = nodo_actual.siguiente
                else:
                    nodo_anterior.siguiente = nodo_actual.siguiente
                
                return True, f"Contenedor {id_contenedor} eliminado exitosamente. CPU liberada: {contenedor.cpu_porcentaje}%, RAM liberada: {contenedor.ram_mb} MB"
            
            nodo_anterior = nodo_actual
            nodo_actual = nodo_actual.siguiente
        
        return False, f"Contenedor {id_contenedor} no encontrado en VM {self.id_vm}"

    def __str__(self):
        ram_total_mb = self.recursos.ram_total * 1024
        return f"VM {self.id_vm} - SO: {self.sistema_operativo} - IP: {self.ip} - CPU Contenedores: {self.cpu_porcentaje_usado:.2f}%/100% - RAM Contenedores: {self.ram_mb_usado}/{ram_total_mb} MB"
