import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os
from datetime import datetime

# Conexión con tus secretos de Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def obtener_resultados():
    # Usamos el link de TuAzar que es muy confiable para Lotto Rey y otros
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url_fuente, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        resultados_encontrados = []

        # Buscamos todas las tablas de resultados en la página
        tablas = soup.find_all('table', class_='table-resultados')

        for tabla in tablas:
            # Identificamos el nombre de la lotería (Lotto Rey, La Granjita, etc.)
            titulo_seccion = tabla.find_previous('h2')
            loteria_nombre = titulo_seccion.text.strip() if titulo_seccion else "Lotería"

            # Sacamos las filas de la tabla (la primera fila después del encabezado)
            filas = tabla.find_all('tr')
            if len(filas) > 1:
                ultima_jugada = filas[1] 
                
                # Extraemos Hora y Animal
                hora = ultima_jugada.find('td', class_='td-res-hora').text.strip()
                animal_con_numero = ultima_jugada.find('td', class_='td-res-animal').text.strip()

                resultados_encontrados.append({
                    "nombre": animal_con_numero,
                    "loteria": loteria_nombre,
                    "hora": hora
                })
        
        return resultados_encontrados
    except Exception as e:
        print(f"Error al leer la página: {e}")
        return []

def guardar_en_base_de_datos():
    lista = obtener_resultados()
    
    if not lista:
        print("No se encontraron resultados nuevos en este momento.")
        return

    for item in lista:
        try:
            # Esto guarda los datos en tu tabla 'resultados'
            data = {
                "nombre": item['nombre'],
                "loteria": item['loteria'],
                "hora": item['hora']
            }
            # El robot intenta insertar. Si ya existe, no se duplica.
            supabase.table("resultados").insert(data).execute()
            print(f"✅ Guardado: {item['loteria']} - {item['nombre']} ({item['hora']})")
        except Exception as e:
            # Si da error es porque quizás ya estaba guardado o falta una columna
            print(f"Aviso: No se guardó {item['loteria']} (posible duplicado o error de tabla)")

if __name__ == "__main__":
    guardar_en_base_de_datos()
            
