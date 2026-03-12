import os
from supabase import create_client
from datetime import datetime

# Conexión segura usando tus secretos
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

def publicar_prueba():
    datos = {
        "Lotto": "Nexus Bot",
        "hora": datetime.now().strftime("%I:%M %p"),
        "numero": "00",
        "animal": "BALLENA",
        "fecha": datetime.now().strftime("%Y-%m-%d")
    }
    try:
        supabase.table("resultados").insert(datos).execute()
        print("✅ ¡Éxito! Revisa tu tabla 'resultados' en Supabase.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    publicar_prueba()
  
