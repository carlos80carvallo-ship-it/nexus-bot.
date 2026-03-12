import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar():
    # Cambiamos a una fuente más permisiva para robots
    url_fuente = "https://www.notiactual.com/resultados-de-los-animalitos-hoy-lotto-activo-la-granjita-y-otros/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    mapa_lottos = {
        "LOTTO ACTIVO": "Lotto Activo",
        "LA GRANJITA": "La Granjita",
        "GUÁCHARO ACTIVO": "Guácharo Activo",
        "LOTTO REY": "Lotto Rey"
    }

    try:
        r = requests.get(url_fuente, headers=headers, timeout=25)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # En esta página los resultados suelen estar en celdas de tablas fuertes
        filas = soup.find_all('tr')
        
        for fila in filas:
            texto_fila = fila.text.upper()
            
            for clave, nombre_real in mapa_lottos.items():
                if clave in texto_fila:
                    celdas = fila.find_all('td')
                    if len(celdas) >= 2:
                        # Extraemos hora y resultado (ej: "10:00 AM - 14 MONO")
                        contenido = celdas[1].text.strip().upper()
                        
                        # Limpiamos el texto para sacar número y animal
                        # Buscamos el último resultado publicado en la fila
                        import re
                        match = re.search(r'(\d{1,2}:\d{2}\s?(?:AM|PM))\s*[:-]?\s*(\d{1,2})\s*([A-ZÁÉÍÓÚÑ]+)', contenido)
                        
                        if match:
                            hora_v = match.group(1)
                            num = match.group(2)
                            ani = match.group(3)

                            datos = {
                                "fecha": datetime.now().strftime("%Y-%m-%d"),
                                "Lotto": nombre_real,
                                "hora": hora_v,
                                "numero": num,
                                "animal": ani
                            }
                            
                            # Insertar
                            supabase.table("resultados").insert(datos).execute()
                            print(f"✅ Notiactual -> {nombre_real}: {num} {ani}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar()
                        
