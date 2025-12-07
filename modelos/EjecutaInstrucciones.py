from TDAs.ListaEnlazada import ListaEnlazada

class EjecutaInstrucciones:
    def __init__(self):
        self.instrucciones = ListaEnlazada()
        self.historial = ListaEnlazada()
    
    def agregar_instruccion(self, instruccion):
        self.instrucciones.insertar(instruccion)
    
    def ejecutar_todas(self, lista_centros, gestor_solicitudes):
        if self.instrucciones.primero is None:
            return "No hay instrucciones para ejecutar"
        
        nodo_instruccion_actual = self.instrucciones.primero
        
        # Recorremos todas las instrucciones para ejecutarlas en orden
        while nodo_instruccion_actual is not None:
            instruccion = nodo_instruccion_actual.dato
            
            if instruccion.tipo == "crearVM":
                resultado = self.ejecutar_crear_vm(instruccion, lista_centros)
                print(f"  ✓ {resultado}")
                self.historial.insertar(f"[crearVM]: {resultado}")
            elif instruccion.tipo == "migrarVM":
                resultado = self.ejecutar_migrar_vm(instruccion, lista_centros)
                print(f"  ✓ {resultado}")
                self.historial.insertar(f"[migrarVM]: {resultado}")
            elif instruccion.tipo == "procesarSolicitudes":
                resultado = self.ejecutar_procesar_solicitudes(instruccion, lista_centros, gestor_solicitudes)
                print(f"  ✓ {resultado}")
                self.historial.insertar(f"[procesarSolicitudes]: {resultado}")
            else:
                resultado = f"Tipo de instruccion desconocido: {instruccion.tipo}"
                print(f"  ✗ {resultado}")
                self.historial.insertar(resultado)
            
            nodo_instruccion_actual = nodo_instruccion_actual.siguiente
    
    def ejecutar_crear_vm(self, instruccion, lista_centros):
        # Soportamos diferentes nombres de parametros del XML
        id_vm = instruccion.obtener_parametro("id")
        id_centro = instruccion.obtener_parametro("centroAsignado")
        if id_centro is None:
            id_centro = instruccion.obtener_parametro("centro")
        
        sistema_operativo = instruccion.obtener_parametro("sistemaOperativo")
        if sistema_operativo is None:
            sistema_operativo = instruccion.obtener_parametro("so")
        
        ip = instruccion.obtener_parametro("ip")
        if ip is None:
            # Si no viene IP, generamos una automatica basada en el hash del id
            ip = "192.168.1.100"
        
        cpu = instruccion.obtener_parametro("cpu")
        ram = instruccion.obtener_parametro("ram")
        almacenamiento = instruccion.obtener_parametro("almacenamiento")
        
        # Verificamos que todos los parametros necesarios esten presentes
        if id_vm is None or id_centro is None or sistema_operativo is None or cpu is None or ram is None or almacenamiento is None:
            return "Error: Faltan parametros para crear VM"
        
        centro = self.buscar_centro_por_id(lista_centros, id_centro)
        if centro is None:
            return f"Error: Centro {id_centro} no encontrado"
        
        exito, mensaje = centro.crear_vm(id_vm, sistema_operativo, ip, cpu, ram, almacenamiento)
        
        if exito:
            return f"VM creada exitosamente"
        else:
            return f"Error al crear VM: {mensaje}"
    
    def ejecutar_migrar_vm(self, instruccion, lista_centros):
        # Soportamos diferentes nombres de parametros del XML
        id_vm = instruccion.obtener_parametro("id")
        if id_vm is None:
            id_vm = instruccion.obtener_parametro("vmId")
        
        centro_origen_id = instruccion.obtener_parametro("centroOrigen")
        centro_destino_id = instruccion.obtener_parametro("centroDestino")
        
        # Verificamos que todos los parametros necesarios esten presentes
        if id_vm is None or centro_origen_id is None or centro_destino_id is None:
            return "Error: Faltan parametros para migrar VM"
        
        centro_origen = self.buscar_centro_por_id(lista_centros, centro_origen_id)
        centro_destino = self.buscar_centro_por_id(lista_centros, centro_destino_id)
        
        if centro_origen is None:
            return f"Error: Centro origen {centro_origen_id} no encontrado"
        
        if centro_destino is None:
            return f"Error: Centro destino {centro_destino_id} no encontrado"
        
        vm = self.buscar_vm_en_centro(centro_origen, id_vm)
        if vm is None:
            return f"Error: VM {id_vm} no encontrada en centro {centro_origen.nombre}"
        
        # Verificamos que el centro destino tenga recursos suficientes
        cpu_disponible = centro_destino.recursos.obtener_cpu_disponible()
        ram_disponible = centro_destino.recursos.obtener_ram_disponible()
        almacenamiento_disponible = centro_destino.recursos.obtener_almacenamiento_disponible()
        
        if vm.recursos.cpu_total > cpu_disponible:
            return f"Error: CPU insuficiente en destino. Disponible: {cpu_disponible}, Requerido: {vm.recursos.cpu_total}"
        
        if vm.recursos.ram_total > ram_disponible:
            return f"Error: RAM insuficiente en destino. Disponible: {ram_disponible}, Requerido: {vm.recursos.ram_total}"
        
        if vm.recursos.almacenamiento_total > almacenamiento_disponible:
            return f"Error: Almacenamiento insuficiente en destino. Disponible: {almacenamiento_disponible}, Requerido: {vm.recursos.almacenamiento_total}"
        
        # Eliminamos la VM del centro origen
        exito = self.eliminar_vm_de_centro(centro_origen, id_vm)
        if not exito:
            return f"Error: No se pudo eliminar VM del centro origen"
        
        # Agregamos la VM al centro destino
        centro_destino.maquinas_virtuales.insertar(vm)
        centro_destino.recursos.asignar_recursos(vm.recursos.cpu_total, vm.recursos.ram_total, vm.recursos.almacenamiento_total)
        vm.centro_asignado = centro_destino.id_centro
        
        return f"VM migrada exitosamente a {centro_destino.nombre}"
    
    def ejecutar_procesar_solicitudes(self, instruccion, lista_centros, gestor_solicitudes):
        cantidad_str = instruccion.obtener_parametro("cantidad")
        
        if cantidad_str is None:
            return "Error: Falta parametro cantidad"
        
        cantidad = int(cantidad_str)
        
        if gestor_solicitudes is None:
            return "Error: No hay gestor de solicitudes disponible"
        
        procesadas = 0
        exitosas = 0
        fallidas = 0
        
        while procesadas < cantidad and not gestor_solicitudes.cola_solicitudes.esta_vacia():
            exito, mensaje = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
            
            if exito:
                exitosas += 1
            else:
                fallidas += 1
            
            procesadas += 1
        
        return f"Procesadas: {procesadas}, Completadas: {exitosas}, Fallidas: {fallidas}"
    
    def buscar_centro_por_id(self, lista_centros, id_centro):
        if lista_centros.primero is None:
            return None
        
        nodo_centro_actual = lista_centros.primero
        while nodo_centro_actual is not None:
            if nodo_centro_actual.dato.id_centro == id_centro:
                return nodo_centro_actual.dato
            nodo_centro_actual = nodo_centro_actual.siguiente
        
        return None
    
    def buscar_vm_en_centro(self, centro, id_vm):
        if centro.maquinas_virtuales.primero is None:
            return None
        
        nodo_vm_actual = centro.maquinas_virtuales.primero
        while nodo_vm_actual is not None:
            if nodo_vm_actual.dato.id_vm == id_vm:
                return nodo_vm_actual.dato
            nodo_vm_actual = nodo_vm_actual.siguiente
        
        return None
    
    def eliminar_vm_de_centro(self, centro, id_vm):
        if centro.maquinas_virtuales.primero is None:
            return False
        
        nodo_vm_actual = centro.maquinas_virtuales.primero
        nodo_vm_anterior = None
        
        # Buscamos la VM en la lista y la eliminamos liberando sus recursos
        while nodo_vm_actual is not None:
            if nodo_vm_actual.dato.id_vm == id_vm:
                vm_a_eliminar = nodo_vm_actual.dato
                
                # Liberamos los recursos que estaba consumiendo la VM
                centro.recursos.liberar_recursos(vm_a_eliminar.recursos.cpu_total, vm_a_eliminar.recursos.ram_total, vm_a_eliminar.recursos.almacenamiento_total)
                
                # Eliminamos el nodo de la lista enlazada
                if nodo_vm_anterior is None:
                    centro.maquinas_virtuales.primero = nodo_vm_actual.siguiente
                else:
                    nodo_vm_anterior.siguiente = nodo_vm_actual.siguiente
                
                # IMPORTANTE: Decrementamos el contador de la lista
                centro.maquinas_virtuales.size -= 1
                
                return True
            
            nodo_vm_anterior = nodo_vm_actual
            nodo_vm_actual = nodo_vm_actual.siguiente
        
        return False
