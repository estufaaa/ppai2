class Sesion:
    def __init__(self, usuario, inicio):
        self.usuario = usuario
        self.fechaHoraInicio = inicio
        self.fechaHoraFin = None

    def obtenerUsuarioLogueado(self):  # deberia llamarse obtenerEmpleado en el diagrama
        return self.usuario.obtenerEmpleado()
