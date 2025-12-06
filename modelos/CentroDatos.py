class CentroDatos:
    def __init__(self, id_centro, nombre, pais, ciudad, capacidad, cpu, ram, almacenamiento):
        self.id_centro = id_centro
        self.nombre = nombre
        self.pais = pais
        self.ciudad = ciudad
        self.capacidad = capacidad
        self.cpu = cpu
        self.ram = ram
        self.almacenamiento = almacenamiento

    def __str__(self):
        return f"{self.id_centro} - {self.nombre} - {self.pais} - {self.ciudad} - {self.capacidad} - {self.cpu} - {self.ram} - {self.almacenamiento}"