__author__ = '22208_65138'

import converter

flag = True

while flag:
    print('\n --=== MENU ===--')
    print('1 - Converter Dados') #Converter dados noutros formatos
    print('X - Terminar')
    n = input('Opção: ')
    if n.strip().upper() == 'X':
        flag = False

    if n.strip() == '1':
        key = 'Z';
        while key.upper() != 'X':
            print('\n --=== Converter Ficheiro ===--')
            print('1 - CSV --> RDF/NT')
            print('2 - RDF/NT -->  RDF/N3')
            print('3 - RDF/NT --> RDF/XML')
            print('4 - RDF/NT --> SQLITE')
            print('X - Menu anterior')
            key = input('Opção')

            if key == '1':
                converter.ConvertCSVToTN ("Dados\\roadaccidents.csv","Dados\\roadaccidents.nt")
            if key == '2':
                converter.ConvertToRDFN3 ("Dados\\roadaccidents.nt", "Dados\\roadaccidents.n3")
            if key == '3':
                converter.ConvertToRDFXML ("Dados\\roadaccidents.nt","Dados\\roadaccidents.xml")
            if key == '4':
                converter.ConvertToSQLLITE ("Dados\\roadaccidents.nt","Dados\\roadaccidents.db")