#importaciones
from XMLReader.xmlReader import XMLReader
from TDAs.ListaEnlazada import ListaEnlazada
from modelos.CentroDatos import CentroDatos



def menu():
    print('\n')
    print("="*50)
    print('CloudSync Manager - Sistema de la Nube')
    print("="*50)
    print('1. Cargar Archivo XML')
    print('2. Gestión de Centros de Datos')
    print('3. Gestión de Máquinas Virtuales')
    print('4. Gestión de Contenedores')
    print('5. Gestión de Solicitudes')
    print('6. Reportes en Graphviz')
    print('7. Generar XML de Salida')
    print('8. Historial de Operaciones')
    print('9. Salir')
    print("="*50)
    print('\n')
    opcion = input('Elige un opción de las que se muestra en el menú: ')

    if opcion == '1':
        ruta_archivo = input('ingresa la ruta del archivo XML: ')
        lectura = XMLReader()
        lista_centros = lectura.analizar_archivoXML(ruta_archivo)
        print('\n')
        print('Archivo cargado correctamente! ')
        menu()
        
    elif opcion == '2':
         def menuOpcion2():
            print('\n')
            print("="*50)
            print('Gestion de Centros de Datos')
            print("="*50)
            print('1. Listar todos los Centros')
            print('2. Buscar Centros por ID')
            print('3. Ver centro con más recursos')
            print('4. Regresar al menú Principal')
            print("="*50)
            opcion = input('seleccione una opción: ')
            
    elif opcion == '3':
        print('procedimiento de gestión de máquinas virtuales')
    
    elif opcion == '4':
        print('procedimiento de gestión de contenedores')

    elif opcion == '5':
        print('procedimiento de gestión de solicitudes')
    
    elif opcion == '6':
        print('procedimiento de reportes en Graphviz')

    elif opcion == '7':
        print('procedimiento de generar XML de salida')
    
    elif opcion == '8':
        print('procedimiento de mostrar historial de operaciones')
    
    elif opcion == '9':
        print('procedimiento de salir del programa')
    
    elif opcion:
        print('\n')
        print('Error: elige una opción entre el rango de 1 a 9')
        print(menu())




if __name__ == "__main__":
    print(menu())