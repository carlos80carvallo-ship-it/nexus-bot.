import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime
import re

# Conexión
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar():
    # Nueva fuente: Notiactual es más estable para bots
    url_fuente = "https://www.notiactual.com/resultados-de-los-animalitos-hoy-lotto-activo-la-granjita-y-otros/"
    
    # Cabecera para engañar al servidor y que piense que somos una persona en Chrome
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    
    mapa_lottos = {
        "LOTTO ACTIVO": "Lotto Activo",
        "LA GRANJITA": "La Granjita",
        "GUÁCHARO ACTIVO": "Guácharo Activo",
        "LOTTO REY": "Lotto Rey"
    }

    try:
        r = requests.get(url_fuente, headers=headers, timeout=30)
        # Forzamos la codificación para que no salgan símbolos raros en los acentos
        r.encoding = 'utf-8' 
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Buscamos en todas las filas de tabla
        filas = soup.find_all('tr')
        
        for fila in filas:
            texto_fila = fila.get_text().upper()
            
            for clave, nombre_real in mapa_lottos.items():
                if clave in texto_fila:
                    # Buscamos el patrón: HORA - NUMERO ANIMAL
                    # Ejemplo: "06:00 PM 11 CURUCHUCHO"
                    match = re.search(r'(\d{1,2}:\d{2}\s?(?:AM|PM))[\s\-:]*(\d{1,2})\s*([A-ZÁÉÍÓÚÑ]+)', texto_fila)
                    
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
                        
                        # Guardar en Supabase
                        supabase.table("resultados").insert(datos).execute()
                        print(f"✅ Robot publicó desde Notiactual: {nombre_real} {hora_v}")
                        
    except Exception as e:
        print(f"Error en el robot: {e}")

if __name__ == "__main__":
    capturar()
    
