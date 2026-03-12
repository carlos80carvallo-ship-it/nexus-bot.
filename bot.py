import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime
import re

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar():
    url_fuente = "https://www.notiactual.com/resultados-de-los-animalitos-hoy-lotto-activo-la-granjita-y-otros/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0'}
    
    # Mapa simplificado para búsqueda parcial
    loterias = {
        "LOTTO ACTIVO": "Lotto Activo",
        "LA GRANJITA": "La Granjita",
        "GUÁCHARO": "Guácharo Activo",
        "LOTTO REY": "Lotto Rey"
    }

    try:
        r = requests.get(url_fuente, headers=headers, timeout=30)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Buscamos todas las celdas de tabla (td)
        celdas = soup.find_all('td')
        
        for i, celda in enumerate(celdas):
            texto = celda.get_text().upper()
            
            for clave, nombre_real in loterias.items():
                if clave in texto:
                    # El resultado suele estar en la misma celda o la siguiente
                    contenido = texto + " " + (celdas[i+1].get_text().upper() if i+1 < len(celdas) else "")
                    
                    # Buscamos: HORA (00:00 AM/PM) - NUMERO - ANIMAL
                    match = re.search(r'(\d{1,2}:\d{2}\s?(?:AM|PM)).*?(\d{1,2})\s*([A-ZÁÉÍÓÚÑ]+)', contenido)
                    
                    if match:
                        datos = {
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                            "Lotto": nombre_real,
                            "hora": match.group(1),
                            "numero": match.group(2),
                            "animal": match.group(3)
                        }
                        
                        # Intentar insertar
                        try:
                            supabase.table("resultados").insert(datos).execute()
                            print(f"✅ ¡PUBLICADO!: {nombre_real} {match.group(1)}")
                        except:
                            pass # Si ya existe, lo ignora
                            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar()
    
