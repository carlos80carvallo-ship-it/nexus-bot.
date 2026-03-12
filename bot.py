import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os

# Conexión automática
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar_animalitos():
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        req = requests.get(url_fuente, headers=headers, timeout=15)
        soup = BeautifulSoup(req.text, 'html.parser')
        tablas = soup.find_all('table', class_='table-resultados')
        
        for tabla in tablas:
            # Obtiene el nombre de la lotería (Lotto Rey, La Granjita, etc.)
            titulo = tabla.find_previous('h2').text.strip() if tabla.find_previous('h2') else "Lotería"
            
            filas = tabla.find_all('tr')
            if len(filas) > 1:
                top = filas[1]
                hora_txt = top.find('td', class_='td-res-hora').text.strip()
                animal_txt = top.find('td', class_='td-res-animal').text.strip()
                
                # Separamos el número del nombre (ej: "00 BALLENA")
                partes = animal_txt.split(' ', 1)
                num = partes[0] if len(partes) > 0 else ""
                nom = partes[1] if len(partes) > 1 else animal_txt

                # Guardamos en Supabase
                datos = {
                    "numero": num,
                    "animal": nom,
                    "loteria": titulo,
                    "hora": hora_txt
                }
                
                # Insertar (Supabase ignorará si está duplicado por seguridad)
                supabase.table("resultados").insert(datos).execute()
                print(f"✅ {titulo}: {nom} ({hora_txt}) guardado.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar_animalitos()
    
