import sys
sys.path.append('../')
from parse.parse_xml import parseXML
from yattag.doc import Doc
from yattag.indentation import indent
import codecs
namespace = "{http://www.uniovi.es/personas}"
doc, tag, text, line = Doc().ttl()
initialx = 20
initialy = 20
width = 200
height = 80
rectstyle = "fill:white; stroke:black;stroke-width:1"
linestyle = "fill:transparent;stroke:black"
personstyle = "fill:blue"
textstyle = "fill:black"

def createSVG(cadena):
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
    #residencia
    residencia = persona.find(namespace+'residencia')
    with tag('text', x=str(xpos+10), y=str(ypos+75), style=textstyle):
        text('Vive en: ' + residencia.attrib['lugar'])
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

    archivoSVG = createSVG(cadena)
    archivo = open('redsocial.svg','w')
    archivo.write(archivoSVG)
    archivo.close()

if __name__ == '__main__':
    main()



