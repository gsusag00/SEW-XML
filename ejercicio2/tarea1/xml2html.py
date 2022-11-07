import sys
sys.path.append('../')
from parse.parse_xml import parseXML
from yattag.doc import Doc
from yattag.indentation import indent
namespace = "{http://www.uniovi.es/personas}"
doc, tag, text, line = Doc().ttl()


def createHTML(cadena):
    estilo = './estilo.css' 
    raiz = cadena.getroot()
    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        doc.attr(lang='es')
        with tag('head'):
            doc.asis('<meta charset="UTF-8">')
            doc.asis('<link rel="stylesheet" href="estilo.css">')
            with tag('title'):
                text('Red Social.')
        with tag('body'):
            with tag('h1'):
                text('Red Social')
            persona = raiz.find(namespace+'persona')
            processPersona(persona,2)   
    return indent(doc.getvalue())

def processPersona(persona,header):
    nombre = persona.attrib['nombre']
    apellido = persona.attrib['apellidos']
    with tag('section'):
        with tag('h'+str(header)):
            text(nombre + ' ' + apellido)
        nacimiento = persona.find(namespace+"nacimiento")
        residencia = persona.find(namespace+"residencia")
        with tag('h' + str(header)):
            text('Nacimiento:')
        with tag('p'):
            text('Fecha: ' + nacimiento.attrib['fecha'])
        with tag('h' + str(header)):
            text('Lugar de nacimiento')
        with tag('p'):
            text('De: ' + nacimiento.attrib['lugar'])
        with tag('h' + str(header)):
            text('Lugar de residencia')
        with tag('p'):
            text('De: ' + residencia.attrib['lugar'])
        with tag('h' + str(header)):
            text('Fotos')
        with tag('aside'): 
            for fotografia in persona.find(namespace+"fotografias").findall(namespace+"fotografia"):
                with tag('picture'):
                    img = '<img src="' + fotografia.attrib["path"] + '" alt="Foto de ' + nombre + ' ' + apellido + '">'
                    doc.asis(img)
        if persona.find(namespace+'videos') != None:
            with tag('h' + str(header)):
                text('Videos')
            with tag('aside'):
                for video in persona.find(namespace+"videos").findall(namespace+"video"):
                    with tag('video'):
                        video = '<source src="' + video.attrib['path'] + '" type="video/mp4">'
                        doc.asis(video)
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
    doc.getvalue()

def main(): 
    
    file = input('Por favor introduce el archivo que quieres convertir a html\n')

    cadena = parseXML(file)

    archivoHTML = createHTML(cadena)
    archivo = open('redsocial.html','w')
    archivo.write(archivoHTML)
    archivo.close()

if __name__ == '__main__':
    main()



