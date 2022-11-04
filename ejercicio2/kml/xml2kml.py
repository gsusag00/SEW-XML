import xml.etree.ElementTree as ET
from yattag import Doc
from yattag import indent
import codecs
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
    doc.asis('<!xml version="1.0" encoding="UTF-8"?>')
    with tag('kml'):
        doc.attr(xmlns="https://www.opengis.net/kml/2.2")
        with tag('head'):
            doc.stag('meta',charset='UTF-8')
            doc.stag('link', rel='stylesheet', href=estilo)
            with tag('title'):
                text('Red Social.')
        with tag('body'):
            with tag('h1'):
                text('Red Social')
            processPersona(raiz,2)   
    return indent(doc.getvalue())

def processPersona(persona,header):
    nombre = persona.attrib['nombre']
    apellido = persona.attrib['apellidos']
    with tag('h'+str(header)):
        text(nombre + ' ' + apellido)
    nacimiento = persona.find(namespace+"nacimiento")
    with tag('h' + str(header)):
        text('Nacimiento:')
    with tag('p'):
        text('Fecha: ' + nacimiento.attrib['fecha'])
    with tag('h' + str(header)):
        text('Lugar de nacimiento')
    with tag('p'):
        text('De: ' + nacimiento.attrib['lugar'])
    with tag('h' + str(header)):
        text('Fotos')
    for fotografia in persona.find(namespace+"fotografias").findall(namespace+"fotografia"):
        with tag('picture'):
            doc.stag('img',src=fotografia.attrib["path"], alt="Foto del " + nombre + " " + apellido)
    if persona.find(namespace+'videos') != None:
        with tag('h' + str(header)):
            text('Videos')
        for video in persona.find(namespace+"videos").findall(namespace+"video"):
            with tag('video'):
                doc.stag('source',src=video.attrib["path"], type='video/mp4')
    with tag('h'+str(header)):
        text('Comentarios: ')
    for comentario in persona.find(namespace+"comentarios").findall(namespace+"comentario"):
        with tag('p'):
            text("Comentario: " + comentario.attrib["valor"])
    if persona.find(namespace+"amigos") != None:
        with tag('h'+str(header)):
            text('Amigos')
        for amigo in persona.find(namespace+"amigos").findall(namespace+"persona"):
            processPersona(amigo,header+1)
    indent(doc.getvalue())

def main(): 
    
    file = input('Por favor introduce el archivo que quieres convertir a html\n')

    cadena = parseXML(file)

    archivoHTML = createHTML(cadena)
    archivo = open('redsocial.html','w')
    archivo.write(archivoHTML)
    archivo.close()

if __name__ == '__main__':
    main()



