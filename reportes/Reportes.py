import subprocess
import os

class GeneradorReportes:
    def __init__(self, lista_centros, gestor_solicitudes):
        self.lista_centros = lista_centros
        self.gestor_solicitudes = gestor_solicitudes
        self.dot_exe = r'C:\Program Files\Graphviz\bin\dot.exe'
    
    def _generar_png(self, archivo_dot, archivo_png):
        try:
            # Usamos string con espacios en vez de lista
            comando = f'"{self.dot_exe}" -Tpng "{archivo_dot}" -o "{archivo_png}"'
            subprocess.run(comando, shell=True, check=True, capture_output=True)
            return True
        except:
            return False
    
    def generar_reporte_centros(self):
        dot_content = 'digraph CentrosDatos {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled];\n'
        dot_content += '    graph [bgcolor=white, fontname="Arial", fontsize=12];\n'
        dot_content += '    \n'
        dot_content += '    titulo [label="CENTROS DE DATOS", shape=ellipse, fillcolor=lightsalmon, fontsize=16, fontname="Arial Bold"];\n'
        dot_content += '    \n'
        
        nodo_centro = self.lista_centros.primero
        contador = 0
        
        while nodo_centro is not None:
            centro = nodo_centro.dato
            contador += 1
            
            cpu_usado = centro.recursos.cpu_usado
            cpu_total = centro.recursos.cpu_total
            cpu_porcentaje = (cpu_usado / cpu_total * 100) if cpu_total > 0 else 0
            
            ram_usado = centro.recursos.ram_usado
            ram_total = centro.recursos.ram_total
            ram_porcentaje = (ram_usado / ram_total * 100) if ram_total > 0 else 0
            
            color = 'lightyellow'
            if cpu_porcentaje > 75 or ram_porcentaje > 75:
                color = 'orange'
            if cpu_porcentaje > 90 or ram_porcentaje > 90:
                color = 'tomato'
            
            label = f'{centro.id_centro}\\n{centro.nombre}\\n'
            label += f'{centro.ciudad}, {centro.pais}\\n\\n'
            label += f'CPU: {cpu_usado}/{cpu_total} ({cpu_porcentaje:.1f}%)\\n'
            label += f'RAM: {ram_usado}/{ram_total} GB ({ram_porcentaje:.1f}%)\\n'
            label += f'VMs: {centro.maquinas_virtuales.size}'
            
            dot_content += f'    centro{contador} [label="{label}", fillcolor={color}];\n'
            dot_content += f'    titulo -> centro{contador};\n'
            
            nodo_centro = nodo_centro.siguiente
        
        dot_content += '}\n'
        
        try:
            archivo = open('reportes/reporte_centros.dot', 'w', encoding='utf-8')
            archivo.write(dot_content)
            archivo.close()
            
            try:
                if self._generar_png('reportes/reporte_centros.dot', 'reportes/reporte_centros.png'):
                    return True, 'reportes/reporte_centros.png'
                else:
                    return True, 'reportes/reporte_centros.dot'
            except Exception as e:
                print(f'   [Aviso: No se pudo generar PNG - {str(e)}]')
                return True, 'reportes/reporte_centros.dot'
        except Exception as error:
            return False, str(error)
    
    def generar_reporte_vms_centro(self, id_centro):
        """Genera reporte de VMs de un centro especifico"""
        nodo_centro = self.lista_centros.primero
        centro_encontrado = None
        
        while nodo_centro is not None:
            if nodo_centro.dato.id_centro == id_centro:
                centro_encontrado = nodo_centro.dato
                break
            nodo_centro = nodo_centro.siguiente
        
        if centro_encontrado is None:
            return False, f'Centro {id_centro} no encontrado'
        
        dot_content = 'digraph VMsCentro {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled];\n'
        dot_content += '    graph [bgcolor=white, fontname="Arial"];\n'
        dot_content += '    \n'
        
        label_titulo = f'MAQUINAS VIRTUALES\\n{centro_encontrado.nombre}'
        dot_content += f'    centro [label="{label_titulo}", shape=ellipse, fillcolor=peachpuff, fontsize=14, fontname="Arial Bold"];\n'
        dot_content += '    \n'
        
        if centro_encontrado.maquinas_virtuales.size == 0:
            dot_content += '    vacio [label="No hay VMs en este centro", shape=note, fillcolor=lightyellow];\n'
            dot_content += '    centro -> vacio;\n'
        else:
            nodo_vm = centro_encontrado.maquinas_virtuales.primero
            contador = 0
            
            while nodo_vm is not None:
                vm = nodo_vm.dato
                contador += 1
                
                label = f'{vm.id_vm}\\n{vm.sistema_operativo}\\n'
                label += f'IP: {vm.ip}\\n'
                label += f'CPU: {vm.recursos.cpu_total} nucleos\\n'
                label += f'RAM: {vm.recursos.ram_total} GB\\n'
                label += f'Contenedores: {vm.contenedores.size}'
                
                color = 'lightsalmon' if vm.contenedores.size > 0 else 'moccasin'
                
                dot_content += f'    vm{contador} [label="{label}", fillcolor={color}];\n'
                dot_content += f'    centro -> vm{contador};\n'
                
                nodo_vm = nodo_vm.siguiente
        
        dot_content += '}\n'
        
        nombre_archivo_dot = f'reportes/reporte_vms_{id_centro}.dot'
        nombre_archivo_png = f'reportes/reporte_vms_{id_centro}.png'
        try:
            archivo = open(nombre_archivo_dot, 'w', encoding='utf-8')
            archivo.write(dot_content)
            archivo.close()
            
            try:
                if self._generar_png(nombre_archivo_dot, nombre_archivo_png):
                    return True, nombre_archivo_png
                else:
                    return True, nombre_archivo_dot
            except Exception as e:
                print(f'   [Aviso: No se pudo generar PNG - {str(e)}]')
                return True, nombre_archivo_dot
        except Exception as error:
            return False, str(error)
    
    def generar_reporte_contenedores_vm(self, id_vm):
        nodo_centro = self.lista_centros.primero
        vm_encontrada = None
        centro_nombre = ""
        
        while nodo_centro is not None:
            centro = nodo_centro.dato
            nodo_vm = centro.maquinas_virtuales.primero
            
            while nodo_vm is not None:
                if nodo_vm.dato.id_vm == id_vm:
                    vm_encontrada = nodo_vm.dato
                    centro_nombre = centro.nombre
                    break
                nodo_vm = nodo_vm.siguiente
            
            if vm_encontrada is not None:
                break
            nodo_centro = nodo_centro.siguiente
        
        if vm_encontrada is None:
            return False, f'VM {id_vm} no encontrada'
        
        dot_content = 'digraph ContenedoresVM {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled];\n'
        dot_content += '    graph [bgcolor=white, fontname="Arial"];\n'
        dot_content += '    \n'
        
        label_vm = f'VM: {vm_encontrada.id_vm}\\n{vm_encontrada.sistema_operativo}\\n{centro_nombre}'
        dot_content += f'    vm [label="{label_vm}", shape=ellipse, fillcolor=lightsalmon, fontsize=14, fontname="Arial Bold"];\n'
        dot_content += '    \n'
        
        if vm_encontrada.contenedores.size == 0:
            dot_content += '    vacio [label="No hay contenedores en esta VM", shape=note, fillcolor=lightyellow];\n'
            dot_content += '    vm -> vacio;\n'
        else:
            nodo_cont = vm_encontrada.contenedores.primero
            contador = 0
            
            while nodo_cont is not None:
                cont = nodo_cont.dato
                contador += 1
                
                label = f'{cont.id_contenedor}\\n{cont.nombre}\\n'
                label += f'Imagen: {cont.imagen}\\n'
                label += f'Puerto: {cont.puerto}\\n'
                label += f'CPU: {cont.cpu_porcentaje}%\\n'
                label += f'RAM: {cont.ram_mb} MB\\n'
                label += f'Estado: {cont.estado}'
                
                color = 'lightpink'
                if cont.estado == 'Pausado':
                    color = 'gold'
                elif cont.estado == 'Detenido':
                    color = 'peachpuff'
                elif cont.estado == 'Reiniciando':
                    color = 'coral'
                
                dot_content += f'    cont{contador} [label="{label}", fillcolor={color}, shape=component];\n'
                dot_content += f'    vm -> cont{contador};\n'
                
                nodo_cont = nodo_cont.siguiente
        
        dot_content += '}\n'
        
        nombre_archivo_dot = f'reportes/reporte_contenedores_{id_vm}.dot'
        nombre_archivo_png = f'reportes/reporte_contenedores_{id_vm}.png'
        try:
            archivo = open(nombre_archivo_dot, 'w', encoding='utf-8')
            archivo.write(dot_content)
            archivo.close()
            
            try:
                if self._generar_png(nombre_archivo_dot, nombre_archivo_png):
                    return True, nombre_archivo_png
                else:
                    return True, nombre_archivo_dot
            except Exception as e:
                print(f'   [Aviso: No se pudo generar PNG - {str(e)}]')
                return True, nombre_archivo_dot
        except Exception as error:
            return False, str(error)
    
    def generar_reporte_cola_solicitudes(self):
        dot_content = 'digraph ColaSolicitudes {\n'
        dot_content += '    rankdir=TB;\n'
        dot_content += '    node [shape=box, style=filled];\n'
        dot_content += '    graph [bgcolor=white, fontname="Arial"];\n'
        dot_content += '    \n'
        dot_content += '    titulo [label="COLA DE SOLICITUDES\\n(Mayor a Menor Prioridad)", shape=ellipse, fillcolor=lightsalmon, fontsize=14, fontname="Arial Bold"];\n'
        dot_content += '    \n'
        
        if self.gestor_solicitudes.cola_solicitudes.esta_vacia():
            dot_content += '    vacio [label="No hay solicitudes pendientes", shape=note, fillcolor=lightyellow];\n'
            dot_content += '    titulo -> vacio;\n'
        else:
            nodo_solicitud = self.gestor_solicitudes.cola_solicitudes.primero
            contador = 0
            nodo_anterior = 'titulo'
            
            while nodo_solicitud is not None:
                solicitud = nodo_solicitud.dato
                contador += 1
                
                label = f'Prioridad: {solicitud.prioridad}\\n'
                label += f'{solicitud.id_solicitud}\\n'
                label += f'Cliente: {solicitud.cliente}\\n'
                label += f'Tipo: {solicitud.tipo}\\n'
                label += f'CPU: {solicitud.cpu} | RAM: {solicitud.ram} GB'
                
                color = 'tomato'
                if solicitud.prioridad >= 8:
                    color = 'tomato'
                elif solicitud.prioridad >= 5:
                    color = 'orange'
                else:
                    color = 'gold'
                
                dot_content += f'    sol{contador} [label="{label}", fillcolor={color}];\n'
                dot_content += f'    {nodo_anterior} -> sol{contador};\n'
                
                nodo_anterior = f'sol{contador}'
                nodo_solicitud = nodo_solicitud.siguiente
        
        dot_content += '}\n'
        
        try:
            archivo = open('reportes/reporte_cola_solicitudes.dot', 'w', encoding='utf-8')
            archivo.write(dot_content)
            archivo.close()
            
            # Generar PNG automáticamente
            try:
                if self._generar_png('reportes/reporte_cola_solicitudes.dot', 'reportes/reporte_cola_solicitudes.png'):
                    return True, 'reportes/reporte_cola_solicitudes.png'
                else:
                    return True, 'reportes/reporte_cola_solicitudes.dot'
            except Exception as e:
                print(f'   [Aviso: No se pudo generar PNG - {str(e)}]')
                return True, 'reportes/reporte_cola_solicitudes.dot'
        except Exception as error:
            return False, str(error)
