import xml.etree.ElementTree as ET

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