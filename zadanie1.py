import os
import logging
from datetime import datetime
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(message)s')

PORT = 2137
KLUCZYK = os.environ.get('OPENWEATHER_API_KEY')

miasta = [
    # polska
    {"country": "PL", "city": "Warszawa"},
    {"country": "PL", "city": "Kraków"},
    {"country": "PL", "city": "Łódź"},
    {"country": "PL", "city": "Wrocław"},
    {"country": "PL", "city": "Poznań"},
    {"country": "PL", "city": "Gdańsk"},
    {"country": "PL", "city": "Szczecin"},
    {"country": "PL", "city": "Bydgoszcz"},
    {"country": "PL", "city": "Lublin"},
    {"country": "PL", "city": "Białystok"},
    {"country": "PL", "city": "Katowice"},
    {"country": "PL", "city": "Gdynia"},
    {"country": "PL", "city": "Częstochowa"},
    {"country": "PL", "city": "Radom"},
    {"country": "PL", "city": "Rzeszów"},
    {"country": "PL", "city": "Toruń"},
    # europa
    {"country": "DE", "city": "Berlin"},
    {"country": "DE", "city": "Hamburg"},
    {"country": "DE", "city": "Frankfurt"},
    {"country": "FR", "city": "Paryż"},
    {"country": "FR", "city": "Lyon"},
    {"country": "GB", "city": "Londyn"},
    {"country": "GB", "city": "Liverpool"},
    {"country": "IT", "city": "Rzym"},
    {"country": "IT", "city": "Florencja"},
    {"country": "ES", "city": "Madryt"},
    {"country": "ES", "city": "Walencja"},
    {"country": "PT", "city": "Lizbona"},
    {"country": "PT", "city": "Porto"},
    {"country": "NL", "city": "Amsterdam"},
    {"country": "NL", "city": "Rotterdam"},
    {"country": "BE", "city": "Bruksela"},
    {"country": "CH", "city": "Zurych"},
    {"country": "CH", "city": "Genewa"},
    {"country": "AT", "city": "Wiedeń"},
    {"country": "CZ", "city": "Praga"},
    {"country": "HU", "city": "Budapeszt"},
    {"country": "GR", "city": "Ateny"},
    {"country": "SE", "city": "Sztokholm"},
    {"country": "NO", "city": "Oslo"},
    {"country": "FI", "city": "Helsinki"},
    {"country": "DK", "city": "Kopenhaga"},
    {"country": "IE", "city": "Dublin"},
    {"country": "UA", "city": "Kijów"},
    # ameryki
    {"country": "US", "city": "Nowy Jork"},
    {"country": "US", "city": "Waszyngton"},
    {"country": "US", "city": "San Francisco"},
    {"country": "US", "city": "Las Vegas"},
    {"country": "US", "city": "Seattle"},
    {"country": "CA", "city": "Toronto"},
    {"country": "CA", "city": "Montreal"},
    {"country": "MX", "city": "Meksyk"},
    {"country": "BR", "city": "Sao Paulo"},
    {"country": "BR", "city": "Rio de Janeiro"},
    {"country": "AR", "city": "Buenos Aires"},
    {"country": "CL", "city": "Santiago"},
    # azja, australia, afryka
    {"country": "JP", "city": "Tokio"},
    {"country": "JP", "city": "Osaka"},
    {"country": "CN", "city": "Pekin"},
    {"country": "CN", "city": "Hongkong"},
    {"country": "KR", "city": "Seul"},
    {"country": "IN", "city": "Nowe Delhi"},
    {"country": "IN", "city": "Bombaj"},
    {"country": "TH", "city": "Bangkok"},
    {"country": "SG", "city": "Singapur"},
    {"country": "AE", "city": "Dubaj"},
    {"country": "TR", "city": "Stambuł"},
    {"country": "AU", "city": "Sydney"},
    {"country": "AU", "city": "Perth"},
    {"country": "NZ", "city": "Wellington"},
    {"country": "EG", "city": "Kair"},
    {"country": "ZA", "city": "Pretoria"},
    {"country": "MA", "city": "Marrakesz"}
]    

@app.route('/', methods=['GET', 'POST'])
def index():
    pogoda = None
    if request.method == 'POST':
        # pobranie wybranego miasta z formularza
        miasto = request.form.get('miasto')
        link_dane = f"http://api.openweathermap.org/data/2.5/weather?q={miasto}&appid={KLUCZYK}&units=metric&lang=pl"
        try:
            # zapytanie do zewnętrznego API
            pobrane_dane = requests.get(link_dane)
            if pobrane_dane.status_code == 200:
                # przekazanie danych pogodowych do szablonu
                pogoda = pobrane_dane.json()
        except:
            pass
    return render_template('index.html', miasta=miasta, pogoda=pogoda)

if __name__ == '__main__':
    teraz = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"Data uruchomienia: {teraz}")
    logging.info(f"Autor: Kamil Rodak")
    logging.info(f"Port: {PORT}")
    app.run(host='0.0.0.0', port=PORT)