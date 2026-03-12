import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

# Conexión con tus llaves
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar_para_nexus():
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        r = requests.get(url_fuente, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        tablas = soup.find_all('table', class_='table-resultados')
        
        for tabla in tablas:
            # Buscamos el título (Lotto Activo, La Granjita, etc.)
            titulo_h2 = tabla.find_previous('h2')
            if not titulo_h2: continue
            lotto_nombre = titulo_h2.text.strip()
            
            # Solo nos interesan las 4 loterías de tu App
            loterias_validas = ["Lotto Activo", "La Granjita", "Guácharo Activo", "Lotto Rey"]
            if lotto_nombre not in loterias_validas: continue

            # Sacamos la última fila de resultados
            fila = tabla.find('tr', class_='fila-resultado') or tabla.find_all('tr')[1]
            if fila:
                cells = fila.find_all('td')
                hora_web = cells[0].text.strip()
                resultado_web = cells[1].text.strip()
                
                # Separar número y animal
                partes = resultado_web.split(' ', 1)
                num = partes[0] if len(partes) > 0 else ""
                nom = partes[1] if len(partes) > 1 else resultado_web

                # DATOS PARA TU APP (respetando tus nombres de columna)
                datos = {
                    "fecha": datetime.now().strftime("%Y-%m-%d"),
                    "Lotto": lotto_nombre, # Con L mayúscula como en tu JS
                    "hora": hora_web,
                    "numero": num,
                    "animal": nom.upper()
                }
                
                # Guardar en Supabase
                try:
                    # Usamos upsert para que si ya existe la combinación, no se repita
                    supabase.table("resultados").insert(datos).execute()
                    print(f"✅ Publicado en Nexus: {lotto_nombre} {hora_web}")
                except:
                    print(f"Aviso: {lotto_nombre} {hora_web} ya estaba publicado.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar_para_nexus()
    
