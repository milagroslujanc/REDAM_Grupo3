import random
from datetime import datetime

# Nombres peruanos de ejemplo
nombres_hombre = ["JUAN", "CARLOS", "LUIS", "MIGUEL", "JAVIER", "GUSTAVO", "DANIEL", "JESUS"]
nombres_mujer = ["MARIA", "LUISA", "CARMEN", "ANA", "ROSARIO", "PATRICIA", "SOFIA", "KAREN"]
apellidos = ["PEREZ", "GARCIA", "RAMIREZ", "RODRIGUEZ", "SALAZAR", "MENDOZA", "CASTILLO", "FLORES"]

tipos_doc = ["DNI", "Carne de Extranjeria", "Pasaporte", "Otros"]

# Simula tu lista de personas (solo 3 ejemplos)
personas = [
    {"nombres": "RONALD WILDER", "apellidos": "TORRES CORTEZ"},
    {"nombres": "JOSE FERNANDO", "apellidos": "RODRIGUEZ GUIZADO"},
    {"nombres": "BRYAN STEVE", "apellidos": "VALDIVIEZO DONAYRE"},
    {"nombres": "RENATO HAMILTON", "apellidos": "AURORA YANQUE"},
    {"nombres": "SEBASTHIAN MARTIN", "apellidos": "ALVARADO CAPCHA"},
    {"nombres": "ISAAC WILLIAMS", "apellidos": "GAVIDIA RIOJA"},
    {"nombres": "DAYBREAK THEGIAN", "apellidos": "VILLARROEL MELO"},
    {"nombres": "MILAGROS", "apellidos": "LUJAN CHAMBI"},
    {"nombres": "FRANK SUKER", "apellidos": "MUSAURIETA INGA"},
    {"nombres": "LEONARDO DARYL", "apellidos": "PABLO FLORES"},
    {"nombres": "SALVINIA", "apellidos": "PALOMINO OCHOA"},
    {"nombres": "JESUS DAVID", "apellidos": "CONTRERAS CONTRERAS"},
    {"nombres": "DANIEL ALESSANDER", "apellidos": "GUILLÉN RIOS"},
    {"nombres": "SEBASTIAN SMITH", "apellidos": "ARISTA SERNA"},
    {"nombres": "JUAN JOSE", "apellidos": "ESPETIA TORREALVA"},
    {"nombres": "GOSFREY ARMANDO", "apellidos": "LOPEZ FLORES"},
    {"nombres": "ADELY ABIGAIL", "apellidos": "SOLIS MATIAS"},
    {"nombres": "DIEGO JHARED", "apellidos": "SALHUANA GALARZA"},
    {"nombres": "OCTAVIO ALEXANDER", "apellidos": "AURIS ALIAGA"},
    {"nombres": "ZAID FRANCISCO", "apellidos": "CARDENAS LAGOS"},
    {"nombres": "YRSA SUHAMY", "apellidos": "CUETO ALVARADO"},
    {"nombres": "KARLA PATRICIA", "apellidos": "MALCA CHAVEZ"},
    {"nombres": "EDER FABIOL", "apellidos": "PAREDES QUISPE"},
    {"nombres": "JHON ALEXANDER", "apellidos": "PEREZ LOPEZ"},
    {"nombres": "JENNYFER", "apellidos": "SALAZAR HUAMAN"},
    {"nombres": "DANITZA", "apellidos": "SILVA CARRILLO"},
    {"nombres": "RONNY", "apellidos": "SOTO CARRILLO"},
    {"nombres": "JULIO", "apellidos": "TICLLA QUISPE"},
    {"nombres": "NANCY", "apellidos": "VALENCIA CORDOVA"},
    {"nombres": "PAMELA", "apellidos": "VILLALOBOS CARRILLO"},
    {"nombres": "WILMER", "apellidos": "ZAPATA CARRILLO"},
    {"nombres": "CYNTHIA", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "DANIELA", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "JHON", "apellidos": "ALVAREZ QUISPE"},
    {"nombres": "JESUS", "apellidos": "MAMANI QUISPE"},
    {"nombres": "JULIO", "apellidos": "PANIAGUA QUISPE"},
    {"nombres": "KAREN", "apellidos": "PAREDES QUISPE"},
    {"nombres": "LUIS", "apellidos": "PEREZ QUISPE"},
    {"nombres": "MARIA", "apellidos": "RODRIGUEZ QUISPE"},
    {"nombres": "MIGUEL", "apellidos": "SALAZAR QUISPE"},
    {"nombres": "NATALIA", "apellidos": "SILVA QUISPE"},
    {"nombres": "OSCAR", "apellidos": "TORO QUISPE"},
    {"nombres": "PATRICIA", "apellidos": "VALDIVIA QUISPE"},
    {"nombres": "RAFAEL", "apellidos": "VILLALOBOS QUISPE"},
    {"nombres": "SANDRA", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "TANIA", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "VIVIAN", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "WILLY", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "YAMILET", "apellidos": "ZEGARRA QUISPE"},
    {"nombres": "ZULEMA", "apellidos": "ZEGARRA QUISPE"},
]

hoy = datetime.now()
fecha_registro = hoy.strftime("%d-%m-%Y")
ultima_modificacion = hoy.strftime("%d-%m-%Y %H:%M")
año = hoy.year

lines = []
for persona in personas:
    apellidos_split = persona["apellidos"].split()
    apellido_paterno = apellidos_split[0]
    apellido_materno = apellidos_split[1] if len(apellidos_split) > 1 else ""
    nombres = persona["nombres"]
    tipo_doc = random.choice(tipos_doc)
    if tipo_doc == "DNI":
        nro_doc = str(random.randint(10000000, 99999999))
    else:
        nro_doc = ''.join(random.choices("AMBP1234567890", k=random.randint(6, 12)))
    nro_expediente = f"{random.randint(1000,9999)}-{año}"
    pension = random.randrange(300, 10001, 10)
    adeudado = round(random.uniform(0, 100000), 2)
    # Demandante: sexo opuesto (asumimos todos son hombres, así que usamos nombre de mujer)
    demandante = f"{random.choice(nombres_mujer)} {random.choice(apellidos)} {random.choice(apellidos)}"
    line = f"{apellido_paterno},{apellido_materno},{nombres},{tipo_doc},{nro_doc},{fecha_registro},{nro_expediente},{pension},{adeudado},{demandante},{ultima_modificacion}"
    lines.append(line)

# Imprime las líneas para pegar en debtors.txt
for l in lines:
    print(l)