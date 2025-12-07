# Importaciones
from XMLReader.xmlReader import XMLReader
from TDAs.ListaEnlazada import ListaEnlazada
from modelos.CentroDatos import CentroDatos
from modelos.GestorSolicitudes import GestorSolicitudes
from modelos.EjecutaInstrucciones import EjecutaInstrucciones

# Variables globales para mantener el estado del sistema
lista_centros = None
lista_solicitudes = None
lista_instrucciones = None
gestor_solicitudes = None
ejecutor_instrucciones = None

def menu_principal():
    """Muestra el menu principal del sistema"""
    global lista_centros, lista_solicitudes, lista_instrucciones
    global gestor_solicitudes, ejecutor_instrucciones
    
    while True:
        print('\n')
        print("="*50)
        print('CloudSync Manager - Sistema de la Nube')
        print("="*50)
        print('1. Cargar Archivo XML')
        print('2. Gestión de Centros de Datos')
        print('3. Gestión de Máquinas Virtuales')
        print('4. Gestión de Contenedores')
        print('5. Gestión de Solicitudes')
        print('6. Ejecutar Instrucciones')
        print('7. Reportes en Graphviz')
        print('8. Generar XML de Salida')
        print('9. Historial de Operaciones')
        print('0. Salir')
        print("="*50)
        
        opcion = input('\nElige una opción: ')
        
        if opcion == '1':
            cargar_archivo_xml()
        elif opcion == '2':
            if lista_centros is None:
                print('\n  Primero debes cargar un archivo XML')
            else:
                menu_centros_datos()
        elif opcion == '3':
            if lista_centros is None:
                print('\n  Primero debes cargar un archivo XML')
            else:
                menu_maquinas_virtuales()
        elif opcion == '4':
            if lista_centros is None:
                print('\n  Primero debes cargar un archivo XML')
            else:
                menu_contenedores()
        elif opcion == '5':
            if lista_centros is None or gestor_solicitudes is None:
                print('\n  Primero debes cargar un archivo XML')
            else:
                menu_solicitudes()
        elif opcion == '6':
            if lista_centros is None or ejecutor_instrucciones is None:
                print('\n Primero debes cargar un archivo XML')
            else:
                ejecutar_instrucciones()
        elif opcion == '7':
            print('\n Módulo de reportes en desarrollo...')
        elif opcion == '8':
            print('\n Módulo de generación XML en desarrollo...')
        elif opcion == '9':
            if ejecutor_instrucciones is not None:
                mostrar_historial()
            else:
                print('\n  No hay historial disponible')
        elif opcion == '0':
            print('\n👋 ¡Hasta pronto!')
            break
        else:
            print('\n   Error: Opción inválida. Elige entre 0 y 9')

def cargar_archivo_xml():
    """Carga el archivo XML y inicializa las estructuras"""
    global lista_centros, lista_solicitudes, lista_instrucciones
    global gestor_solicitudes, ejecutor_instrucciones
    
    print('\n=== CARGAR ARCHIVO XML ===\n')
    ruta_archivo = input('Ingresa la ruta del archivo XML: ')
    
    try:
        lector = XMLReader()
        lista_centros, lista_solicitudes, lista_instrucciones = lector.analizar_archivoXML(ruta_archivo)
        
        if lista_centros is None:
            print('\n   Error al cargar el archivo')
            return
        
        # Inicializamos el gestor de solicitudes y cargamos las solicitudes
        gestor_solicitudes = GestorSolicitudes()
        nodo_solicitud = lista_solicitudes.primero
        while nodo_solicitud is not None:
            gestor_solicitudes.encolar_solicitud(nodo_solicitud.dato)
            nodo_solicitud = nodo_solicitud.siguiente
        
        # Inicializamos el ejecutor de instrucciones
        ejecutor_instrucciones = EjecutaInstrucciones()
        ejecutor_instrucciones.instrucciones = lista_instrucciones
        
        # Ejecutamos automáticamente las instrucciones
        ejecutor_instrucciones.ejecutar_todas(lista_centros, gestor_solicitudes)
        
        print('\n✓ Archivo XML cargado exitosamente')
        
    except Exception as e:
        print(f'\n   Error al cargar el archivo: {e}')

def menu_centros_datos():
    """Menu para gestionar centros de datos"""
    global lista_centros
    
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Centros de Datos')
        print("="*50)
        print('1. Listar todos los Centros')
        print('2. Buscar Centro por ID')
        print('3. Ver centro con más recursos disponibles')
        print('4. Ver detalles completos de un centro')
        print('0. Regresar al menú Principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            listar_centros()
        elif opcion == '2':
            buscar_centro_por_id()
        elif opcion == '3':
            ver_centro_mas_recursos()
        elif opcion == '4':
            ver_detalles_centro()
        elif opcion == '0':
            break
        else:
            print('\n   Opción inválida')

def listar_centros():
    """Lista todos los centros de datos"""
    global lista_centros
    
    print('\n' + "="*50)
    print('CENTROS DE DATOS')
    print("="*50)
    
    nodo_centro = lista_centros.primero
    contador = 1
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        print(f'\n{contador}. {centro.nombre} ({centro.id_centro})')
        print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
        print(f'   {centro.recursos}')
        print(f'   Total de VMs: {centro.maquinas_virtuales.size}')
        
        nodo_centro = nodo_centro.siguiente
        contador += 1

def buscar_centro_por_id():
    """Busca un centro por su ID"""
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro a buscar: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            print(f'\n   Centro encontrado:')
            print(f'   Nombre: {centro.nombre}')
            print(f'   ID: {centro.id_centro}')
            print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
            print(f'   {centro.recursos}')
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro con ID {id_centro} no encontrado')

def ver_centro_mas_recursos():
    """Muestra el centro con más recursos disponibles"""
    global lista_centros
    
    if lista_centros.primero is None:
        print('\n  No hay centros disponibles')
        return
    
    centro_max = None
    recursos_max = 0
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        recursos_disponibles = (centro.recursos.obtener_cpu_disponible() + 
                               centro.recursos.obtener_ram_disponible() + 
                               centro.recursos.obtener_almacenamiento_disponible())
        
        if recursos_disponibles > recursos_max:
            recursos_max = recursos_disponibles
            centro_max = centro
        
        nodo_centro = nodo_centro.siguiente
    
    if centro_max is not None:
        print(f'\n   Centro con más recursos: {centro_max.nombre}')
        print(f'   {centro_max.recursos}')

def ver_detalles_centro():
    """Muestra detalles completos de un centro incluyendo VMs y contenedores"""
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            print(f'\n{"="*50}')
            print(f'{centro.nombre} ({centro.id_centro})')
            print(f'{"="*50}')
            print(f'Ubicación: {centro.ciudad}, {centro.pais}')
            print(f'{centro.recursos}')
            print(f'\nMáquinas Virtuales: {centro.maquinas_virtuales.size}')
            
            nodo_vm = centro.maquinas_virtuales.primero
            while nodo_vm is not None:
                vm = nodo_vm.dato
                print(f'\n     {vm.id_vm}: {vm.sistema_operativo}')
                print(f'     IP: {vm.ip}')
                print(f'     {vm.recursos}')
                print(f'     Contenedores: {vm.contenedores.size}')
                
                nodo_cont = vm.contenedores.primero
                while nodo_cont is not None:
                    cont = nodo_cont.dato
                    print(f'          {cont.id_contenedor}: {cont.nombre}')
                    print(f'          Imagen: {cont.imagen}')
                    print(f'          CPU: {cont.cpu_porcentaje}%, RAM: {cont.ram_mb} MB')
                    nodo_cont = nodo_cont.siguiente
                
                nodo_vm = nodo_vm.siguiente
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro con ID {id_centro} no encontrado')

def menu_maquinas_virtuales():
    """Menu para gestionar máquinas virtuales"""
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Máquinas Virtuales')
        print("="*50)
        print('1. Listar todas las VMs')
        print('2. Crear nueva VM')
        print('3. Buscar VM por ID')
        print('4. Migrar VM entre centros')
        print('0. Regresar')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            listar_todas_vms()
        elif opcion == '2':
            crear_nueva_vm()
        elif opcion == '3':
            buscar_vm_por_id()
        elif opcion == '4':
            migrar_vm()
        elif opcion == '0':
            break
        else:
            print('\n   Opción inválida')

def listar_todas_vms():
    """Lista todas las máquinas virtuales del sistema"""
    global lista_centros
    
    print('\n' + "="*50)
    print('MÁQUINAS VIRTUALES')
    print("="*50)
    
    total_vms = 0
    nodo_centro = lista_centros.primero
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        if centro.maquinas_virtuales.size > 0:
            print(f'\n   Centro: {centro.nombre}')
            
            nodo_vm = centro.maquinas_virtuales.primero
            while nodo_vm is not None:
                vm = nodo_vm.dato
                print(f'      {vm.id_vm}: {vm.sistema_operativo} ({vm.ip})')
                print(f'      {vm.recursos}')
                total_vms += 1
                nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Total de VMs en el sistema: {total_vms}')

def crear_nueva_vm():
    """Crea una nueva máquina virtual"""
    global lista_centros
    
    print('\n--- Crear Nueva VM ---')
    id_vm = input('ID de la VM: ')
    id_centro = input('ID del Centro donde crearla: ')
    sistema_operativo = input('Sistema Operativo: ')
    ip = input('Dirección IP: ')
    cpu = input('CPU (núcleos): ')
    ram = input('RAM (GB): ')
    almacenamiento = input('Almacenamiento (GB): ')
    
    # Buscamos el centro
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            exito, mensaje = centro.crear_vm(id_vm, sistema_operativo, ip, cpu, ram, almacenamiento)
            
            if exito:
                print(f'\n   {mensaje}')
            else:
                print(f'\n   {mensaje}')
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro {id_centro} no encontrado')

def buscar_vm_por_id():
    """Busca una VM por su ID en todos los centros"""
    global lista_centros
    
    id_vm = input('\nIngresa el ID de la VM: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                print(f'\n   VM encontrada en: {centro.nombre}')
                print(f'   ID: {vm.id_vm}')
                print(f'   SO: {vm.sistema_operativo}')
                print(f'   IP: {vm.ip}')
                print(f'   {vm.recursos}')
                print(f'   Contenedores: {vm.contenedores.size}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada')

def migrar_vm():
    """Migra una VM de un centro a otro"""
    global lista_centros, ejecutor_instrucciones
    
    print('\n--- Migrar VM ---')
    id_vm = input('ID de la VM a migrar: ')
    id_origen = input('ID del Centro origen: ')
    id_destino = input('ID del Centro destino: ')
    
    # Usamos el ejecutor para migrar
    from modelos.Instruccion import Instruccion
    instruccion = Instruccion('migrarVM')
    instruccion.agregar_parametro('vmId', id_vm)
    instruccion.agregar_parametro('centroOrigen', id_origen)
    instruccion.agregar_parametro('centroDestino', id_destino)
    
    resultado = ejecutor_instrucciones.ejecutar_migrar_vm(instruccion, lista_centros)
    print(f'\n{resultado}')

def menu_contenedores():
    """Menu para gestionar contenedores"""
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Contenedores')
        print("="*50)
        print('1. Listar todos los contenedores')
        print('2. Agregar contenedor a una VM')
        print('3. Eliminar contenedor de una VM')
        print('0. Regresar')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            listar_contenedores()
        elif opcion == '2':
            agregar_contenedor()
        elif opcion == '3':
            eliminar_contenedor()
        elif opcion == '0':
            break
        else:
            print('\n   Opción inválida')

def listar_contenedores():
    """Lista todos los contenedores del sistema"""
    global lista_centros
    
    print('\n' + "="*50)
    print('CONTENEDORES')
    print("="*50)
    
    total_contenedores = 0
    nodo_centro = lista_centros.primero
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            vm = nodo_vm.dato
            
            if vm.contenedores.size > 0:
                print(f'\n   VM: {vm.id_vm} ({centro.nombre})')
                
                nodo_cont = vm.contenedores.primero
                while nodo_cont is not None:
                    cont = nodo_cont.dato
                    print(f'      {cont.id_contenedor}: {cont.nombre}')
                    print(f'      Imagen: {cont.imagen}, Puerto: {cont.puerto}')
                    print(f'      CPU: {cont.cpu_porcentaje}%, RAM: {cont.ram_mb} MB')
                    total_contenedores += 1
                    nodo_cont = nodo_cont.siguiente
            
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Total de contenedores: {total_contenedores}')

def agregar_contenedor():
    """Agrega un contenedor a una VM"""
    global lista_centros
    
    print('\n--- Agregar Contenedor ---')
    id_vm = input('ID de la VM: ')
    id_contenedor = input('ID del Contenedor: ')
    nombre = input('Nombre: ')
    imagen = input('Imagen: ')
    puerto = input('Puerto: ')
    cpu_porcentaje = input('CPU (%): ')
    ram_mb = input('RAM (MB): ')
    
    # Buscamos la VM en todos los centros
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                exito, mensaje = vm.agregar_contenedor(id_contenedor, nombre, imagen, puerto, cpu_porcentaje, ram_mb)
                
                if exito:
                    print(f'\n   {mensaje}')
                else:
                    print(f'\n   {mensaje}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada')

def eliminar_contenedor():
    """Elimina un contenedor de una VM"""
    global lista_centros
    
    print('\n--- Eliminar Contenedor ---')
    id_vm = input('ID de la VM: ')
    id_contenedor = input('ID del Contenedor a eliminar: ')
    
    # Buscamos la VM en todos los centros
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                exito, mensaje = vm.eliminar_contenedor(id_contenedor)
                
                if exito:
                    print(f'\n   {mensaje}')
                else:
                    print(f'\n   {mensaje}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada')

def menu_solicitudes():
    """Menu para gestionar solicitudes"""
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Solicitudes')
        print("="*50)
        print('1. Ver solicitudes pendientes')
        print('2. Agregar nueva solicitud')
        print('3. Procesar siguiente solicitud')
        print('4. Procesar múltiples solicitudes')
        print('0. Regresar')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            ver_solicitudes_pendientes()
        elif opcion == '2':
            agregar_nueva_solicitud()
        elif opcion == '3':
            procesar_siguiente_solicitud()
        elif opcion == '4':
            procesar_multiples_solicitudes()
        elif opcion == '0':
            break
        else:
            print('\n   Opción inválida')

def ver_solicitudes_pendientes():
    """Muestra las solicitudes pendientes"""
    global gestor_solicitudes
    
    print('\n' + "="*50)
    print('SOLICITUDES PENDIENTES')
    print("="*50)
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('\n  No hay solicitudes pendientes')
        return
    
    # Mostramos la cola (sin desencolar)
    nodo_solicitud = gestor_solicitudes.cola_solicitudes.primero
    contador = 1
    
    while nodo_solicitud is not None:
        solicitud = nodo_solicitud.dato
        print(f'\n{contador}. {solicitud}')
        nodo_solicitud = nodo_solicitud.siguiente
        contador += 1

def agregar_nueva_solicitud():
    """Agrega una nueva solicitud al sistema"""
    global gestor_solicitudes
    
    print('\n--- Nueva Solicitud ---')
    id_solicitud = input('ID de la solicitud: ')
    cliente = input('Cliente: ')
    print('Tipo (1=Deploy, 2=Backup): ')
    tipo_opcion = input('Selecciona: ')
    tipo = 'Deploy' if tipo_opcion == '1' else 'Backup'
    prioridad = input('Prioridad (1-10): ')
    cpu = input('CPU requerido (núcleos): ')
    ram = input('RAM requerido (GB): ')
    almacenamiento = input('Almacenamiento requerido (GB): ')
    tiempo_estimado = input('Tiempo estimado (minutos): ')
    
    exito, mensaje = gestor_solicitudes.agregar_solicitud(
        id_solicitud, cliente, tipo, prioridad, cpu, ram, almacenamiento, tiempo_estimado
    )
    
    if exito:
        print(f'\n   {mensaje}')
    else:
        print(f'\n   {mensaje}')

def procesar_siguiente_solicitud():
    """Procesa la siguiente solicitud en la cola"""
    global lista_centros, gestor_solicitudes
    
    exito, mensaje = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
    
    if exito:
        print(f'\n   {mensaje}')
    else:
        print(f'\n   {mensaje}')

def procesar_multiples_solicitudes():
    """Procesa múltiples solicitudes"""
    global lista_centros, gestor_solicitudes
    
    cantidad = input('\n¿Cuántas solicitudes deseas procesar?: ')
    
    try:
        cantidad_num = int(cantidad)
        exito, mensaje = gestor_solicitudes.procesar_solicitudes(lista_centros, cantidad_num)
        print(f'\n{mensaje}')
    except:
        print('\n   Cantidad inválida')

def ejecutar_instrucciones():
    """Ejecuta todas las instrucciones cargadas del XML"""
    global lista_centros, gestor_solicitudes, ejecutor_instrucciones
    
    print('\n' + "="*50)
    print('EJECUTANDO INSTRUCCIONES')
    print("="*50)
    
    ejecutor_instrucciones.ejecutar_todas(lista_centros, gestor_solicitudes)

def mostrar_historial():
    """Muestra el historial de operaciones"""
    global ejecutor_instrucciones
    
    print('\n' + "="*50)
    print('HISTORIAL DE OPERACIONES')
    print("="*50)
    
    if ejecutor_instrucciones.historial.primero is None:
        print('\n  No hay operaciones en el historial')
        return
    
    nodo_hist = ejecutor_instrucciones.historial.primero
    while nodo_hist is not None:
        print(f'  • {nodo_hist.dato}')
        nodo_hist = nodo_hist.siguiente

if __name__ == "__main__":
    menu_principal()
