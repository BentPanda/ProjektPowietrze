import requests

class KlientJakościPowietrza:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "http://api.airvisual.com/v2"
    
    def pobierz_jakość_powietrza_stacji(self, city: str, state: str, country: str) -> dict:
        endpoint = f"{self.base_url}/city?city={city}&state={state}&country={country}&key={self.api_key}"
        response = requests.get(endpoint)
        if response.ok:
            return response.json()
        else:
            raise Exception(f"API request failed with status code {response.status_code}")

    def waliduj_i_formatuj_dane(self, data):
        if 'data' not in data:
            raise ValueError("Invalid data structure")
        
        temp = data['data']['current']['weather']['tp']
        pressure = data['data']['current']['weather']['pr']
        if not (-50 <= temp <= 50):
            raise ValueError("Invalid temperature value")
        if not (900 <= pressure <= 1100):
            raise ValueError("Invalid pressure value")
        
        formatted_data = {
            'city': "Warsaw",
            'state': "Mazovia",
            'country': "Poland",
            'temperature': temp,
            'pressure': pressure,
            'air_quality_index': data['data']['current']['pollution']['aqius'],
            'timestamp': data['data']['current']['weather']['ts']
        }
        return formatted_data

    def wyślij_dane_do_backendu(self, data, backend_url):
        """ Sends the data to the backend server """
        response = requests.post(backend_url, json=data)
        if response.status_code == 201:
            print("Data sent successfully")
        else:
            print(f"Failed to send data: {response.status_code}")

if __name__ == "__main__":
    api_key = "e6940cc0-2038-4800-9c18-8f0078cea0d3"
    backend_url = "http://localhost:5000/data"
    klient = KlientJakościPowietrza(api_key)
    try:
        air_quality_data = klient.pobierz_jakość_powietrza_stacji("Warsaw", "Mazovia", "Poland")
        formatted_data = klient.waliduj_i_formatuj_dane(air_quality_data)
        klient.wyślij_dane_do_backendu(formatted_data, backend_url)
    except Exception as e:
        print(f"Error: {e}")
