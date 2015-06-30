
# -*- encoding: utf-8 -*-
"""
    pyTraslate v0.1.2015.29.06
    Este programa esta dedicado a convertir código escrito en el lenguaje HTML a texto plano

"""

# Se importa todos los elementos de plex
from plex import *
import urllib2

class Analyzer(Scanner):

    def __init__(self):

        """
        Se definen las expresiones regulares para analizar el archivo
        """
        #dl: Busca expresiones que inicien con <dl> y terminen con </dl>
        dl = Str("<dl>") + Rep(AnyBut("</dl>"))
        #dt: Busca expresiones que inicien con <dt> y terminen con </dt>
        dt = Str("<dt>") + Rep(AnyBut("</dt>"))
        #dd: Busca expresiones que inicien con <dd> y terminen con </dd>
        dd = Str("<dd>") + Rep(AnyBut("</dd>"))

        txt = Rep(AnyBut("\n"))

        #lexicon1 y lexicon2 servira para hacer las comparaciones en el archivo a leer
        self.lexicon1 = Lexicon([
            (dl, 'DescriptionList'),
            (txt, IGNORE)
        ])

        self.lexicon2 = Lexicon([
            (dt, 'DefinesTerms'),
            (dd, 'DefinesDescriptions')
        ])

        #analizer: Guarda la informacion del escaner del documento
        self.analizer = ''

        #txt: permite la comunicacion con el archivo txt
        self.txt = ''

        #displays: Almacena cada una de las tuplas encontradas por el lexicon1
        self.displays = []
        #displays2: Almacena cada una de las tuplas encontradas por el lexicon2
        self.displays2 = []
        #symbolTable: es la tabla de simbolos
        self.symbolTable = []

    """
        Este metodo de clase tiene como fin el leer el archivo HTML desde la URL utilizando la libreria urllib2
    """
    def ReadHTML(self):
        f = urllib2.urlopen("https://docs.python.org/3/glossary.html")
        html = f.read()
        self.createAndFillHTML(html)
        filename = 'contentHTML.html'
        f = open(filename, 'r')
        self.analizer = Scanner(self.lexicon1, f, filename)

    """
        Este metodo de clase tiene como fin el leer el archivo help el cual contiene la lineas a que contiene un dl
    """
    def readHELP(self):
        filename = 'help.html'
        f = open(filename, 'r')
        self.analizer = Scanner(self.lexicon2, f, filename)

    """
        La funcionalidad de este metodo de clase es la de crear un archivo .txt donde se guardara las acciones tomadas
        gracias a plex y codificacion personal
    """
    def createTXT(self):
        self.txt = open('output.txt', 'w')
        self.txt.close()

    """
        Este metodo de clase tiene como fin crear un archivo de ayuda help.html en el cual se almacenara lineas para
        ser analizadas por plex, esto en ayuda de la lectura y resolucion del ejercicio planteado
    """
    def createHELP(self):
        help = open('help.html', 'w')
        help.close()

    """
        Este metodo permite crear y llenar inmediatamente el archivo HTML, el cual es la informacion tomada desde la
        pagina web gracias a la libreria urllib2
    """
    def createAndFillHTML(self, html):
        file = open('contentHTML.html', 'w')
        file.close()
        file = open('contentHTML.html', 'a')
        file.write(html)

    """
        EL metodo fillDisplays tiene como fin llenar arreglos de diplays (muestras) donde los valores son las tuplas
        leidas por plex utilizando el lexicon
    """
    def fillDisplays(self, type):
        while 1:
            element = self.analizer.read()
            if type:
                self.displays.append(element)
            else:
                self.displays2.append(element)
            if element[0] is None:
                break

    """
        fillTXT es un metodo que permite el analisis y llenado de la tabla de simbolos recolectada a traves de toda
        la informacion recolectada desde el archivo html
    """

    def fillTXT(self):
        self.txt = open('output.txt', 'a')

        for element in self.displays:
            if element[0] == 'DescriptionList':
                self.validateDescriptionList(element[1])
            if element[0] is None:
                break

        for items in self.symbolTable:
            self.txt.write('-'*60)
            self.txt.write(items[0] + "\n")
            self.txt.write(items[1] + "\n")
            print '-'*60
            print items[0] + "\n"
            print items[1] + "\n"

        self.txt.close()

    """
        fillHELP permite llenar el archivo de ayuda llamado help.html con el fin de ser leido por plex y analizado a
        traves de lexicon2
    """
    def fillHELP(self, element):
        help = open('help.html', 'w')
        help.close()
        help = open('help.html', 'a')
        help.write(element)
        help.close()


    """
        Gracias a este metodo se pueden validar las DescriptionList y a traves de estas validar las demas opciones
    """
    def validateDescriptionList(self, element):
        cantchars = 0
        for char in element:
            if char != '>':
                cantchars += 1
            else:
                break

        text = element[cantchars+1:len(element) - 5]
        self.createHELP()
        self.fillHELP(text)
        self.readHELP()
        self.fillDisplays(False)
        self.validateHELP()

    """
        Debido a este metodo se pueden validar las DefinesTerms y las DefinesDescriptions pertenecientes a la dl
        encontrada anteriormente
    """
    def validateDefinesTermsANDDefinesDescriptions(self, element):
        cantchars = 0
        for char in element:
            if char != '>':
                cantchars += 1
            else:
                break

        text = element[cantchars+1:len(element) - 5]
        return text

    """
        Este metodo permite validar lo encontrado en el archivo help.html
    """
    def validateHELP(self):
        for element in len(self.displays2):
            dt = ""
            dd = ""
            if self.displays2[element][0] == 'DefinesTerms':
                dt = validateDefinesTermsANDDefinesDescriptions(self.displays2[element][1])
                if self.displays2[element + 1][0] == 'DefinesDescriptions':
                    dd = validateDefinesTermsANDDefinesDescriptions(self.displays2[element][1])
                    element += 1
            if self.displays2[element][0] == 'DefinesDescriptions':
                dd = validateDefinesTermsANDDefinesDescriptions(self.displays2[element][1])

            self.symbolTable.append((dt, dd))
            if self.displays2[element][0] is None:
                break

    """
        Este es el metodo principal del programa, es el primero en ejecutarse y llevar la secuencia de todo el ciclo
        de instrucciones
    """
    def start(self):
        self.ReadHTML()
        self.createTXT()
        self.fillDisplays(True)
        self.fillTXT()

#Inicializamos una variable y comenzamos la ejecucion del programa
analizer = Analyzer()
analizer.start()
