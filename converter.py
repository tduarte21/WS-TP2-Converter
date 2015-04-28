__author__ = 'Pedro Bordonhos'

import rdflib
from rdflib import ConjunctiveGraph
import grafo

def ConvertToRDFN3 (filename, destinationFileName):
    _graph = ConjunctiveGraph()
    _graph.parse(filename, format="nt")
    _graph.triples((None, None, None))

    of = open(destinationFileName, "wb")
    of.write(_graph.serialize(format="n3"))
    of.close()

def ConvertToRDFXML (filename,destinationFileName):
    _graph = ConjunctiveGraph()
    _graph.parse(filename, format="nt")
    _graph.triples((None, None, None))

    of = open(destinationFileName, "wb")
    of.write(_graph.serialize(format="pretty-xml"))
    of.close()

def ConvertToSQLLITE (filename,destinationFileName):

    _graph = ConjunctiveGraph()
    _graph.parse(filename, format="nt")
    _graph.triples((None, None, None))


    sql = ConjunctiveGraph('SQLite')
    sql.open(destinationFileName, create=True)

    for t in _graph.triples((None,None,None)):
        sql.add(t)

    sql.commit()
    sql.close()

def ConvertCSVToTN (filename, destinationFileName):
    g = grafo.grafo()
    g.load(filename)  #--> Working
    allTriples = g.search ((None, None, None))
    linha = ""
    tipos = []
    ntFile = open(destinationFileName, "w")
    for s, p, o in allTriples:
        linha = "<http://ws_22208_65138.com/" + s + "> "
        if str(p) != 'lat' and str(p)!= 'long':
            linha = linha  + "<http://xmlns.com/gah/0.1/"+str(p) + "> "
            if str(p) == "description":
                linha =  linha  +'"' + str (o) + '".'
            elif str(p) == "accidentID":
                linha =  linha  +'"' + str (o) + '"^^<http://www.w3.org/2001/XMLSchema#int>.'
            elif str(p) == "victimID":
                linha =  linha  +'"' + str (o) + '"^^<http://www.w3.org/2001/XMLSchema#int>.'
            elif str(p) == "dateOfAccident":
                linha =  linha  +'"' + str (o) + '"^^<http://www.w3.org/2001/XMLSchema#date>.'
            else:
                newObj = "<http://ws_22208_65138.com/" + str (o) + ">";
                if ( not newObj in tipos):
                    tipos.append("<http://ws_22208_65138.com/" + str (o) + ">");
                linha =  linha + newObj+"."
        else:
            linha = linha  + "<http://www.w3.org/2003/01/geo/wgs84_pos#" + str(p) +"> "
            #já se coloca também o objecto
            linha = linha + '"' + str(o) + '".'
        ntFile.write(linha +"\n");

    for tipo in tipos:
        linha = tipo + " <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
        elementos = str(tipo).split("/")
        linha = linha + "<http://xmlns.com/gah/0.1/" + elementos[len(elementos)-2] + ">."
        ntFile.write(linha +"\n");

    ntFile.close()



