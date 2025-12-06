class Recursos:
    def __init__(self, cpu_total, ram_total, almacenamiento_total):
        self.cpu_total = int(cpu_total)
        self.ram_total = int(ram_total)
        self.almacenamiento_total = int(almacenamiento_total)
        self.cpu_usado = 0
        self.ram_usado = 0
        self.almacenamiento_usado = 0

    def obtener_cpu_disponible(self):
        return self.cpu_total - self.cpu_usado

    def obtener_ram_disponible(self):
        return self.ram_total - self.ram_usado

    def obtener_almacenamiento_disponible(self):
        return self.almacenamiento_total - self.almacenamiento_usado

    def verificar_disponibilidad(self, cpu_req, ram_req, almacenamiento_req):
        cpu_disponible = self.obtener_cpu_disponible() >= cpu_req
        ram_disponible = self.obtener_ram_disponible() >= ram_req
        almacenamiento_disponible = self.obtener_almacenamiento_disponible() >= almacenamiento_req
        
        return cpu_disponible and ram_disponible and almacenamiento_disponible

    def asignar_recursos(self, cpu, ram, almacenamiento):
        if self.verificar_disponibilidad(cpu, ram, almacenamiento):
            self.cpu_usado += cpu
            self.ram_usado += ram
            self.almacenamiento_usado += almacenamiento
            return True
        return False

    def liberar_recursos(self, cpu, ram, almacenamiento):
        self.cpu_usado -= cpu
        self.ram_usado -= ram
        self.almacenamiento_usado -= almacenamiento
        
        if self.cpu_usado < 0:
            self.cpu_usado = 0
        if self.ram_usado < 0:
            self.ram_usado = 0
        if self.almacenamiento_usado < 0:
            self.almacenamiento_usado = 0

    def __str__(self):
        return f"CPU: {self.cpu_usado}/{self.cpu_total} nucleos | RAM: {self.ram_usado}/{self.ram_total} GB | Almacenamiento: {self.almacenamiento_usado}/{self.almacenamiento_total} GB"
