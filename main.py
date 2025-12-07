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
        print('6. Reportes Graphviz')
        print('7. Generar XML de Salida')
        print('8. Historial de Operaciones')
        print('9. Salir')
        print("="*50)
        
        opcion = input('\nElige una opción: ')
        
        if opcion == '1':
            cargar_archivo_xml()
        elif opcion == '2':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_centros_datos()
        elif opcion == '3':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_maquinas_virtuales()
        elif opcion == '4':
            if lista_centros is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_contenedores()
        elif opcion == '5':
            if lista_centros is None or gestor_solicitudes is None:
                print('\n   Primero debes cargar un archivo XML')
            else:
                menu_solicitudes()
        elif opcion == '6':
            print('\n  falta graphviz')
        elif opcion == '7':
            print('\n  falta xml de salida')
        elif opcion == '8':
            if ejecutor_instrucciones is not None:
                mostrar_historial()
            else:
                print('\n   No hay historial disponible')
        elif opcion == '9':
            print('\n   ¡Hasta pronto!')
            break
        else:
            print('\n   Error: Opción inválida. Elige entre 1 y 9')

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
        
        print('\n  Archivo XML cargado exitosamente')
        
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
        print('3. Ver centro con más recursos')
        print('4. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            listar_centros()
        elif opcion == '2':
            buscar_centro_por_id()
        elif opcion == '3':
            ver_centro_mas_recursos()
        elif opcion == '4':
            break
        else:
            print('\n   Opción inválida')

def listar_centros():
    """Lista todos los centros de datos"""
    global lista_centros
    
    print('\n=== CENTROS DE DATOS REGISTRADOS ===\n')
    
    nodo_centro = lista_centros.primero
    contador = 1
    
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        # Calculamos porcentajes de uso
        cpu_usado = centro.recursos.cpu_usado
        cpu_total = centro.recursos.cpu_total
        porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
        
        ram_usado = centro.recursos.ram_usado
        ram_total = centro.recursos.ram_total
        porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
        
        alm_usado = centro.recursos.almacenamiento_usado
        alm_total = centro.recursos.almacenamiento_total
        porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
        
        # Mostramos la información del centro
        print(f'{contador}. Centro: {centro.nombre} ({centro.id_centro}) - {centro.ciudad}, {centro.pais}')
        print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
        print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
        print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
        print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
        print(f'   VMs activas: {centro.maquinas_virtuales.size}\n')
        
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
            
            # Calculamos porcentajes de uso
            cpu_usado = centro.recursos.cpu_usado
            cpu_total = centro.recursos.cpu_total
            porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
            
            ram_usado = centro.recursos.ram_usado
            ram_total = centro.recursos.ram_total
            porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
            
            alm_usado = centro.recursos.almacenamiento_usado
            alm_total = centro.recursos.almacenamiento_total
            porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
            
            # Mostramos la información del centro (mismo formato que el listado)
            print(f'\n1. Centro: {centro.nombre} ({centro.id_centro}) - {centro.ciudad}, {centro.pais}')
            print(f'   Ubicación: {centro.ciudad}, {centro.pais}')
            print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
            print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
            print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
            print(f'   VMs activas: {centro.maquinas_virtuales.size}\n')
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n Centro con ID {id_centro} no encontrado')

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
        # Calculamos porcentajes de uso
        cpu_usado = centro_max.recursos.cpu_usado
        cpu_total = centro_max.recursos.cpu_total
        porcentaje_cpu = (cpu_usado * 100.0) / cpu_total if cpu_total > 0 else 0.0
        
        ram_usado = centro_max.recursos.ram_usado
        ram_total = centro_max.recursos.ram_total
        porcentaje_ram = (ram_usado * 100.0) / ram_total if ram_total > 0 else 0.0
        
        alm_usado = centro_max.recursos.almacenamiento_usado
        alm_total = centro_max.recursos.almacenamiento_total
        porcentaje_alm = (alm_usado * 100.0) / alm_total if alm_total > 0 else 0.0
        
        # Mostramos la información del centro (mismo formato que el listado)
        print(f'\n1. Centro: {centro_max.nombre} ({centro_max.id_centro}) - {centro_max.ciudad}, {centro_max.pais}')
        print(f'   Ubicación: {centro_max.ciudad}, {centro_max.pais}')
        print(f'   CPU: {cpu_usado}/{cpu_total} ({porcentaje_cpu:.2f}% usado)')
        print(f'   RAM: {ram_usado}/{ram_total} GB ({porcentaje_ram:.2f}% usado)')
        print(f'   Almacenamiento: {alm_usado}/{alm_total} TB ')
        print(f'   VMs activas: {centro_max.maquinas_virtuales.size}\n')

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
        print('1. Buscar VM por ID')
        print('2. Listar VMs de un centro')
        print('3. Migrar VM entre centros')
        print('4. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            buscar_vm_por_id()
        elif opcion == '2':
            listar_vms_de_un_centro()
        elif opcion == '3':
            migrar_vm()
        elif opcion == '4':
            break
        else:
            print('\n   Opción inválida')

def listar_vms_de_un_centro():
    """Lista las VMs de un centro específico"""
    global lista_centros
    
    id_centro = input('\nIngresa el ID del centro: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        if nodo_centro.dato.id_centro == id_centro:
            centro = nodo_centro.dato
            
            print(f'\n=== VMs en {centro.nombre} ===\n')
            
            if centro.maquinas_virtuales.size == 0:
                print('   No hay VMs en este centro\n')
                return
            
            nodo_vm = centro.maquinas_virtuales.primero
            contador = 1
            
            while nodo_vm is not None:
                vm = nodo_vm.dato
                
                # Determinamos el estado basado en si tiene contenedores activos
                estado = "Activa" if vm.contenedores.size > 0 else "Activa"
                
                print(f'{contador}. VM: {vm.id_vm} - {vm.sistema_operativo} (CPU: {vm.recursos.cpu_total}, RAM: {vm.recursos.ram_total}GB)')
                print(f'   Estado: {estado}')
                print(f'   IP: {vm.ip}')
                print(f'   Contenedores: {vm.contenedores.size}\n')
                
                nodo_vm = nodo_vm.siguiente
                contador += 1
            
            return
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   Centro con ID {id_centro} no encontrado')

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
    
    print('\n=== BUSCAR MÁQUINA VIRTUAL ===\n')
    id_vm = input('ID de la VM a buscar: ')
    
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                
                # Determinamos el estado basado en si tiene contenedores activos
                estado = "Activa" if vm.contenedores.size > 0 else "Inactiva"
                
                print(f'\n  VM encontrada:')
                print(f'   VM: {vm.id_vm} - {vm.sistema_operativo} (CPU: {vm.recursos.cpu_total}, RAM: {vm.recursos.ram_total}GB)')
                print(f'   Estado: {estado}')
                print(f'   IP: {vm.ip}')
                print(f'   Centro asignado: {centro.nombre}')
                print(f'   Contenedores: {vm.contenedores.size}\n')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada\n')

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
        print('1. Desplegar contenedor en VM')
        print('2. Listar contenedores de una VM')
        print('3. Cambiar estado de contenedor')
        print('4. Eliminar contenedor')
        print('5. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            desplegar_contenedor()
        elif opcion == '2':
            listar_contenedores_de_vm()
        elif opcion == '3':
            cambiar_estado_contenedor()
        elif opcion == '4':
            eliminar_contenedor()
        elif opcion == '5':
            break
        else:
            print('\n Opción inválida')

def desplegar_contenedor():
    """Despliega un nuevo contenedor en una VM"""
    global lista_centros
    
    print('\n=== DESPLEGAR CONTENEDOR ===\n')
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
                
                # Guardamos el estado anterior para mostrar el cambio
                cpu_usado_antes = vm.cpu_porcentaje_usado
                ram_usado_antes = vm.ram_mb_usado
                
                exito, mensaje = vm.agregar_contenedor(id_contenedor, nombre, imagen, puerto, cpu_porcentaje, ram_mb)
                
                if exito:
                    print(f'\n   {mensaje}')
                    print(f'\n  Recursos de VM {id_vm} actualizados:')
                    print(f'   CPU usado: {cpu_usado_antes:.1f}% → {vm.cpu_porcentaje_usado:.1f}% (+{float(cpu_porcentaje):.1f}%)')
                    print(f'   RAM usado: {ram_usado_antes} MB → {vm.ram_mb_usado} MB (+{int(ram_mb)} MB)')
                    print(f'   CPU disponible: {vm.obtener_cpu_disponible_porcentaje():.1f}%')
                    print(f'   RAM disponible: {vm.obtener_ram_disponible_mb()} MB')
                else:
                    print(f'\n   {mensaje}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n   VM {id_vm} no encontrada')

def listar_contenedores_de_vm():
    """Lista todos los contenedores de una VM específica"""
    global lista_centros
    
    print('\n=== LISTAR CONTENEDORES ===\n')
    id_vm = input('ID de la VM: ')
    
    # Buscamos la VM en todos los centros
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                
                print(f'\n=== Contenedores en VM {id_vm} ===\n')
                
                if vm.contenedores.size == 0:
                    print('   No hay contenedores en esta VM\n')
                    return
                
                nodo_cont = vm.contenedores.primero
                contador = 1
                
                while nodo_cont is not None:
                    cont = nodo_cont.dato
                    
                    print(f'{contador}. Contenedor: {cont.id_contenedor} - {cont.nombre} ({cont.imagen}) - Puerto: {cont.puerto}')
                    print(f'   Estado: {cont.estado}')
                    print(f'   CPU: {cont.cpu_porcentaje}%')
                    print(f'   RAM: {cont.ram_mb} MB\n')
                    
                    nodo_cont = nodo_cont.siguiente
                    contador += 1
                
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n VM {id_vm} no encontrada')

def cambiar_estado_contenedor():
    """Cambia el estado de un contenedor"""
    global lista_centros
    
    print('\n=== CAMBIAR ESTADO DE CONTENEDOR ===\n')
    id_vm = input('ID de la VM: ')
    id_contenedor = input('ID del Contenedor: ')
    
    print('\nEstados disponibles:')
    print('1. Pausado')
    print('2. Reiniciando')
    print('3. Activo')
    print('4. Detenido')
    
    nuevo_estado = input('\nSeleccione el nuevo estado (1-4): ')
    
    estados = {
        '1': 'Pausado',
        '2': 'Reiniciando',
        '3': 'Activo',
        '4': 'Detenido'
    }
    
    if nuevo_estado not in estados:
        print('\n Estado inválido')
        return
    
    # Buscamos la VM y el contenedor
    nodo_centro = lista_centros.primero
    while nodo_centro is not None:
        centro = nodo_centro.dato
        
        nodo_vm = centro.maquinas_virtuales.primero
        while nodo_vm is not None:
            if nodo_vm.dato.id_vm == id_vm:
                vm = nodo_vm.dato
                
                # Buscamos el contenedor
                nodo_cont = vm.contenedores.primero
                while nodo_cont is not None:
                    if nodo_cont.dato.id_contenedor == id_contenedor:
                        # Cambiamos el estado del contenedor
                        nodo_cont.dato.estado = estados[nuevo_estado]
                        print(f'\n   Estado del contenedor {id_contenedor} cambiado a: {estados[nuevo_estado]}')
                        return
                    nodo_cont = nodo_cont.siguiente
                
                print(f'\n Contenedor {id_contenedor} no encontrado en VM {id_vm}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n VM {id_vm} no encontrada')

def eliminar_contenedor():
    """Elimina un contenedor de una VM"""
    global lista_centros
    
    print('\n=== ELIMINAR CONTENEDOR ===\n')
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
                    print(f'\n  Recursos de VM {id_vm} actualizados:')
                    print(f'   CPU usado: {vm.cpu_porcentaje_usado:.1f}%')
                    print(f'   RAM usado: {vm.ram_mb_usado} MB')
                    print(f'   CPU disponible: {vm.obtener_cpu_disponible_porcentaje():.1f}%')
                    print(f'   RAM disponible: {vm.obtener_ram_disponible_mb()} MB')
                else:
                    print(f'\n   {mensaje}')
                return
            nodo_vm = nodo_vm.siguiente
        
        nodo_centro = nodo_centro.siguiente
    
    print(f'\n VM {id_vm} no encontrada')

def menu_solicitudes():
    """Menu para gestionar solicitudes"""
    while True:
        print('\n')
        print("="*50)
        print('Gestión de Solicitudes')
        print("="*50)
        print('1. Agregar nueva solicitud')
        print('2. Procesar solicitud de mayor prioridad')
        print('3. Procesar N solicitudes')
        print('4. Ver cola de solicitudes')
        print('5. Volver al menú principal')
        print("="*50)
        
        opcion = input('\nSeleccione una opción: ')
        
        if opcion == '1':
            agregar_nueva_solicitud()
        elif opcion == '2':
            procesar_solicitud_mayor_prioridad()
        elif opcion == '3':
            procesar_n_solicitudes()
        elif opcion == '4':
            ver_cola_solicitudes()
        elif opcion == '5':
            break
        else:
            print('\n   Opción inválida')

def agregar_nueva_solicitud():
    """Agrega una nueva solicitud al sistema"""
    global gestor_solicitudes
    
    print('\n=== AGREGAR NUEVA SOLICITUD ===\n')
    id_solicitud = input('ID de la solicitud: ')
    cliente = input('Cliente: ')
    
    print('\nTipo de solicitud:')
    print('1. Deploy')
    print('2. Backup')
    tipo_opcion = input('Selecciona (1-2): ')
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

def procesar_solicitud_mayor_prioridad():
    """Procesa la solicitud con mayor prioridad"""
    global lista_centros, gestor_solicitudes
    
    print('\n=== PROCESAR SOLICITUD DE MAYOR PRIORIDAD ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes en la cola\n')
        return
    
    exito, mensaje = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
    
    if exito:
        print(f'   {mensaje}\n')
    else:
        print(f'   {mensaje}\n')

def procesar_n_solicitudes():
    """Procesa N solicitudes en orden de prioridad"""
    global lista_centros, gestor_solicitudes
    
    print('\n=== PROCESAR N SOLICITUDES ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes en la cola\n')
        return
    
    cantidad = input('¿Cuántas solicitudes deseas procesar?: ')
    
    try:
        cantidad_num = int(cantidad)
        
        if cantidad_num <= 0:
            print('\n   La cantidad debe ser mayor a 0\n')
            return
        
        print(f'\n   Procesando {cantidad_num} solicitud(es)...\n')
        
        procesadas = 0
        exitosas = 0
        fallidas = 0
        
        while procesadas < cantidad_num and not gestor_solicitudes.cola_solicitudes.esta_vacia():
            exito, mensaje = gestor_solicitudes.procesar_siguiente_solicitud(lista_centros)
            
            if exito:
                print(f'   {mensaje}')
                exitosas += 1
            else:
                print(f'   {mensaje}')
                fallidas += 1
            
            procesadas += 1
        
        print(f'\n  Resumen:')
        print(f'   Total procesadas: {procesadas}')
        print(f'   Exitosas: {exitosas}')
        print(f'   Fallidas: {fallidas}\n')
        
    except ValueError:
        print('\n   Cantidad inválida. Debe ser un número entero\n')

def ver_cola_solicitudes():
    """Muestra todas las solicitudes pendientes ordenadas por prioridad"""
    global gestor_solicitudes
    
    print('\n=== COLA DE SOLICITUDES ===\n')
    
    if gestor_solicitudes.cola_solicitudes.esta_vacia():
        print('   No hay solicitudes pendientes\n')
        return
    
    # Mostramos la cola (sin desencolar)
    nodo_solicitud = gestor_solicitudes.cola_solicitudes.primero
    contador = 1
    
    while nodo_solicitud is not None:
        solicitud = nodo_solicitud.dato
        
        print(f'{contador}. Solicitud: {solicitud.id_solicitud} - {solicitud.cliente} ({solicitud.tipo}) - Prioridad: {solicitud.prioridad}')
        print(f'   Estado: Pendiente')
        print(f'   Recursos: CPU={solicitud.cpu}, RAM={solicitud.ram}GB\n')
        
        nodo_solicitud = nodo_solicitud.siguiente
        contador += 1

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
