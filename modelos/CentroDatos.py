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
        
        cpu_necesario = int(cpu_requerido)
        ram_necesaria = int(ram_requerido)
        almacenamiento_necesario = int(almacenamiento_requerido)
        
        cpu_disponible = self.recursos.obtener_cpu_disponible()
        ram_disponible = self.recursos.obtener_ram_disponible()
        almacenamiento_disponible = self.recursos.obtener_almacenamiento_disponible()
        
        # Verificamos si el centro tiene suficientes nucleos de CPU
        if cpu_necesario > cpu_disponible:
            return False, f"CPU insuficiente. Disponible: {cpu_disponible} nucleos, Requerido: {cpu_necesario} nucleos"
        
        # Verificamos si el centro tiene suficiente memoria RAM
        if ram_necesaria > ram_disponible:
            return False, f"RAM insuficiente. Disponible: {ram_disponible} GB, Requerido: {ram_necesaria} GB"
        
        # Verificamos si el centro tiene suficiente almacenamiento
        if almacenamiento_necesario > almacenamiento_disponible:
            return False, f"Almacenamiento insuficiente. Disponible: {almacenamiento_disponible} GB, Requerido: {almacenamiento_necesario} GB"
        
        # Creamos la nueva maquina virtual con los recursos solicitados
        vm_nueva = MaquinaVirtual(id_vm, self.id_centro, sistema_operativo, ip, cpu_necesario, ram_necesaria, almacenamiento_necesario)
        self.maquinas_virtuales.insertar(vm_nueva)
        
        # Asignamos los recursos al centro (se consumen)
        self.recursos.asignar_recursos(cpu_necesario, ram_necesaria, almacenamiento_necesario)
        
        return True, f"VM {id_vm} creada exitosamente en {self.nombre}"

    def __str__(self):
        return f"{self.id_centro} - {self.nombre} - {self.pais}, {self.ciudad} - Capacidad: {self.capacidad} VMs - {self.recursos}"