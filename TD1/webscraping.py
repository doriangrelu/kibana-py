import certifi
import urllib3
import time, random
from bs4 import BeautifulSoup

page_html = """<html><head></head><body><p class="bold-paragraph">Voilà un paragraphe<a href="https://www.meteociel.fr/" id="identifiant1">Un lien intéressant pour scrapper des données web</a></p><p class="bold-paragraph extra-large">Voilà un deuxième paragraphe<a href="https://www.python.org/downloads/" class="extra-large">Pour télécharger la dernière version de python</a></p><table class="table-datas"><tr><td>Date</td><td>Tmax</td><td>Tmin</td></tr><tr><td>12-01-2018</td><td>18.2</td><td>8.7</td></tr><tr><td>13-01-2018</td><td>17.5</td><td>9.3</td></tr><tr><td>14-01-2018</td><td>18</td><td>9.2</td></tr></table></body></html>"""

if __name__ == "__main__":
    requete_http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    url = "https://www.meteociel.fr/cartes_obs/climato2v4.php"
    method = 'GET'
    response = requete_http.request(method, url, fields={"code": 103, "mois": 4, "annee": 2018, "print": 1})
    mois = [1,2,3,4,5,6,7,8,9,10,11,12]
    if (response.status == 200):
        response = requete_http.request(method, url, fields={"code": 103, "mois": 4, "annee": 2018, "print": 1})
        print("---------- AVRIL 2018 ---------- \n")
        soup = BeautifulSoup(response.data, features="html.parser")
        for script in soup(["script", "style"]):
            script.extract()
            allTrTags = soup.find_all('tr')[2:]
            for trTag in allTrTags:
                alltdTags = trTag.find_all('td')
                if (len(alltdTags) > 3):
                    jour = alltdTags[0].text.strip()
                    tempMax = alltdTags[1].text.strip().split('°')[0]
                    tempMin = alltdTags[2].text.strip().split('°')[0]
                    precipitation = alltdTags[3].text.strip()
                    print(
                        "Jour : " + jour + " : \t - température maximum : " + tempMax + " \t - température minimum : " + tempMin + " \t - précipitation : " + precipitation + "\n")
                pass
            pass
