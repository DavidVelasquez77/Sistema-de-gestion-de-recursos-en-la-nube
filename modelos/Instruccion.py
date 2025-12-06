class Instruccion:
    def __init__(self, tipo):
        self.tipo = tipo
        self.parametros = {}
    
    def agregar_parametro(self, clave, valor):
        self.parametros[clave] = valor
    
    def obtener_parametro(self, clave):
        if clave in self.parametros:
            return self.parametros[clave]
        return None
    
    def __str__(self):
        params_str = ", ".join([f"{k}: {v}" for k, v in self.parametros.items()])
        return f"Instruccion [{self.tipo}] - {params_str}"
