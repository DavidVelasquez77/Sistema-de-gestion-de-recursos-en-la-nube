from xml.dom import minidom
from modelos.CentroDatos import CentroDatos
from TDAs.ListaEnlazada import ListaEnlazada

class XMLReader:

    def analizar_archivoXML(self, ruta_archivo):
        try:
            doc = minidom.parse(ruta_archivo)
            root = doc.documentElement  # definiendo raíz: <cloudSync>
            listaCentros = ListaEnlazada()

            print('\n')
            print("="*50)
            print("CENTROS DE DATOS")

            #ACCEDIENDO A LOS CENTROS DE DATOS
            centros = root.getElementsByTagName("configuracion")[0] \
                          .getElementsByTagName("centrosDatos")[0] \
                          .getElementsByTagName("centro")

            for centro in centros:
                id_centro = centro.getAttribute("id")
                nombre = centro.getAttribute("nombre")

                # Ubicación
                ubicacion = centro.getElementsByTagName("ubicacion")[0]
                pais = ubicacion.getElementsByTagName("pais")[0].firstChild.data
                ciudad = ubicacion.getElementsByTagName("ciudad")[0].firstChild.data

                # Capacidad
                capacidad = centro.getElementsByTagName("capacidad")[0]
                cpu = capacidad.getElementsByTagName("cpu")[0].firstChild.data
                ram = capacidad.getElementsByTagName("ram")[0].firstChild.data
                almacenamiento = capacidad.getElementsByTagName("almacenamiento")[0].firstChild.data

                #creando objetos para agregarlos a la lista enlazada y mostrarlos
                nuevo_centro = CentroDatos(id_centro, nombre, pais, ciudad, capacidad, cpu, ram, almacenamiento)
                listaCentros.insertar(nuevo_centro)

            return listaCentros

            for centro in centros:
                print(f' Centro {centro.getAttribute('id')} cargado correcamente')

            # reconociendo máquinas virtuales
            print("\n" + "="*50)
            print("MÁQUINAS VIRTUALES")

            vms = root.getElementsByTagName("configuracion")[0] \
                      .getElementsByTagName("maquinasVirtuales")[0] \
                      .getElementsByTagName("vm")

            for vm in vms:
                id_vm = vm.getAttribute("id")
                centro_asignado = vm.getAttribute("centroAsignado")

                so = vm.getElementsByTagName("sistemaOperativo")[0].firstChild.data
                ip = vm.getElementsByTagName("ip")[0].firstChild.data

                recursos = vm.getElementsByTagName("recursos")[0]
                cpu = recursos.getElementsByTagName("cpu")[0].firstChild.data
                ram = recursos.getElementsByTagName("ram")[0].firstChild.data
                almacenamiento = recursos.getElementsByTagName("almacenamiento")[0].firstChild.data

                print(f'maquina virtual {vm.getAttribute('id')} cargada con sus especificaciones correctamente! ')

                # CONTENEDORES dentro de la VM
                contenedores = vm.getElementsByTagName("contenedores")[0] \
                                 .getElementsByTagName("contenedor")

                for contenedor in contenedores:
                    id_cont = contenedor.getAttribute("id")
                    nombre = contenedor.getElementsByTagName("nombre")[0].firstChild.data
                    imagen = contenedor.getElementsByTagName("imagen")[0].firstChild.data
                    puerto = contenedor.getElementsByTagName("puerto")[0].firstChild.data

                    rec = contenedor.getElementsByTagName("recursos")[0]
                    cpu_c = rec.getElementsByTagName("cpu")[0].firstChild.data
                    ram_c = rec.getElementsByTagName("ram")[0].firstChild.data

                    print(f'contenedor {contenedor.getAttribute('id')} cargado con sus especificacione correctamente! ')

            # reconociendo Solicitudes
            print("\n" + "="*50)
            print("SOLICITUDES")

            solicitudes = root.getElementsByTagName("configuracion")[0] \
                              .getElementsByTagName("solicitudes")[0] \
                              .getElementsByTagName("solicitud")

            for solicitud in solicitudes:
                id_soli = solicitud.getAttribute("id")
                cliente_soli = solicitud.getElementsByTagName("cliente")[0].firstChild.data
                tipo_soli = solicitud.getElementsByTagName("tipo")[0].firstChild.data
                prioridad = solicitud.getElementsByTagName("prioridad")[0].firstChild.data
                tiempo_estimado = solicitud.getElementsByTagName("tiempoEstimado")[0].firstChild.data

                recursos = solicitud.getElementsByTagName("recursos")[0]
                cpu_s = recursos.getElementsByTagName("cpu")[0].firstChild.data
                ram_s = recursos.getElementsByTagName("ram")[0].firstChild.data
                alm_s = recursos.getElementsByTagName("almacenamiento")[0].firstChild.data

                print(f'solicitud con id: {solicitud.getAttribute('id')} cargada con sus especificaciones correctamente! ')

            # --- INSTRUCCIONES ---
            print("\n" + "="*50)
            print("INSTRUCCIONES")

            instrucciones = root.getElementsByTagName("instrucciones")[0] \
                                 .getElementsByTagName("instruccion")

            for instr in instrucciones:
                tipo = instr.getAttribute("tipo")
                print(f"Instrucción tipo: {tipo}")

                for child in instr.childNodes:
                    if child.nodeType == child.ELEMENT_NODE:
                        valor = child.firstChild.data if child.firstChild else ""
                        print(f"   {child.tagName}: {valor}")

        except Exception as e:
            print("Error al cargar el archivo XML:", e)


    
    
