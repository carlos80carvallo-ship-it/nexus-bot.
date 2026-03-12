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
    
    try:
        r = requests.get(url_fuente, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        tablas = soup.find_all('table', class_='table-resultados')
        
        for tabla in tablas:
            titulo = tabla.find_previous('h2')
            if not titulo: continue
            nombre_lotto = titulo.text.strip()
            
            # Solo procesar las que tú usas
            if nombre_lotto in ["Lotto Activo", "La Granjita", "Guácharo Activo", "Lotto Rey"]:
                fila = tabla.find('tr', class_='fila-resultado') or tabla.find_all('tr')[1]
                if fila:
                    celdas = fila.find_all('td')
                    hora_valor = celdas[0].text.strip()
                    res_valor = celdas[1].text.strip()
                    
                    partes = res_valor.split(' ', 1)
                    num = partes[0] if len(partes) > 0 else ""
                    ani = partes[1] if len(partes) > 1 else res_valor

                    datos = {
                        "fecha": datetime.now().strftime("%Y-%m-%d"),
                        "Lotto": nombre_lotto, # Coincide con tu App
                        "hora": hora_valor,    # Coincide con tu App
                        "numero": num,
                        "animal": ani.upper()
                    }
                    
                    # Guardar
                    supabase.table("resultados").insert(datos).execute()
                    print(f"✅ Guardado: {nombre_lotto}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar()
    
