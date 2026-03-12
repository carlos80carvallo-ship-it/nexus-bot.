import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar():
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    loterias_validas = ["Lotto Activo", "La Granjita", "Guácharo Activo", "Lotto Rey"]
    
    try:
        r = requests.get(url_fuente, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        tablas = soup.find_all('table', class_='table-resultados')
        
        for tabla in tablas:
            titulo = tabla.find_previous('h2')
            if not titulo: continue
            nombre_lotto = titulo.text.strip()
            
            if nombre_lotto in loterias_validas:
                fila = tabla.find('tr', class_='fila-resultado') or tabla.find_all('tr')[1]
                if fila:
                    celdas = fila.find_all('td')
                    hora_v = celdas[0].text.strip()
                    res_v = celdas[1].text.strip()
                    
                    # SOLO GUARDAR SI HAY RESULTADO REAL (Evita "ESPERANDO" o vacíos)
                    if res_v and len(res_v) > 2:
                        partes = res_v.split(' ', 1)
                        num = partes[0]
                        ani = partes[1] if len(partes) > 1 else res_v

                        datos = {
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                            "Lotto": nombre_lotto,
                            "hora": hora_v,
                            "numero": num,
                            "animal": ani.upper()
                        }
                        
                        # Usamos upsert para no repetir el mismo sorteo
                        supabase.table("resultados").upsert(datos, on_conflict="fecha,Lotto,hora").execute()
                        print(f"✅ Éxito: {nombre_lotto} {hora_v}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar()
    
