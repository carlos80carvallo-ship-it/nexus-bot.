import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

# Conexión
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def capturar():
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # Este mapa asegura que el nombre sea EXACTO al que tú usas
    mapa_lottos = {
        "LOTTO ACTIVO": "Lotto Activo",
        "LA GRANJITA": "La Granjita",
        "GUÁCHARO ACTIVO": "Guácharo Activo",
        "LOTTO REY": "Lotto Rey"
    }

    try:
        r = requests.get(url_fuente, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        tablas = soup.find_all('table', class_='table-resultados')
        
        for tabla in tablas:
            titulo_h2 = tabla.find_previous('h2')
            if not titulo_h2: continue
            
            nombre_web = titulo_h2.text.strip().upper()
            
            # Si la lotería está en nuestra lista
            if nombre_web in mapa_lottos:
                nombre_final = mapa_lottos[nombre_web]
                
                # Buscamos la fila del resultado
                fila = tabla.find('tr', class_='fila-resultado') or tabla.find_all('tr')[1]
                if fila:
                    celdas = fila.find_all('td')
                    hora_v = celdas[0].text.strip()
                    res_v = celdas[1].text.strip()
                    
                    if res_v and len(res_v) > 2:
                        partes = res_v.split(' ', 1)
                        num = partes[0]
                        ani = partes[1] if len(partes) > 1 else res_v

                        # Insertamos EXACTAMENTE como lo haces tú manualmente
                        datos = {
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                            "Lotto": nombre_final, # Aquí forzamos el nombre correcto
                            "hora": hora_v,
                            "numero": num,
                            "animal": ani.upper()
                        }
                        
                        # Guardar en la tabla resultados
                        supabase.table("resultados").insert(datos).execute()
                        print(f"✅ Robot imitó a Carlos con éxito: {nombre_final}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    capturar()
    
