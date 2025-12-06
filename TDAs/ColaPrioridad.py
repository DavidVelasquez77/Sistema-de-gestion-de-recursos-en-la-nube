from TDAs.Nodo import Nodo

class ColaPrioridad:
    def __init__(self):
        self.primero = None
        self.size = 0

    def encolar(self, solicitud):
        nuevo_nodo = Nodo(solicitud)
        
        if self.primero is None:
            self.primero = nuevo_nodo
        elif solicitud.prioridad > self.primero.dato.prioridad:
            nuevo_nodo.siguiente = self.primero
            self.primero = nuevo_nodo
        else:
            actual = self.primero
            while actual.siguiente and actual.siguiente.dato.prioridad >= solicitud.prioridad:
                actual = actual.siguiente
            nuevo_nodo.siguiente = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self.size += 1

    def desencolar(self):
        if self.primero is None:
            return None
        
        solicitud = self.primero.dato
        self.primero = self.primero.siguiente
        self.size -= 1
        return solicitud

    def ver_primero(self):
        if self.primero is None:
            return None
        return self.primero.dato

    def esta_vacia(self):
        return self.primero is None

    def mostrar_todas(self):
        if self.primero is None:
            return
        
        actual = self.primero
        while actual:
            print(actual.dato)
            actual = actual.siguiente
