import sys
sys.path.append('../')
import xml.etree.ElementTree as ET
from ejercicio2.parse.parse_xml import parseXML
from zipfile import ZipFile
purl = '{http://purl.org/dc/elements/1.1/}'
namespace = '{http://www.idpf.org/2007/opf}'
outputfile = 'output.opf'
xmlheader = '<?xml version="1.0" encoding="utf-8" standalone="no"?>'

def editContents(raiz):
    yn = ""
    hijoset = set()
    while yn.lower() != 'n':
        metadata = raiz.find(namespace+'metadata')
        print('Que quieres editar: (En caso de que existan muchos contribuidores se te pedira el número del que quieres editar)\n')
        for hijo in metadata.findall('.//'):
            tag = hijo.tag.split('}')[1]
            hijoset.add(tag)
            print (tag)
        """
            metadata = raiz.find(namespace+'metadata')
            metadata.find(purl+'language').text = "es"
        """
        toedit = input()
        while toedit.lower() not in hijoset:
            toedit = input('Valor no admitido, por favor introduzca un valor correcto\n')
        if toedit.lower() == 'meta':
            meta = metadata.find(namespace+toedit.lower())
            print(f"Valor de {toedit.lower()} es {meta.text}")
            newval = input("Que valor quieres que tome: \n")
            meta.text = newval
        elif toedit.lower() == 'contributor':
            contributors = metadata.findall(purl+toedit)
            print(contributors)
            length = len(contributors)
            number = input(f"Que numero quieres editar: 0-{length-1}")
            contributor = contributors.find(purl+toedit.lower())[int(number)]
            print(f"Valor de {toedit.lower()} es {contributor.text}")
            newval = input("Que valor quieres que tome: \n")
            contributor.text = newval
        else: 
            element = metadata.find(purl+toedit.lower())
            print(f"Valor de {toedit.lower()} es {element.text}")
            newval = input("Que valor quieres que tome: \n")
            element.text = newval
        yn = input('¿Algo más? Y-N\n')
    return raiz

def finetunefile(opf_file): 
    finetune = open(outputfile,"r")
    lines = finetune.readlines()
    finetune.close()
    finetuned = open(opf_file,'w')
    finetuned.writelines(xmlheader+'\n')
    for line in lines:
        newline = line.replace("ns0:","")
        newline = newline.replace(':ns0',"")
        finetuned.writelines(newline)
    finetuned.close()

def main():
    """
        Por simplicidad por favor ponga el archivo en la misma carpeta que el script.
    """
    file = input('Escribe el nombre del archivo\n')
    name = file.replace('.epub','')
    unzipped_directory = 'unzipped_' + name
    package_opf_file = unzipped_directory + '/EPUB/package.opf'
    print (package_opf_file)

    with ZipFile(file) as zip_ref:
        zip_ref.extractall(unzipped_directory)

    cadena = parseXML(package_opf_file)
    raiz = cadena.getroot()
    editContents(raiz)
    cadena.write(outputfile)
    finetunefile(package_opf_file)


if __name__ == '__main__':
    main()