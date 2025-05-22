import random
from datetime import datetime, timedelta

from entidad.Estado import Estado
from entidad.Empleado import Empleado
from entidad.Usuario import Usuario
from entidad.Sesion import Sesion
from entidad.EventoSismico import EventoSismico
from entidad.SerieTemporal import SerieTemporal
from entidad.AlcanceSismo import AlcanceSismo
from entidad.OrigenDeGeneracion import OrigenDeGeneracion
from entidad.ClasificacionSismo import ClasificacionSismo
from entidad.EstacionSismologica import EstacionSismologica
from entidad.Sismografo import Sismografo

empleados = [Empleado("Juan", "Perez", "juan@gmail.com", "111-1111"),
             Empleado("Pepe", "Fernandez", "pepe@gmail.com", "222-2222"),
             Empleado("Clara", "Gonzalez", "clara@gmail.com", "333-3333")]

usuarios = [Usuario("juan123", "1234", empleados[0]),
            Usuario("elpepe", "qwerty", empleados[1]),
            Usuario("clari", "contraseña", empleados[2])]

sesion = Sesion(usuarios[random.randrange(0, len(usuarios))], datetime.now())

estados = [Estado("AutoDetectado", "Evento Sismico"),
            Estado("AutoConfirmado", "Evento Sismico"),
            Estado("BloqueadoEnRevision", "Evento Sismico"),
            Estado("Confirmado", "Evento Sismico"),
            Estado("Rechazado", "Evento Sismico"),
            Estado("Derivado", "Evento Sismico")]

alcances = [AlcanceSismo("Local"), AlcanceSismo("Regional"), AlcanceSismo("Tele Sismo")]
origenes = [OrigenDeGeneracion("Interplaca"), OrigenDeGeneracion("Volcanico"), OrigenDeGeneracion("Explosion de mina")]
clasificaciones = [ClasificacionSismo("Superficial", 0, 60),
                   ClasificacionSismo("Intermedio", 60, 300),
                   ClasificacionSismo("Profundo", 300, 650)]

estaciones = [EstacionSismologica(1, "CORDOBA"), EstacionSismologica(2, "TUCUMAN"),
              EstacionSismologica(3, "LA RIOJA")]

sismografos = [Sismografo(i + 1, datetime(2021 + i, i + 1, i + 1), 1234 + 1111*i, estaciones[i]) for i in range(3)]

eventos = []
# eventos random
for i in range(1, 5):
    inicio = datetime(2025, 5, i)
    fin = inicio + timedelta(minutes=random.randint(5, 30))
    latitud = random.uniform(-90.0, 90.0)
    longitud = random.uniform(-180, 180)
    magnitud = random.uniform(0.1, 10)
    estado = estados[1] if magnitud >= 4 else estados[5] if magnitud >= 3 else estados[4]
    ev = EventoSismico(inicio, fin, latitud, longitud, latitud + random.uniform(-0.1, 0.1),
                       longitud + random.uniform(-0.1, 0.1), magnitud, None,
                       None, None, [], estado)
    eventos.append(ev)
# eventos AutoDetectados
for i in range(3):
    inicio = datetime.now() - timedelta(seconds=random.randrange(0, 300))
    fin = None  # esta ocurriendo ahora
    latitud = random.uniform(-90.0, 90.0)
    longitud = random.uniform(-180, 180)
    magnitud = random.uniform(0.1, 3.99)
    estado = estados[0]   # AutoDetectado
    alcance = alcances[random.randrange(len(alcances))]
    clasificacion = clasificaciones[random.randrange(len(clasificaciones))]
    origen = origenes[random.randrange(len(origenes))]
    ev = EventoSismico(inicio, fin, latitud, longitud, latitud + random.uniform(-0.1, 0.1),
                       longitud + random.uniform(-0.1, 0.1), magnitud, alcance, clasificacion, origen,
                       [SerieTemporal(inicio, inicio,
                                      50, [], sismografos[random.randrange(len(sismografos))]),
                        SerieTemporal(inicio, inicio + timedelta(seconds=random.uniform(60, 300)),
                                      50, [], sismografos[random.randrange(len(sismografos))]),
                        SerieTemporal(inicio, inicio + timedelta(seconds=random.uniform(60, 300)),
                                      50, [], sismografos[random.randrange(len(sismografos))])],
                       estado)
    eventos.append(ev)

