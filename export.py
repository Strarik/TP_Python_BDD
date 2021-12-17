#Formatage au format .csv
def convertToCSV(list):
    delim = '\n'
    stringcsv = delim.join(map(str,list))
    stringcsv = stringcsv.replace('(','')
    stringcsv = stringcsv.replace(')','')
    stringcsv = stringcsv.replace(',',';')
    stringcsv = stringcsv.replace('\'','')
    stringcsv = stringcsv.replace('"','')
    return stringcsv

#Ecriture du fichier .csv
def export (data, path) :
    stringcsv = convertToCSV(data)

    with open(path, 'w') as file:
        file.write(stringcsv)