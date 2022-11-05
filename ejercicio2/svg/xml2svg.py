import xml.etree.ElementTree as ET
from yattag import Doc
from yattag import indent
import codecs
namespace = "{http://www.uniovi.es/personas}"
doc, tag, text, line = Doc().ttl()
initialx = 20
initialy = 20
width = 200
height = 70
rectstyle = "fill:white; stroke:black;stroke-width:1"
linestyle = "fill:transparent;stroke:black"
personstyle = "fill:blue"
textstyle = "fill:black"
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
    raiz = cadena.getroot()
    doc.asis('<?xml version="1.0" encoding="UTF-8"?>')
    with tag('svg'):
        doc.attr(width='2000')
        doc.attr(height='2000')
        doc.attr(style='overflow:visible')
        doc.attr(version='1.1')
        doc.attr(xmlns='http://www.w3.org/2000/svg')
        drawRecs(raiz,initialx,initialy,3)   
    return indent(doc.getvalue())

def drawRecs(persona,xpos,ypos,mult):
    doc.stag('rect',x=str(xpos), y=str(ypos), width=str(width), height=str(height),style=rectstyle)
    #persona
    with tag('text', x=str(xpos+10), y=str(ypos+15), style=personstyle):
        text('Persona')
    #nombre
    with tag('text', x=str(xpos+10), y=str(ypos+30), style=textstyle):
        text(persona.attrib['nombre'] + ' ' + persona.attrib['apellidos'])
    #lugar
    nacimiento = persona.find(namespace+"nacimiento")
    with tag('text', x=str(xpos+10), y=str(ypos+45), style=textstyle):
        text('De: ' + nacimiento.attrib['lugar'])
    #fecha
    with tag('text', x=str(xpos+10), y=str(ypos+60), style=textstyle):
        text('Nacimiento: ' + nacimiento.attrib['fecha'])
    if persona.find(namespace+"amigos") != None:
        prevypos = ypos
        for amigo in persona.find(namespace+"amigos").findall(namespace+"persona"):
            drawRecs(amigo,xpos+230,ypos,1)
            drawLine(xpos,ypos,prevypos)
            ypos += (100 * mult)
    indent(doc.getvalue())

def drawLine(xpos,ypos,prevypos):
    doc.stag('line',x1=str(xpos+width),y1=str(prevypos+(height/2)),x2=str(xpos+230),y2=str(ypos+(height/2)),style=linestyle)

def main(): 
    
    file = input('Por favor introduce el archivo que quieres convertir a svg\n')

    cadena = parseXML(file)

    archivoHTML = createHTML(cadena)
    archivo = open('redsocial.svg','w')
    archivo.write(archivoHTML)
    archivo.close()

if __name__ == '__main__':
    main()



