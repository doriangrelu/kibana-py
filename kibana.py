import certifi
import urllib3
import csv
import json
from elasticsearch import Elasticsearch


def nom_examen_csv(type, sexe):
    if sexe == '':
        return "PISA: Mean performance on the reading scale"
    return "PISA: Mean performance on the " + type + " scale. " + sexe


def extract_nom_exem(chaine):
    if nom_examen_csv('mathematics', 'Male') == chaine or nom_examen_csv('mathematics', 'Female') == chaine:
        return 'Maths'

    if nom_examen_csv('science', 'Male') == chaine or nom_examen_csv('science', 'Female') == chaine:
        return 'Science'

    if nom_examen_csv('reading', 'Male') == chaine or nom_examen_csv('reading', 'Female') == chaine:
        return 'Lecture'
    return ''


def extract_sexe_exem(examen, chaine):
    exploded = chaine.split('.')
    if len(exploded) != 2:
        return ''

    if exploded[1].strip() == 'Male':
        return 'Garcon'
    return 'Fille'


if __name__ == "__main__":
    # http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    # response = http.request("PUT", "http://127.0.0.1:9200/mabiblio/_doc/iban14226",
    #                        body="""{"iban":14226,"titre":"Le grand prince","langue":"Francais, RUSSE","auteur":"Arnale"}""",
    #                        headers={"Content-Type": "application/json"})
    # responseJson = json.loads(response.data)
    # print(json.dumps(responseJson, indent=4, sort_keys=True))
    paysVoulus = {"ARG": "Argentine", "BRA": "Bresil", "FRA": "France", "JPN": "Japon", "JORD": "Jordanie",
                  "KAZ": "Kazakshtan", "KOR": "Corée du sud", "MEX": "Mexique ", "RUS": "Russie", "TUR": "Turquie"}

    dicoGlobal = {}

    ocde = ['FRA', 'TUR', 'MEX', 'JPN', 'KOR']

    lazyPib = {}

    with open('storage/PIB.csv', 'r') as data:
        data_dict = csv.reader(data, delimiter=',', lineterminator='\n')
        i = 0
        for lines in data_dict:
            if i == 0:
                i += 1
                continue
            lazyPib[lines[3]] = {
                'pib_2012': lines[4],
                'pib_2015': lines[5],
                'pib_2018': lines[6]
            }

    anneesVoulus = [2015, 2016, 2017, 2018]
    es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])
    with open('storage/DATA_PISA.csv', 'r') as data:
        data_dict = csv.reader(data, delimiter=',', lineterminator='\n')
        i = 0
        for lines in data_dict:
            if i == 0:
                i += 1
                continue
            dico = {}
            codePays = lines[1]
            exam = extract_nom_exem(lines[2])

            if codePays not in paysVoulus or exam == '':
                continue
            nomPays = paysVoulus[codePays]
            dico['pays'] = nomPays
            dico['exemen'] = extract_nom_exem(lines[2])
            dico['sexe'] = extract_sexe_exem(exam, lines[2])

            dico['resultats_2012'] = lines[4]
            dico['resultats_2015'] = lines[5]
            dico['resultats_2018'] = lines[6]

            isocde = 0
            if (codePays in ocde):
                isocde = 1

            dico['is_ocde'] = isocde

            if (codePays in lazyPib):
                dico.update(lazyPib[codePays])

            print(dico)
            es.index(index='pisa', body=json.dumps(dico))
