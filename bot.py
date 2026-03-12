import requests
from bs4 import BeautifulSoup
from supabase import create_client
import os

# Configuración de seguridad (Usa tus secretos de GitHub)
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def obtener_animalito():
    # Intentamos sacar el resultado de TuAzar
    url_fuente = "https://www.tuazar.com/loteria/animalitos/resultados/"
    try:
        response = requests.get(url_fuente, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Buscamos el primer animal y número que aparece en la tabla
        nombre = soup.find('td', class_='td-animal-nombre').text.strip()
        numero = soup.find('td', class_='td-animal-numero').text.strip()
        
        return {"nombre": nombre, "numero": numero}
    except Exception as e:
        print(f"Error leyendo la página: {e}")
        return None

def ejecutar_robot():
    resultado = obtener_animalito()
    
    if resultado:
        # Enviamos el animalito a tu tabla 'resultados' en Supabase
        data = {
            "nombre": resultado['nombre'],
            "numero": resultado['numero']
        }
        supabase.table("resultados").insert(data).execute()
        print(f"✅ ¡Robot trabajó con éxito! Guardó: {resultado['nombre']}")
    else:
        print("❌ El robot no encontró resultados nuevos todavía.")

if __name__ == "__main__":
    ejecutar_robot()
    
