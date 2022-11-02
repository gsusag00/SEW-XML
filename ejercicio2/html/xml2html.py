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

def createHTML(cadena):
    estilo = '.\estilo.css' 
    raiz = cadena.getroot()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang='es')
        with tag('head'):
            doc.stag('meta',charset='UTF-8')
            doc.stag('link', rel='stylesheet', href=estilo)
            with tag('title'):
                text('Red Social.')
        with tag('body'):
            with tag('h1'):
                text('Red Social')
            with tag('h2'):
                text(raiz.attrib['nombre'] + ' ' + raiz.attrib['apellidos'])
            nacimiento = raiz.find(namespace+"nacimiento")
            with tag('p'):
                text('Nacimiento: ' + nacimiento.attrib['fecha'])
            with tag('p'):
                text('De: ' + nacimiento.attrib['lugar'])
            for fotografia in raiz.find(namespace+"fotografias").findall(namespace+"fotografia"):
                doc.stag('img',src=fotografia.attrib["path"], alt="Foto del individuo")
            for video in raiz.find(namespace+"videos").findall(namespace+"video"):
                doc.stag('video',src=video.attrib["path"])
            with tag('p'):
                text('Comentarios: ')
            for comentario in raiz.find(namespace+"comentarios").findall(namespace+"comentario"):
                with tag('p'):
                    text("Comentario: " + comentario.attrib["valor"])
            with tag('h2'):
                text('Amigos')
            for amigo in raiz.find(namespace+"amigos").findall(namespace+"persona"):
                print (amigo.attrib["nombre"])
            
    return indent(doc.getvalue())


def main(): 
    
    file = input('Por favor introduce el archivo que quieres convertir a html\n')

    cadena = parseXML(file)

    archivoHTML = createHTML(cadena)
    archivo = open('redsocial.html','w')
    archivo.write(archivoHTML)
    archivo.close()

if __name__ == '__main__':
    main()



