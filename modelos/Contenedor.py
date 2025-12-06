class Contenedor:
    def __init__(self, id_contenedor, nombre, imagen, puerto, cpu_porcentaje, ram_mb):
        self.id_contenedor = id_contenedor
        self.nombre = nombre
        self.imagen = imagen
        self.puerto = int(puerto)
        self.cpu_porcentaje = float(cpu_porcentaje)
        self.ram_mb = int(ram_mb)

    def __str__(self):
        return f"Contenedor {self.id_contenedor} - {self.nombre} - Imagen: {self.imagen} - Puerto: {self.puerto} - CPU: {self.cpu_porcentaje}% - RAM: {self.ram_mb} MB"
