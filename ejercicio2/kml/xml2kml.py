import xml.etree.ElementTree as ET
from yattag import Doc
from yattag import indent
namespace = "{http://www.uniovi.es/personas}"
doc, tag, text, line = Doc().ttl()
"""
    Parsea el xml, devuelve una lista con el xml paraseado
"""
def parseXML(file):
    try: 
        cadena = ET.parse(file)
    except IOError:
        print('No se encuentra el archivo')
        exit()
    except ET.ParseError:
        print('Error parseando el archivo xml.')
        exit()
    return cadena

def createKML(cadena):
    raiz = cadena.getroot()
    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
    with tag('kml'):
        doc.attr(xmlns="http://earth.google.com/kml/2.2")
        with tag('Document'):
            line('name',"Red Social")
            processPersona(raiz)   
    return indent(doc.getvalue())

def processPersona(persona):
    with tag('Placemark'):
        line('name',persona.attrib['nombre'] + ' ' + persona.attrib['apellidos'])
        with tag('Point'):
            coordenadas = persona.find(namespace+"nacimiento").find(namespace+"coordenadas")
            latitud = coordenadas.attrib['latitud']
            longitud = coordenadas.attrib['longitud']
            altitud = coordenadas.attrib['altitud']
            line('coordinates','\n' + str(longitud)+','+str(latitud)+',0\n')
    if persona.find(namespace+'amigos') != None:
        for amigo in persona.find(namespace+'amigos').findall(namespace+'persona'):
            processPersona(amigo)

def main(): 
    
    file = input('Por favor introduce el archivo que quieres convertir a kml\n')

    cadena = parseXML(file)

    archivoHTML = createKML(cadena)
    archivo = open('red_social.kml','w')
    archivo.write(archivoHTML)
    archivo.close()

if __name__ == '__main__':
    main()



