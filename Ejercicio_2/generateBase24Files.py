import random
import string
from datetime import datetime, timedelta

# Definición de la estructura de cada sección
tipoTransacao = ["001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","051","052","020","021","022","023","030","031","032","034","040"]
meioCaptura = ["001","003","004","005","006","007","008","009","010","011","012","013","014"]
bandeira = ["M ","V ","X ","9 ","A ","E ","H ","L ","G ","T ","B ","U ","F ","C ","S ","D "]
codProduto = ["0 ","1 ","2 ","3 ","4 ","5 ","6 ","7 ","8 ","9 ","A ","B ","C ","D ","E ","J ","F ","M ","P ","Q ","U "]

HEADER_FIELDS = [
    ('TIP-REGISTRO',2,'00'),
	('DAT-PROCESSAMENTO',8),
	('HOR-PROCESSAMENTO',6),
	('NOM-ARQUIVO',50),
	('SEQ-ARQUIVO',9),
	('VER-LAYOUT',5),
	('IND-AMBIENTE',2),
	('FILLER',218),
]

BODY_FIELDS = [
    ('TIP-REGISTRO',2,'01'),
    ('DAT-PROCESSAMENTO-BODY',8),
    ('COD-ESTABELECIMENTO',9),
    ('COD-TERMINAL',8),
    ('COD-TIPO-TRANSACAO',3),
    ('TIPO-MEIO-CAPTURA',3),
    ('DATA-TRANSACAO',8),
    ('HORA-TRANSACAO',6),
    ('NSU-CAPTURA',12),
    ('NSU-TERMINAL',12),
    ('VALOR-TRANSACAO',18),
    ('COD-NEGADA-EMISSOR',3),
    ('COD-NEGADA-BANDEIRA',3),
    ('COD-NEGADA-BASE24',3),
    ('TRAN-CODE',6),
    ('BANDEIRA',2),
    ('VALOR-MERCHANT-FEE',12),
    ('PORCERT-MERCHANT-FEE',5),
    ('VALOR-INTERC-FEE',12),
    ('PORC-INTERC-FEE',5),
    ('COD-AUT-EMISSOR',6),
    ('ID-TRANSACAO',18),
    ('ESTORNO-DATA-TRANSACAO',8),
    ('ESTORNO-HORA-TRANSACAO',6),
    ('ESTORNO-NSU-TERMINAL',9),
    ('ESTORNO-NSU-CAPTURA',9),
    ('CNPJ',14),
    ('COD-PRODUTO',2),
    ('DATA-COMPETÊNCIA',8),
    ('RESPONDER',1),
    ('PARCEIRO',4),
    ('PROPRIEDADE-MEIO-CAPTURA',3),
    ('AUTENTICADA',1),
    ('MCC-GET',4),
    ('MCC-PARCEIRO',4),
    ('COD-ESTAB-PARCEIRO',11),
    ('COD-MOEDA',3),
    ('TIPO-PESSOA',1),
    ('FILLER',48),
]

TRAILER_FIELDS = [
    ('TP-REGISTRO',2,'99'),
    ('QT-REGISTRO',9),
    ('FILLER',289),
]

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
    
    return fecha_transaccion.strftime('%Y%m%d')

def generar_dato_aleatorio(campo, longitud):
    """Genera un dato aleatorio para un campo de longitud fija."""
    nombre_campo = campo[0]

    if nombre_campo == 'TIP-REGISTRO':
        return campo[2]

    init_process_date = datetime.now().replace(day=1)
    random_process_date = generar_fecha_mes_anterior()

    # Datos para el header
    if nombre_campo == 'DAT-PROCESSAMENTO':
        return init_process_date.strftime('%Y%m%d')
    if 'HOR' in nombre_campo:
        return datetime.now().strftime('%H%M%S')
    if nombre_campo == 'NOM-ARQUIVO':
        return 'TRANSACOES NAO FINANCEIRAS'.ljust(longitud)
    if 'SEQ' in nombre_campo:
        return str(random.randint(1, 999999999)).zfill(longitud)
    if 'VER' in nombre_campo:
        return '1'.zfill(longitud)
    if 'IND' in nombre_campo:
        return random.choice(['01', '02', '03'])  # Ejemplo de ambientes 01=Producción, 02=Homologación, 03=Desarrollo
    if 'FILLER' in nombre_campo:
        return ''.ljust(longitud)

    # Datos para el body
    if nombre_campo == 'DAT-PROCESSAMENTO-BODY':
        return random_process_date
    if 'COD-ESTABELECIMENTO' in nombre_campo:
        return str(random.randint(100000000, 999999999)).zfill(longitud)
    if 'COD-TERMINAL' in nombre_campo:
        return str(random.randint(1000000, 9999999)).zfill(longitud)
    if 'COD-TIPO-TRANSACAO' in nombre_campo:
        return str(random.choice(tipoTransacao)).zfill(longitud)
    if 'TIPO-MEIO-CAPTURA' in nombre_campo:
        return str(random.choice(meioCaptura)).zfill(longitud)
    if 'DATA-TRANSACAO' in nombre_campo:
        return random_process_date
    if 'NSU-CAPTURA' in nombre_campo:
        return str(random.randint(100000000000, 999999999999)).zfill(longitud)
    if 'NSU-TERMINAL' in nombre_campo:
        return str(random.randint(100000000000, 999999999999)).zfill(longitud)
    if 'VALOR-TRANSACAO' in nombre_campo:
        # Valor con 2 decimales, longitud total 18 (ej. 000000005525)
        valor = random.uniform(1.0, 99999999.99)
        return f'{valor:.2f}'.replace('.', '').zfill(longitud)
    if 'COD-NEGADA-EMISSOR' in nombre_campo:
        return str(random.randint(100, 999)).zfill(longitud)
    if 'COD-NEGADA-BANDEIRA' in nombre_campo:
        return str(random.randint(100, 999)).zfill(longitud)
    if 'COD-NEGADA-BASE24' in nombre_campo:
        return str(random.randint(100, 999)).zfill(longitud)
    if 'TRAN-CODE' in nombre_campo:
        return str(random.randint(100000, 999999)).zfill(longitud)
    if 'BANDEIRA' in nombre_campo:
        return str(random.choice(bandeira))
    if 'VALOR-MERCHANT-FEE' in nombre_campo:
        valor = random.uniform(0.0, 9999999999.99)
        return f'{valor:.2f}'.replace('.', '').zfill(longitud)
    if 'PORCERT-MERCHANT-FEE' in nombre_campo:
        porc = random.uniform(0.0, 999.99)
        return f'{porc:.2f}'.replace('.', '').zfill(longitud)
    if 'VALOR-INTERC-FEE' in nombre_campo:
        valor = random.uniform(0.0, 9999999999.99)
        return f'{valor:.2f}'.replace('.', '').zfill(longitud)
    if 'PORC-INTERC-FEE' in nombre_campo:
        porc = random.uniform(0.0, 999.99)
        return f'{porc:.2f}'.replace('.', '').zfill(longitud)
    if 'COD-AUT-EMISSOR' in nombre_campo:
        return str(random.randint(100000, 999999)).zfill(longitud)
    if 'ID-TRANSACAO' in nombre_campo:
        return str(random.randint(100000000000000000, 999999999999999999)).zfill(longitud)
    if 'ESTORNO-DATA-TRANSACAO' in nombre_campo:
        return ''.ljust(longitud)
    if 'ESTORNO-HORA-TRANSACAO' in nombre_campo:
        return ''.ljust(longitud)
    if 'ESTORNO-NSU-TERMINAL' in nombre_campo:
        return ''.ljust(longitud)
    if 'ESTORNO-NSU-CAPTURA' in nombre_campo:
        return ''.ljust(longitud)
    if 'CNPJ' in nombre_campo:
        return str(random.randint(10000000000000, 99999999999999)).zfill(longitud)
    if 'COD-PRODUTO' in nombre_campo:
        return random.choice(codProduto)
    if 'DATA-COMPETÊNCIA' in nombre_campo:
        return datetime.now().strftime('%Y%m%d')
    if 'RESPONDER' in nombre_campo:
        return random.choice(['A', 'E', 'L'])
    if 'PARCEIRO' in nombre_campo:
        return str(random.randint(1, 9999)).zfill(longitud)
    if 'PROPRIEDADE-MEIO-CAPTURA' in nombre_campo:
        return random.choice(['A', 'E', 'L'])
    if 'AUTENTICADA' in nombre_campo:
        return random.choice(['S', 'N', ' '])
    if 'MCC-GET' in nombre_campo:
        return str(random.randint(1000, 9999)).zfill(longitud)
    if 'MCC-PARCEIRO' in nombre_campo:
        return str(random.randint(1000, 9999)).zfill(longitud)
    if 'COD-ESTAB-PARCEIRO' in nombre_campo:
        return str(random.randint(10000000000, 99999999999)).zfill(longitud)
    if 'COD-MOEDA' in nombre_campo:
        return random.choice(['032', '036', '124', '156', '344', '356', '392', '410', '484', '578', '702', '710', '724', '752', '756', '826', '840'])
    if 'TIPO-PESSOA' in nombre_campo:
        return random.choice(['0', '1', '2'])

    # Datos para el trailer
    if 'TP-REGISTRO' in nombre_campo:
        return campo[2]
    if 'QT-REGISTRO' in nombre_campo:
        return ''.zfill(longitud)  # Se calculará más tarde

    # Para cualquier otro campo no especificado
    return ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))


def generar_linea(estructura, datos_aleatorios):
    """Crea una línea de longitud fija a partir de una estructura y datos."""
    linea = ''
    for i, estructura_int in enumerate(estructura):
        dato = datos_aleatorios[i]
        linea += str(dato).ljust(estructura_int[1])
    return linea

def generar_header():
    """Genera la línea del header."""
    datos = [generar_dato_aleatorio(campo, campo[1]) for campo in HEADER_FIELDS]
    return generar_linea(HEADER_FIELDS, datos)

def generar_body(num_registros):
    """Genera una lista de líneas para el body."""
    body_registros = []
    for _ in range(num_registros):
        datos = [generar_dato_aleatorio(campo, campo[1]) for campo in BODY_FIELDS]
        body_registros.append(generar_linea(BODY_FIELDS, datos))
    return body_registros

def generar_trailer(num_registros_body):
    """Genera la línea del trailer con los valores calculados."""
    trailer_datos = [generar_dato_aleatorio(campo, campo[1]) for campo in TRAILER_FIELDS]
    trailer_datos[1] = str(num_registros_body + 2).zfill(len(trailer_datos[1]))  # +2 por header y trailer
    return generar_linea(TRAILER_FIELDS, trailer_datos)

def crear_archivo_longitud_fija(nombre_archivo):
    """
    Función principal para crear el archivo con header, body y trailer.
    """

    # --- Solicitar cantidad de registros ---
    while True:
        try:
            num_registros_body = int(input("Ingrese la cantidad de registros a generar: "))
            if num_registros_body < 1:
                print("Por favor, ingrese un número mayor a cero.")
            else:
                break
        except ValueError:
            print("Entrada inválida. Por favor, ingrese un número entero.")

    # Generar el header (un solo registro)
    header = generar_header()

    # Generar el body (múltiples registros)
    body = generar_body(num_registros_body)

    # Calcular los valores del trailer a partir de los datos del body
    suma_cantidades = 0
    for registro in body:
        # Extraer la cantidad del registro del body (pos 7 a 10)
        cantidad_str = registro[7:11].strip()
        if cantidad_str:
            suma_cantidades += int(cantidad_str)

    # Generar el trailer (un solo registro)
    trailer = generar_trailer(num_registros_body)

    # Escribir todas las partes en el archivo
    try:
        # Abre el archivo en modo escritura ('w')
        with open(nombre_archivo, 'w') as f:
            f.write(header + '\n')
            for registro_body in body:
                f.write(registro_body + '\n')
            f.write(trailer + '\n')

            print("-" * 50)
        print(f"✅ ¡Archivo generado exitosamente!")
        print(f"   Nombre del archivo: {nombre_archivo}")
        print(f"   Registros creados: {num_registros_body} + 2 (header y trailer)")
        print("-" * 50)

    except Exception as e:
        print(f"❌ Ocurrió un error al escribir el archivo: {e}")

# --- Ejecutar el programa ---
if __name__ == "__main__":
    today = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0).strftime('%Y%m')
    today_int = int(today) - 1
    nombre_archivo_salida = 'FAT_' + str(today_int) + '_training.csv'
    crear_archivo_longitud_fija(nombre_archivo_salida)