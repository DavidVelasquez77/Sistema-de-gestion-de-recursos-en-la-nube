from TDAs.Nodo import Nodo

class ListaEnlazada:
    def __init__(self):
        self.size = 0
        self.ultimo = None
        self.primero = None
    
    #definiendo la función que va a insertar los datos a la lista
     #____________________________________________________________________
    def insertar(self, dato):
        nuevo = Nodo(dato)

        if self.primero is None: 
            self.primero = nuevo

        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
     #____________________________________________________________________

       

    #definiendo la función que va a mostrar los datos en la lista
     #____________________________________________________________________
    def mostrar(self):
        actual = self.primero
        while actual:
            print(actual.dato)
            actual = actual.siguiente
    #______________________________________________________________________



    #definiendo la función que va a buscar los datos en la lista
     #____________________________________________________________________
    def buscar(self, id):
        actual = self.primero
        while actual:
            if actual.dato.id == id:
                return actual.dato
            actual = actual.siguiente
        return None
     #____________________________________________________________________


    
            