from xml.dom import minidom
from modelos.CentroDatos import CentroDatos
from modelos.MaquinaVirtual import MaquinaVirtual
from modelos.Contenedor import Contenedor
from modelos.Solicitud import Solicitud
from modelos.Instruccion import Instruccion
from TDAs.ListaEnlazada import ListaEnlazada

class XMLReader:

    def analizar_archivoXML(self, ruta_archivo):
        try:
            doc = minidom.parse(ruta_archivo)
            root = doc.documentElement  # definiendo raiz: <cloudSync>
            
            # Estructuras principales que devolveremos
            lista_centros = ListaEnlazada()
            lista_solicitudes = ListaEnlazada()
            lista_instrucciones = ListaEnlazada()

            print('\n')
            print("Cargando archivo...")
            print("="*50)

            # ========== CARGANDO CENTROS DE DATOS ==========
            centros = root.getElementsByTagName("configuracion")[0] \
                          .getElementsByTagName("centrosDatos")[0] \
                          .getElementsByTagName("centro")

            for centro in centros:
                id_centro = centro.getAttribute("id")
                nombre = centro.getAttribute("nombre")

                # Obteniendo ubicacion del centro
                ubicacion = centro.getElementsByTagName("ubicacion")[0]
                pais = ubicacion.getElementsByTagName("pais")[0].firstChild.data
                ciudad = ubicacion.getElementsByTagName("ciudad")[0].firstChild.data

                # Obteniendo capacidad de recursos del centro
                capacidad_elemento = centro.getElementsByTagName("capacidad")[0]
                cpu = capacidad_elemento.getElementsByTagName("cpu")[0].firstChild.data
                ram = capacidad_elemento.getElementsByTagName("ram")[0].firstChild.data
                almacenamiento = capacidad_elemento.getElementsByTagName("almacenamiento")[0].firstChild.data

                # Creamos el objeto CentroDatos y lo agregamos a la lista
                # Nota: el parametro capacidad no se usa en el constructor, solo los valores individuales
                nuevo_centro = CentroDatos(id_centro, nombre, pais, ciudad, 0, cpu, ram, almacenamiento)
                lista_centros.insertar(nuevo_centro)
                print(f"✓ Centro {id_centro} cargado")


            # ========== CARGANDO MAQUINAS VIRTUALES ==========
            vms = root.getElementsByTagName("configuracion")[0] \
                      .getElementsByTagName("maquinasVirtuales")[0] \
                      .getElementsByTagName("vm")

            for vm in vms:
                id_vm = vm.getAttribute("id")
                centro_asignado = vm.getAttribute("centroAsignado")

                # Obteniendo datos de la VM
                so = vm.getElementsByTagName("sistemaOperativo")[0].firstChild.data
                ip = vm.getElementsByTagName("ip")[0].firstChild.data

                # Obteniendo recursos de la VM
                recursos = vm.getElementsByTagName("recursos")[0]
                cpu = recursos.getElementsByTagName("cpu")[0].firstChild.data
                ram = recursos.getElementsByTagName("ram")[0].firstChild.data
                almacenamiento = recursos.getElementsByTagName("almacenamiento")[0].firstChild.data

                # Buscamos el centro al que pertenece esta VM
                centro_encontrado = self.buscar_centro_por_id(lista_centros, centro_asignado)
                
                if centro_encontrado is not None:
                    # Creamos la VM y la agregamos al centro correspondiente
                    exito, mensaje = centro_encontrado.crear_vm(id_vm, so, ip, cpu, ram, almacenamiento)
                    
                    if exito:
                        print(f"✓ VM {id_vm} cargada en {centro_asignado}")
                        
                        # Obtenemos la VM recien creada para agregarle los contenedores
                        vm_creada = self.buscar_vm_en_centro(centro_encontrado, id_vm)
                        
                        if vm_creada is not None:
                            # CARGANDO CONTENEDORES dentro de la VM
                            contenedores = vm.getElementsByTagName("contenedores")[0] \
                                             .getElementsByTagName("contenedor")

                            for contenedor in contenedores:
                                id_cont = contenedor.getAttribute("id")
                                nombre = contenedor.getElementsByTagName("nombre")[0].firstChild.data
                                imagen = contenedor.getElementsByTagName("imagen")[0].firstChild.data
                                puerto = contenedor.getElementsByTagName("puerto")[0].firstChild.data

                                # Obteniendo recursos del contenedor (CPU en %, RAM en MB)
                                rec = contenedor.getElementsByTagName("recursos")[0]
                                cpu_porcentaje = rec.getElementsByTagName("cpu")[0].firstChild.data
                                ram_mb = rec.getElementsByTagName("ram")[0].firstChild.data

                                # Agregamos el contenedor a la VM
                                exito_cont, mensaje_cont = vm_creada.agregar_contenedor(id_cont, nombre, imagen, puerto, cpu_porcentaje, ram_mb)
                                
                                if exito_cont:
                                    print(f"  ✓ Contenedor {id_cont} agregado a VM {id_vm}")
                                else:
                                    print(f"  ✗ Error al agregar contenedor {id_cont}: {mensaje_cont}")
                    else:
                        print(f"✗ Error al cargar VM {id_vm}: {mensaje}")
                else:
                    print(f"✗ Error: Centro {centro_asignado} no encontrado para VM {id_vm}")


            # ========== CARGANDO SOLICITUDES ==========
            solicitudes = root.getElementsByTagName("configuracion")[0] \
                              .getElementsByTagName("solicitudes")[0] \
                              .getElementsByTagName("solicitud")

            for solicitud in solicitudes:
                id_soli = solicitud.getAttribute("id")
                cliente_soli = solicitud.getElementsByTagName("cliente")[0].firstChild.data
                tipo_soli = solicitud.getElementsByTagName("tipo")[0].firstChild.data
                prioridad = solicitud.getElementsByTagName("prioridad")[0].firstChild.data
                tiempo_estimado = solicitud.getElementsByTagName("tiempoEstimado")[0].firstChild.data

                # Obteniendo recursos solicitados
                recursos = solicitud.getElementsByTagName("recursos")[0]
                cpu_s = recursos.getElementsByTagName("cpu")[0].firstChild.data
                ram_s = recursos.getElementsByTagName("ram")[0].firstChild.data
                alm_s = recursos.getElementsByTagName("almacenamiento")[0].firstChild.data

                # Creamos el objeto Solicitud y lo agregamos a la lista
                nueva_solicitud = Solicitud(id_soli, cliente_soli, tipo_soli, prioridad, cpu_s, ram_s, alm_s, tiempo_estimado)
                lista_solicitudes.insertar(nueva_solicitud)
                print(f"✓ Solicitud {id_soli} cargada")


            # ========== CARGANDO INSTRUCCIONES ==========
            instrucciones = root.getElementsByTagName("instrucciones")[0] \
                                 .getElementsByTagName("instruccion")

            for instr in instrucciones:
                tipo = instr.getAttribute("tipo")
                nueva_instruccion = Instruccion(tipo)

                # Recorremos todos los nodos hijos para extraer los parametros
                child = instr.firstChild
                while child is not None:
                    # Solo procesamos nodos tipo elemento (ignoramos texto/espacios)
                    if child.nodeType == child.ELEMENT_NODE:
                        nombre_parametro = child.tagName
                        valor_parametro = ""
                        
                        # Obtenemos el valor del parametro si existe
                        if child.firstChild is not None:
                            valor_parametro = child.firstChild.data
                        
                        # Agregamos el parametro a la instruccion
                        nueva_instruccion.agregar_parametro(nombre_parametro, valor_parametro)
                    
                    child = child.nextSibling
                
                # Agregamos la instruccion a la lista
                lista_instrucciones.insertar(nueva_instruccion)

            print('\n=== Ejecutando Instrucciones ===')
            
            # Retornamos las tres estructuras principales
            return lista_centros, lista_solicitudes, lista_instrucciones

        except Exception as e:
            print(f"Error al cargar el archivo XML: {e}")
            return None, None, None
    
    def buscar_centro_por_id(self, lista_centros, id_centro):
        """Busca un centro de datos por su ID en la lista de centros"""
        if lista_centros.primero is None:
            return None
        
        nodo_centro_actual = lista_centros.primero
        while nodo_centro_actual is not None:
            if nodo_centro_actual.dato.id_centro == id_centro:
                return nodo_centro_actual.dato
            nodo_centro_actual = nodo_centro_actual.siguiente
        
        return None
    
    def buscar_vm_en_centro(self, centro, id_vm):
        """Busca una maquina virtual por su ID dentro de un centro de datos"""
        if centro.maquinas_virtuales.primero is None:
            return None
        
        nodo_vm_actual = centro.maquinas_virtuales.primero
        while nodo_vm_actual is not None:
            if nodo_vm_actual.dato.id_vm == id_vm:
                return nodo_vm_actual.dato
            nodo_vm_actual = nodo_vm_actual.siguiente
        
        return None

