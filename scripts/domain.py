# domain.py
from datetime import datetime, timedelta

class Estado:
    def __init__(self, nombre):
        self.nombre = nombre

# Predefino los estados
ESTADO_AUTODETECTADO = Estado("Auto detectado")
ESTADO_AUTOCONFIRMADO = Estado("Auto confirmado")
ESTADO_CONFIRMADO    = Estado("Confirmado")
ESTADO_RECHAZADO     = Estado("Rechazado")
ESTADO_REV_EXPERTO   = Estado("Revisión a Experto")
ESTADO_BLOQUEADO     = Estado("Bloqueado en revision") # NUEVO

class CambioEstado:
    def __init__(self, evento, estado, fecha_hora, responsable=None):
        self.evento = evento
        self.estado = estado
        self.fecha_hora = fecha_hora
        self.responsable = responsable

class Rol:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

class Empleado:
    def __init__(self, apellido, email, nombre, telefono, rol):
        self.apellido = apellido
        self.email = email
        self.nombre = nombre
        self.telefono = telefono
        self.rol = rol

class AlcanceSismo:
    def __init__(self, nombre):
        self.nombre = nombre

class ClasificacionSismo:
    def __init__(self, nombre):
        self.nombre = nombre

class OrigenDeGeneracion:
    def __init__(self, nombre):
        self.nombre = nombre

class TipoDeDato:
    def __init__(self, nombre):
        self.nombre = nombre

class EstacionSismologica:
    def __init__(self, codigo):
        self.codigo = codigo

class MuestraSismos:
    def __init__(self, fecha_hora, tipo_de_dato, valor):
        self.fecha_hora = fecha_hora
        self.tipo_de_dato = tipo_de_dato
        self.valor = valor

class SerieTemporal:
    def __init__(self, estacion, muestras):
        self.estacion = estacion
        self.muestras = muestras

class EventoSismico:
    def __init__(self, id, fecha_ini, fecha_fin, e_longitud, e_latitud, h_longitud, h_latitud, profundidad, valor_magnitud,
                 alcance, clasificacion, origen, series_temporales, estado=None):
        self.id = id
        self.fecha_ini = fecha_ini
        self.fecha_fin = fecha_fin
        self.longitud_epi = e_longitud
        self.latitud_epi = e_latitud
        self.longitud_hipo = h_longitud
        self.latitud_hipo = h_latitud
        self.profundidad = profundidad
        self.valor_magnitud = valor_magnitud
        self.alcance = alcance
        self.clasificacion = clasificacion
        self.origen = origen
        self.series_temporales = series_temporales
        self.estado = estado or ESTADO_AUTODETECTADO
        self.historial_estados = []
        self.analista_revisor = None
        self.fecha_revision = None

    def cambiar_estado(self, nuevo_estado, responsable=None):
        now = datetime.now()
        cambio = CambioEstado(self, nuevo_estado, now, responsable)
        self.estado = nuevo_estado
        self.historial_estados.append(cambio)
        if responsable:
            self.analista_revisor = responsable
            self.fecha_revision = datetime.now()

# --- Datos hardcodeados de ejemplo con clasificación basada en magnitud ---

rol_analista = Rol("-", "Analista de Sismos")
analista = Empleado("Becerra", "maximoi.becerra@gmail.com", "Máximo", "3512562340", rol_analista)

# Alcance y origen (igual que antes)
alcances = [AlcanceSismo("Local"), AlcanceSismo("Regional"), AlcanceSismo("Global")]
origenes = [OrigenDeGeneracion("Tectónico"), OrigenDeGeneracion("Volcánico"), OrigenDeGeneracion("Artificial")]

# Tipos de dato y estaciones
tipos_dato = [TipoDeDato("Velocidad de onda"), TipoDeDato("Frecuencia de onda")]
estaciones = [EstacionSismologica(1), EstacionSismologica(2), EstacionSismologica(3)]

# Clasificaciones posibles
CL_MICRO       = ClasificacionSismo("Micro")
CL_LEVE        = ClasificacionSismo("Leve")
CL_MODERADO    = ClasificacionSismo("Moderado")
CL_CONSIDERABLE= ClasificacionSismo("Considerable")
CL_FUERTE      = ClasificacionSismo("Fuerte")
CL_DESTRUCTIVO = ClasificacionSismo("Destructivo")

def obtener_clasificacion(mag):
    if mag < 2.0:
        return CL_MICRO
    elif mag < 4.0:
        return CL_LEVE
    elif mag < 5.0:
        return CL_MODERADO
    elif mag < 6.0:
        return CL_CONSIDERABLE
    elif mag < 7.0:
        return CL_FUERTE
    else:
        return CL_DESTRUCTIVO

def generar_series_con_tres_estaciones(fecha_base, magnitud):
    muestras_base = [
        MuestraSismos(fecha_base, tipos_dato[0], magnitud * 2),
        MuestraSismos(fecha_base, tipos_dato[1], magnitud * 3)
    ]
    series = []
    for est in estaciones[:3]:  # Tomamos exactamente 3 estaciones
        # Clonamos las muestras para cada estación
        muestras = [
            MuestraSismos(fecha_base, tipos_dato[0], magnitud * 2),
            MuestraSismos(fecha_base, tipos_dato[1], magnitud * 3)
        ]
        series.append(SerieTemporal(est, muestras))
    return series


sample_events = []
magnitudes = [1.5, 2.5, 3.8, 4.2, 5.5, 6.3, 7.1]
for i, mag in enumerate(magnitudes, start=1):
    ini = datetime(2025, 5, i, 12, 0, 0)
    fin = ini + timedelta(minutes=5)
    clasif = obtener_clasificacion(mag)
    # Estados: si mag>=4.0 => auto confirmado; si mag<4.0 => auto detectado
    estado_inicial = ESTADO_AUTOCONFIRMADO if mag >= 4.0 else ESTADO_AUTODETECTADO
    muestras = [
        MuestraSismos(ini, tipos_dato[0], mag*2),
        MuestraSismos(ini, tipos_dato[1], mag*3)
    ]
    series = generar_series_con_tres_estaciones(ini, mag)
    ev = EventoSismico(
        id=i,
        fecha_ini=ini,
        fecha_fin=fin,
        e_longitud=-64.0 + i,
        e_latitud=-31.0 - i,
        h_longitud=-64.0 + i,
        h_latitud=-31.0 - i,
        profundidad=10.0 + i,
        valor_magnitud=mag,
        alcance=alcances[i % len(alcances)],
        clasificacion=clasif,
        origen=origenes[i % len(origenes)],
        series_temporales=series,
        estado=estado_inicial
    )
    sample_events.append(ev)

# Evento 8: estado Confirmado
ev8 = EventoSismico(
    id=8,
    fecha_ini=datetime(2025,5,8,15,0,0),
    fecha_fin=datetime(2025,5,8,15,5,0),
    e_longitud=-60.0, e_latitud=-30.0, h_longitud=-60.0, h_latitud=-30.0,
    profundidad=12.0,
    valor_magnitud=3.3,  # <4 → habría sido autodetectado, pero forzamos Confirmado
    alcance=alcances[0],
    clasificacion=obtener_clasificacion(3.3),
    origen=origenes[0],
    series_temporales=[SerieTemporal(estaciones[0], [
        MuestraSismos(datetime(2025,5,8,15,0,0), tipos_dato[0], 6.6)
    ])],
    estado=ESTADO_CONFIRMADO
)
sample_events.append(ev8)

# Evento 9: estado Rechazado
ev9 = EventoSismico(
    id=9,
    fecha_ini=datetime(2025,5,9,16,0,0),
    fecha_fin=datetime(2025,5,9,16,5,0),
    e_longitud=-61.0, e_latitud=-31.0, h_longitud=-61.0, h_latitud=-31.0,
    profundidad=8.0,
    valor_magnitud=2.2,
    alcance=alcances[1],
    clasificacion=obtener_clasificacion(2.2),
    origen=origenes[1],
    series_temporales=[SerieTemporal(estaciones[1], [
        MuestraSismos(datetime(2025,5,9,16,0,0), tipos_dato[1], 6.6)
    ])],
    estado=ESTADO_RECHAZADO
)
sample_events.append(ev9)

# Evento 10: estado Revisión a Experto
ev10 = EventoSismico(
    id=10,
    fecha_ini=datetime(2025,5,10,17,0,0),
    fecha_fin=datetime(2025,5,10,17,5,0),
    e_longitud=-62.0, e_latitud=-32.0, h_longitud=-62.0, h_latitud=-32.0,
    profundidad=15.0,
    valor_magnitud=4.8,  # >=4 → Auto confirmado por defecto, pero forzamos revisión
    alcance=alcances[2],
    clasificacion=obtener_clasificacion(4.8),
    origen=origenes[2],
    series_temporales=[SerieTemporal(estaciones[2], [
        MuestraSismos(datetime(2025,5,10,17,0,0), tipos_dato[0], 9.6)
    ])],
    estado=ESTADO_REV_EXPERTO
)
sample_events.append(ev10)


