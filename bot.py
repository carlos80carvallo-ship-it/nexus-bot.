import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

# Conexión
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar_animalitos():
    # Probamos con la página principal de hoy
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        req = requests.get(url_fuente, headers=headers, timeout=20)
        soup = BeautifulSoup(req.text, 'html.parser')
        
        # Buscamos todas las tablas de resultados
        tablas = soup.find_all('table')
        print(f"Buscando en {len(tablas)} tablas...")

        for tabla in tablas:
            # Intentamos sacar el nombre de la lotería de arriba de la tabla
            titulo = tabla.find_previous(['h2', 'h3', 'strong'])
            nombre_lotto = titulo.text.strip() if titulo else "Animalitos"

            filas = tabla.find_all('tr')
            for fila in filas[1:2]: # Solo la última jugada
                celdas = fila.find_all('td')
                if len(celdas) >= 2:
                    hora = celdas[0].text.strip()
                    resultado_full = celdas[1].text.strip()
                    
                    # Separar numero y nombre (Ej: "10 GALLO")
                    partes = resultado_full.split(' ', 1)
                    num = partes[0] if len(partes) > 0 else ""
                    animal = partes[1] if len(partes) > 1 else resultado_full

                    # Guardar en Supabase
                    data = {
                        "numero": num,
                        "animal": animal,
                        "loteria": nombre_lotto,
                        "hora": hora,
                        "fecha": datetime.now().strftime("%Y-%m-%d")
                    }
                    
                    supabase.table("resultados").insert(data).execute()
                    print(f"✅ Guardado: {nombre_lotto} - {animal}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar_animalitos()
    
