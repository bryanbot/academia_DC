import csv
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

# --- Variables de Configuración ---
NOMBRE_ARCHIVO = "input_transactions.csv"
DELIMITADOR = ";"

# --- Datos de Referencia para Generación Aleatoria ---
MONEDAS = ["USD"]
TIPOS_TARJETA = ["Visa", "Mastercard", "Amex", "Discover"]
NOMBRES = [Faker().name() for _ in range(20)]

def generar_registro_aleatorio():
    """Genera un solo registro de transacción con datos aleatorios."""
    
    # 1. Valor (Ejemplo: entre 1.00 y 9999.99 con 6 decimales)
    valor = round(random.uniform(0.000000, 9999.999999), 6)
    
    # 2. Moneda
    moneda = random.choice(MONEDAS)
    
    # 3. Nombre
    nombre = random.choice(NOMBRES)
    
    # 4. Fecha de Transacción (Ejemplo: Transacción del ultimo mes anterior con respecto al mes actual)
    fecha_transaccion = generar_fecha_mes_anterior()
    
    # 5. UUID (Identificador Universal Único)
    identificador_uuid = str(uuid.uuid4())
    
    # 6. Tipo de Tarjeta
    tipo_tarjeta = random.choice(TIPOS_TARJETA)
    
    return [valor, moneda, nombre, fecha_transaccion, identificador_uuid, tipo_tarjeta]

def generar_fecha_mes_anterior():
    """Genera una fecha y hora aleatoria dentro del mes anterior."""
    
    # 1. Inicio del Mes Actual (Ej: si hoy es 30/09, esto es 01/09)
    #    Usamos .date() y luego lo convertimos a datetime para simplificar
    today = datetime.now()
    inicio_mes_actual = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # 2. Final del Mes Anterior (Ej: 31/08 a las 23:59:59.999999)
    #    Simplemente restamos 1 microsegundo al inicio del mes actual
    fin_mes_anterior = inicio_mes_actual - timedelta(microseconds=1)

    # 3. Inicio del Mes Anterior (Ej: 01/08 a las 00:00:00)
    #    Vamos al día 1 de la fecha de fin_mes_anterior
    inicio_mes_anterior = fin_mes_anterior.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Cálculo de la duración total del mes anterior en segundos
    rango_segundos = int((fin_mes_anterior - inicio_mes_anterior).total_seconds())

    # Generar un desplazamiento aleatorio dentro de ese rango
    desplazamiento_segundos = random.randint(0, rango_segundos)

    # Fecha Aleatoria: Inicio del mes anterior + desplazamiento aleatorio
    fecha_transaccion = inicio_mes_anterior + timedelta(seconds=desplazamiento_segundos)
    
    return fecha_transaccion.strftime('%Y-%m-%d %H:%M:%S')

def generar_archivo_csv():
    """Pide la cantidad de registros y genera el archivo CSV."""
    
    # --- 1. Solicitar cantidad de registros ---
    while True:
        try:
            cantidad_registros = int(input("Ingrese la cantidad de registros a generar: "))
            if cantidad_registros < 1:
                print("Por favor, ingrese un número mayor a cero.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    # --- 2. Definir el encabezado (Header) ---
    header = [
        "Valor", 
        "Moneda", 
        "Nombre", 
        "Fecha de Transaccion", 
        "UUID", 
        "Tipo de Tarjeta"
    ]

    # --- 3. Generar y escribir el archivo ---
    try:
        # Abre el archivo en modo escritura ('w')
        with open(NOMBRE_ARCHIVO, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.writer(archivo_csv, delimiter=DELIMITADOR)
            
            # Escribir el encabezado
            writer.writerow(header)
            
            # Escribir los registros
            for _ in range(cantidad_registros):
                registro = generar_registro_aleatorio()
                writer.writerow(registro)

        print("-" * 50)
        print(f"✅ ¡Archivo generado exitosamente!")
        print(f"   Nombre del archivo: {NOMBRE_ARCHIVO}")
        print(f"   Registros creados: {cantidad_registros}")
        print(f"   Delimitador usado: '{DELIMITADOR}'")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Ocurrió un error al escribir el archivo: {e}")

# --- Punto de entrada principal ---
if __name__ == "__main__":
    generar_archivo_csv()